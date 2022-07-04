# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form_facturero.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_form_facturero(object):
    def setupUi(self, form_facturero):
        form_facturero.setObjectName("form_facturero")
        form_facturero.setWindowModality(QtCore.Qt.NonModal)
        form_facturero.resize(480, 275)
        form_facturero.setSizeGripEnabled(False)
        form_facturero.setModal(False)
        self.btn_box = QtWidgets.QDialogButtonBox(form_facturero)
        self.btn_box.setGeometry(QtCore.QRect(30, 240, 441, 32))
        self.btn_box.setOrientation(QtCore.Qt.Horizontal)
        self.btn_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.btn_box.setObjectName("btn_box")
        self.lbl_img = QtWidgets.QLabel(form_facturero)
        self.lbl_img.setGeometry(QtCore.QRect(10, 10, 191, 231))
        self.lbl_img.setScaledContents(False)
        self.lbl_img.setObjectName("lbl_img")
        self.frame = QtWidgets.QFrame(form_facturero)
        self.frame.setGeometry(QtCore.QRect(210, 10, 261, 231))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.lbl_titulo = QtWidgets.QLabel(self.frame)
        self.lbl_titulo.setGeometry(QtCore.QRect(6, 2, 251, 31))
        self.lbl_titulo.setObjectName("lbl_titulo")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 40, 261, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(5, 20, 10, 10)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(30)
        self.formLayout.setObjectName("formLayout")
        self.lbl_nombre = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_nombre.setObjectName("lbl_nombre")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lbl_nombre)
        self.txt_nombre = QtWidgets.QLineEdit(self.layoutWidget)
        self.txt_nombre.setObjectName("txt_nombre")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txt_nombre)
        self.lbl_estructura = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_estructura.setObjectName("lbl_estructura")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_estructura)
        self.txt_estructura = QtWidgets.QLineEdit(self.layoutWidget)
        self.txt_estructura.setObjectName("txt_estructura")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txt_estructura)
        self.lbl_partida = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_partida.setObjectName("lbl_partida")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_partida)
        self.txt_partida = QtWidgets.QLineEdit(self.layoutWidget)
        self.txt_partida.setObjectName("txt_partida")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_partida)

        self.retranslateUi(form_facturero)
        self.btn_box.accepted.connect(form_facturero.accept) # type: ignore
        self.btn_box.rejected.connect(form_facturero.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(form_facturero)

    def retranslateUi(self, form_facturero):
        _translate = QtCore.QCoreApplication.translate
        form_facturero.setWindowTitle(_translate("form_facturero", "Agregar / Editar Facturero"))
        self.lbl_img.setText(_translate("form_facturero", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Imagen de Fondo</span></p></body></html>"))
        self.lbl_titulo.setText(_translate("form_facturero", "<html><head/><body><p align=\"center\"><span style=\" font-size:14pt;\">Agregar Facturero</span></p></body></html>"))
        self.lbl_nombre.setText(_translate("form_facturero", "Nombre"))
        self.lbl_estructura.setText(_translate("form_facturero", "Estructura"))
        self.lbl_partida.setText(_translate("form_facturero", "Partida"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form_facturero = QtWidgets.QDialog()
    ui = Ui_form_facturero()
    ui.setupUi(form_facturero)
    form_facturero.show()
    sys.exit(app.exec_())
