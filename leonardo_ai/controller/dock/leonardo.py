import time
import requests
from typing import Callable

from PyQt5 import QtCore
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QByteArray, QThread

from krita import DockWidget, Node, Document, Selection

from .ui_sketch2image import Sketch2Image
from ...client.abstract import JobStatus, AbstractClient, Generation
from ...client.graphql.graphql import GraphqlClient
from ...client.restClient import RestClient
from ...view.dock import Ui_LeonardoAI
from ...config import Config, ConfigRegistry
from ...util.thread import Thread


class BalanceUpdater(QThread):

  def __init__(self, leonardoClient: Callable[[], AbstractClient], ui: Ui_LeonardoAI):
    super().__init__()

    self.getLeonardoAI = leonardoClient
    self.ui = ui

  def run(self):
    leonardoAI = self.getLeonardoAI()
    if leonardoAI is not None:
      self.ui.lcdBalance.display(str(leonardoAI.getUserInfo().Token.General))

class LeonardoDock(Sketch2Image):
  generationThread: Thread = None
  sigGenerationFailed = QtCore.pyqtSignal(Generation)
  sigGenerationDoneText2Image = QtCore.pyqtSignal(Generation)

  def __init__(self):
    super().__init__()
    self.config = Config.instance()

    self.sigGenerationFailed.connect(self.onGenerationFailed)
    self.sigGenerationDoneText2Image.connect(self.onGenerationDoneText2Image)

    self.ui.btnGenerate.clicked.connect(self.onGenerate)

    self.modelLoadingThread = None
    self._initialiseSDK()

    def getLeonardoAI(): return self.leonardoAI
    self.balanceUpdater = BalanceUpdater(getLeonardoAI, self.ui)
    self.updateBalance()

  def _initialiseSDK(self):
    clientType = self.config.get(ConfigRegistry.LEONARDO_CLIENT_TYPE)
    if clientType == "gql":
      self.leonardoAI = GraphqlClient(
        self.config.get(ConfigRegistry.LEONARDO_CLIENT_GQL_USERNAME),
        self.config.get(ConfigRegistry.LEONARDO_CLIENT_GQL_PASSWORD),
      )
    elif clientType == "rest":
      self.leonardoAI = RestClient(self.config.get(ConfigRegistry.LEONARDO_CLIENT_REST_KEY))
    else:
      self.leonardoAI = None

    if self.modelLoadingThread is not None:
      return

    def loadModels():
      models = self.leonardoAI.getModels(favorites=True)
      for model in models: self.sigAddModel.emit(model)

      models = self.leonardoAI.getModels(official=True)
      for model in models: self.sigAddModel.emit(model)

    self.modelLoadingThread = Thread(loadModels)
    self.modelLoadingThread.start()

  def canvasChanged(self, canvas):
    pass

  def onSettingsChanged(self):
    super().onSettingsChanged()
    self._initialiseSDK()
    self.updateBalance()


  def updateBalance(self):
    if self.balanceUpdater.isRunning() and not self.balanceUpdater.isFinished(): return
    self.balanceUpdater.start()

  def onGenerate(self):
    if self.ui.tabType.currentWidget() == self.ui.tabTxt2Img:
      self.onImage()
    elif self.ui.tabType.currentWidget() == self.ui.tabInpaint:
      self.onInpaint()
    elif self.ui.tabType.currentWidget() == self.ui.tabOutpaint:
      self.onOutpaint()
    elif self.ui.tabType.currentWidget() == self.ui.tabImg2Img:
      self.onImage2Image()
    elif self.ui.tabType.currentWidget() == self.ui.tabSketch2Img:
      self.onSketch2Image()

  def generate(self, genFunc: Callable[[...], str], genArgs: dict, signal: QtCore.pyqtBoundSignal):
    self.ui.btnGenerate.setEnabled(False)

    if self.generationThread is not None and self.generationThread.isRunning():
      self.generationThread.terminate()

    def run():
      genId = genFunc(**genArgs)

      while True:
        time.sleep(1)
        job = self.leonardoAI.getGenerationById(genId)

        if job.Status == JobStatus.COMPLETE:
          signal.emit(job)
          break
        if job.Status == JobStatus.FAILED:
          self.onGenerationFailed.emit(job)
          break

      self.updateBalance()

    self.generationThread = Thread(run)
    self.generationThread.start()

  def onImage(self):
    args = {
      "modelId": self.model.Id, "sdVersion": self.model.StableDiffusionVersion,
      "prompt": self.prompt, "negativePrompt": self.negativePrompt,
      "notSaveForWork": self.nsfw, "public": self.public, "numberOfImages": self.numberOfImages,
      "width": self.dimWidth, "height": self.dimHeight,
      "tiling": self.t2iTiling,
    }
    if self.ui.grpAdvancedSettings.isVisible():
      args.update({
        "guidanceScale": self.guidanceScale, "seed": self.seed, "scheduler": self.scheduler,
      })
    if self.ui.chkPhotoReal.isChecked():
      args.update({
        "photoRealStrength": self.photoRealStrength, "photoRealHighContrast": not self.photoRealRawMode, "photoRealStyle": self.photoRealStyle,
      })
    if self.ui.chkAlchemy.isChecked():
      args.update({
        "alchemyHighResolution": self.alchemyHighResolution, "alchemyContrastBoost": self.alchemyContrastBoost, "alchemyResonance": self.alchemyResonance,
        "promptMagicVersion": self.alchemyPromptMagicVersion, "promptMagicStrength": self.alchemyPromptMagicStrength, "promptMagicHighContrast": self.alchemyHighContrast,
      })

    self.generate(self.leonardoAI.createImageGeneration, args, self.sigGenerationDoneText2Image)

  @QtCore.pyqtSlot(Generation)
  def onGenerationFailed(self, generation: Generation):
    self.ui.btnGenerate.setEnabled(True)
    print("Generation failed!", generation)

  @QtCore.pyqtSlot(Generation)
  def onGenerationDoneText2Image(self, generation: Generation):
    self.ui.btnGenerate.setEnabled(True)

    document = Krita.instance().activeDocument()
    grpLayer = document.createGroupLayer(f"""AI - {generation.Prompt} - {generation.Id}""")
    document.rootNode().addChildNode(grpLayer, None)

    for generatedImage in generation.GeneratedImages:
      image = QImage.fromData(requests.get(generatedImage.Url).content)
      layer = document.createNode(generatedImage.Id, "paintlayer")
      grpLayer.addChildNode(layer, None)

      ptr = image.bits()
      ptr.setsize(image.byteCount())
      layer.setPixelData(QByteArray(ptr.asstring()), 0, 0, image.width(), image.height())

    document.crop(0, 0, max(document.width(), generation.ImageWidth), max(document.height(), generation.ImageHeight))
    document.refreshProjection()

  def onInpaint(self):
    document = Krita.instance().activeDocument()
    selection = document.selection()

    img = self.partFromSelection(document, selection)
    mask = self.maskFromSelection(selection)

    genId = self.leonardoAI.createInpaintGeneration(self.prompt, img, mask, negativePrompt=self.negativePrompt, numberOfImages=self.numberOfImages, imageStrength=0.2)
    images = None

    while True:
      job = self.leonardoAI.getGenerationById(genId)

      if job.Status == JobStatus.COMPLETE:
        images = job.GeneratedImages
        break
      if job.Status == JobStatus.FAILED:
        raise Exception("leonardo generation job failed")

      time.sleep(1)

    genImg = QImage.fromData(requests.get(images[0].Url).content)
    self.insert(genImg, document, selection)

    document.refreshProjection()

  def onOutpaint(self):
    document = Krita.instance().activeDocument()
    selection = document.selection()

    img = self.partFromSelection(document, selection)

    genId = self.leonardoAI.createInpaintGeneration(self.prompt, img, negativePrompt=self.negativePrompt, numberOfImages=self.numberOfImages, imageStrength=0.1)
    images = None

    while True:
      job = self.leonardoAI.getGenerationById(genId)

      if job.Status == JobStatus.COMPLETE:
        images = job.GeneratedImages
        break
      if job.Status == JobStatus.FAILED:
        raise Exception("leonardo generation job failed")

      time.sleep(1)

    genImg = QImage.fromData(requests.get(images[0].Url).content)
    self.insert(genImg, document, selection)

    document.refreshProjection()

    document.crop(
      min(selection.x(), 0),
      min(selection.y(), 0),
      max(selection.x() + selection.width(), document.width() + abs(min(selection.x(), 0))),
      max(selection.y() + selection.height(), document.height() + abs(min(selection.y(), 0))),
    )

  def onImage2Image(self):
    document = Krita.instance().activeDocument()
    selection = document.selection()

    img = self.partFromSelection(document, selection)

    genId = self.leonardoAI.createImage2ImageGeneration(self.prompt, img, negativePrompt=self.negativePrompt, numberOfImages=self.numberOfImages)
    images = None

    while True:
      job = self.leonardoAI.getGenerationById(genId)

      if job.Status == JobStatus.COMPLETE:
        images = job.GeneratedImages
        break
      if job.Status == JobStatus.FAILED:
        raise Exception("leonardo generation job failed")

      time.sleep(1)

    genImg = QImage.fromData(requests.get(images[0].Url).content)
    self.insert(genImg, document, selection)

    document.refreshProjection()

  def onSketch2Image(self):
    document = Krita.instance().activeDocument()
    selection = document.selection()

    img = self.partFromSelection(document, selection)

    mask = self.maskFromSelection(selection)

    genId = self.leonardoAI.createSketch2ImageGeneration(self.prompt, img, mask, negativePrompt=self.negativePrompt, numberOfImages=self.numberOfImages)
    images = None

    while True:
      job = self.leonardoAI.getGenerationById(genId)

      if job.Status == JobStatus.COMPLETE:
        images = job.GeneratedImages
        break
      if job.Status == JobStatus.FAILED:
        raise Exception("leonardo generation job failed")

      time.sleep(1)

    genImg = QImage.fromData(requests.get(images[0].Url).content)
    self.insert(genImg, document, selection)

    document.refreshProjection()

  def insert(self, image: QImage,
             document: Document | None = None,
             selection: Selection | None = None) -> Node:

    document = document if document is not None else Krita.instance().instance().activeDocument()
    selection = selection if selection is not None else document.selection()

    layer = document.createNode("Leonardo-AI", "paintlayer")
    document.rootNode().addChildNode(layer, None)

    ptr = image.bits()
    ptr.setsize(image.byteCount())
    layer.setPixelData(QByteArray(ptr.asstring()), selection.x(), selection.y(), image.width(), image.height())
    layer.cropNode(selection.x(), selection.y(), selection.width(), selection.height())

    invertedSelection = selection.duplicate()
    invertedSelection.invert()
    invertedSelection.cut(layer)

    return layer

  def maskFromSelection(self, selection: Selection | None = None) -> QImage:
    selection = selection if selection is not None else Krita.instance().activeDocument().selection()

    width = max(selection.width(), 512)
    height = max(selection.height(), 512)
    return QImage(
      selection.pixelData(selection.x(), selection.y(), width, height),
      width,
      height,
      width,
      QImage.Format_Grayscale8,
    )

  def partFromSelection(self,
                        document: Document | None = None,
                        selection: Selection | None = None) -> QImage:

    document = document if document is not None else Krita.instance().activeDocument()
    selection = selection if selection is not None else document.selection()

    width = max(selection.width(), 512)
    height = max(selection.height(), 512)
    return QImage(
      document.pixelData(selection.x(), selection.y(), width, height),
      width,
      height,
      QImage.Format_ARGB32,
    )