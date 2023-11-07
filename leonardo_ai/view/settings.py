# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './leonardo_ai/view/settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName("Settings")
        Settings.resize(400, 227)
        self.formLayout = QtWidgets.QFormLayout(Settings)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Settings)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.frame = QtWidgets.QFrame(Settings)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radClientGQL = QtWidgets.QRadioButton(self.frame)
        self.radClientGQL.setChecked(True)
        self.radClientGQL.setObjectName("radClientGQL")
        self.buttonGroup = QtWidgets.QButtonGroup(Settings)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.radClientGQL)
        self.horizontalLayout.addWidget(self.radClientGQL)
        self.radClientREST = QtWidgets.QRadioButton(self.frame)
        self.radClientREST.setObjectName("radClientREST")
        self.buttonGroup.addButton(self.radClientREST)
        self.horizontalLayout.addWidget(self.radClientREST)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.frame)
        self.grpClientGQL = QtWidgets.QFrame(Settings)
        self.grpClientGQL.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.grpClientGQL.setFrameShadow(QtWidgets.QFrame.Raised)
        self.grpClientGQL.setObjectName("grpClientGQL")
        self.formLayout_2 = QtWidgets.QFormLayout(self.grpClientGQL)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.grpClientGQL)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.inClientUsername = QtWidgets.QLineEdit(self.grpClientGQL)
        self.inClientUsername.setObjectName("inClientUsername")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inClientUsername)
        self.label_3 = QtWidgets.QLabel(self.grpClientGQL)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.inClientPassword = QtWidgets.QLineEdit(self.grpClientGQL)
        self.inClientPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.inClientPassword.setObjectName("inClientPassword")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.inClientPassword)
        self.btnTestGQL = QtWidgets.QPushButton(self.grpClientGQL)
        self.btnTestGQL.setObjectName("btnTestGQL")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.btnTestGQL)
        self.lblTestGQL = QtWidgets.QLabel(self.grpClientGQL)
        self.lblTestGQL.setText("")
        self.lblTestGQL.setObjectName("lblTestGQL")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lblTestGQL)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.grpClientGQL)
        self.grpClientRest = QtWidgets.QFrame(Settings)
        self.grpClientRest.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.grpClientRest.setFrameShadow(QtWidgets.QFrame.Raised)
        self.grpClientRest.setLineWidth(0)
        self.grpClientRest.setObjectName("grpClientRest")
        self.formLayout_3 = QtWidgets.QFormLayout(self.grpClientRest)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QtWidgets.QLabel(self.grpClientRest)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.inClientKey = QtWidgets.QLineEdit(self.grpClientRest)
        self.inClientKey.setText("")
        self.inClientKey.setObjectName("inClientKey")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.inClientKey)
        self.btnTestREST = QtWidgets.QPushButton(self.grpClientRest)
        self.btnTestREST.setObjectName("btnTestREST")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.btnTestREST)
        self.lblTestREST = QtWidgets.QLabel(self.grpClientRest)
        self.lblTestREST.setText("")
        self.lblTestREST.setObjectName("lblTestREST")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lblTestREST)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.grpClientRest)
        self.btnApply = QtWidgets.QPushButton(Settings)
        self.btnApply.setObjectName("btnApply")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.btnApply)
        self.btnClose = QtWidgets.QPushButton(Settings)
        self.btnClose.setObjectName("btnClose")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.btnClose)

        self.retranslateUi(Settings)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        _translate = QtCore.QCoreApplication.translate
        Settings.setWindowTitle(_translate("Settings", "Frame"))
        self.label.setText(_translate("Settings", "Client"))
        self.radClientGQL.setText(_translate("Settings", "GraphQL"))
        self.radClientREST.setText(_translate("Settings", "REST"))
        self.label_2.setText(_translate("Settings", "Username"))
        self.inClientUsername.setPlaceholderText(_translate("Settings", "leonardo@da-vinci.ai"))
        self.label_3.setText(_translate("Settings", "Password"))
        self.inClientPassword.setPlaceholderText(_translate("Settings", "cryptext"))
        self.btnTestGQL.setText(_translate("Settings", "Test"))
        self.label_4.setText(_translate("Settings", "API-Key"))
        self.inClientKey.setPlaceholderText(_translate("Settings", "00000000-1111-2222-3333-444444444444"))
        self.btnTestREST.setText(_translate("Settings", "Test"))
        self.btnApply.setText(_translate("Settings", "Apply Settings"))
        self.btnClose.setText(_translate("Settings", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Settings = QtWidgets.QFrame()
    ui = Ui_Settings()
    ui.setupUi(Settings)
    Settings.show()
    sys.exit(app.exec_())
