from typing import Callable

from PyQt5.QtCore import QThread

class Thread(QThread):
  def __init__(self, target: Callable[[QThread], None]):
    QThread.__init__(self)
    self.target = target

  def run(self):
    self.target(self)
