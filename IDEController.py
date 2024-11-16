# Form implementation generated from reading ui file 'IDEview.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(986, 639)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet("\n"
"\n"
"QMainWindow {\n"
"    background-color: #1E1E2E;\n"
"    color: #FFFFFF;\n"
"    font-family: \"Roboto\", sans-serif;\n"
"    transition: background-color 0.3s ease, color 0.3s ease;\n"
"}\n"
"\n"
"QMenuBar {\n"
"    background-color: #252537;\n"
"    color: #FFFFFF;\n"
"    border-bottom: 2px solid #3A3A4F;\n"
"    font-family: \"Helvetica Neue\", sans-serif;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    transition: background-color 0.3s ease;\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    background-color: transparent;\n"
"    color: #FFFFFF;\n"
"    padding: 8px 12px;\n"
"    border-radius: 4px;\n"
"    transition: background-color 0.3s ease;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #3A3A4F;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QMenu {\n"
"    background-color: #2D2D3E;\n"
"    color: #FFFFFF;\n"
"    border: 1px solid #3A3A4F;\n"
"    padding: 6px;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QMenu::item {\n"
"    background-color: transparent;\n"
"    padding: 8px 12px;\n"
"    border-radius: 4px;\n"
"    transition: background-color 0.3s ease;\n"
"}\n"
"\n"
"QMenu::item:selected {\n"
"    background-color: #505068;\n"
"    color: #E5E5E5;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #E5E5E5;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"    margin-bottom: 10px;\n"
"    transition: color 0.3s ease;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #505068;\n"
"    color: #E5E5E5;\n"
"    border: 1px solid #3A3A4F;\n"
"    border-radius: 8px;\n"
"    padding: 10px 20px;\n"
"    font-family: \"Helvetica Neue\", sans-serif;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    transition: background-color 0.3s ease, transform 0.2s ease;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #636382;\n"
"    border-color: #505068;\n"
"    transform: scale(1.05);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #3A3A4F;\n"
"    transform: scale(0.98);\n"
"}\n"
"\n"
"QTextEdit {\n"
"    background-color: #2D2D3E;\n"
"    color: #E5E5E5;\n"
"    border: 1px solid #3A3A4F;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    font-family: \"Courier New\", monospace;\n"
"    font-size: 14px;\n"
"    transition: border-color 0.3s ease, box-shadow 0.3s ease;\n"
"}\n"
"\n"
"QTextEdit:focus {\n"
"    border-color: #505068;\n"
"    box-shadow: 0 0 10px rgba(80, 80, 80, 0.5);\n"
"}\n"
"\n"
"QStatusBar {\n"
"    background-color: #1E1E2E;\n"
"    color: #FFFFFF;\n"
"    border-top: 1px solid #3A3A4F;\n"
"    font-size: 12px;\n"
"    font-family: \"Roboto\", sans-serif;\n"
"}\n"
"\n"
"QVBoxLayout, QHBoxLayout {\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QWidget {\n"
"    transition: background-color 0.3s ease, color 0.3s ease;\n"
"}\n"
"\n"
"QFrame, QWidget {\n"
"    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"QPushButton:hover, QMenuBar::item:hover, QMenu::item:hover {\n"
"    background-color: #636382;\n"
"    border-color: #505068;\n"
"    cursor: pointer;\n"
"}\n"
"\n"
"QMenuBar {\n"
"    transition: background-color 0.3s ease;\n"
"}\n"
"\n"
"QMenuBar::item:selected {\n"
"    background-color: #505068;\n"
"}\n"
"\n"
"QMessageBox {\n"
"    background-color: #2D2D3E; /* Fondo oscuro similar a los otros componentes */\n"
"    color: #E5E5E5; /* Color blanco para el texto */\n"
"    font-family: \"Roboto\", sans-serif;\n"
"    font-size: 14px;\n"
"    border-radius: 8px;\n"
"    padding: 20px;\n"
"    min-width: 300px; /* Ancho mínimo para mejorar la visibilidad */\n"
"    box-shadow: 0 0 15px rgba(0, 0, 0, 0.2); /* Sombra para darle profundidad */\n"
"}\n"
"\n"
"QMessageBox QLabel {\n"
"    color: #E5E5E5; /* Color claro para el texto */\n"
"    font-size: 16px; /* Asegura que el texto sea legible */\n"
"    font-weight: normal;\n"
"    margin-bottom: 10px;\n"
"}\n"
"\n"
"QMessageBox QPushButton {\n"
"    background-color: #505068;\n"
"    color: #E5E5E5;\n"
"    border: 1px solid #3A3A4F;\n"
"    border-radius: 8px;\n"
"    padding: 8px 15px;\n"
"    font-family: \"Helvetica Neue\", sans-serif;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    transition: background-color 0.3s ease, transform 0.2s ease;\n"
"}\n"
"\n"
"QMessageBox QPushButton:hover {\n"
"    background-color: #636382;\n"
"    border-color: #505068;\n"
"    transform: scale(1.05);\n"
"}\n"
"\n"
"QMessageBox QPushButton:pressed {\n"
"    background-color: #3A3A4F;\n"
"    transform: scale(0.98);\n"
"}\n"
"\n"
"QMessageBox QPushButton#ok {\n"
"    background-color: #505068;\n"
"    color: #E5E5E5;\n"
"}\n"
"\n"
"QMessageBox QPushButton#ok:hover {\n"
"    background-color: #636382;\n"
"    border-color: #505068;\n"
"}\n"
"\n"
"QMessageBox QLabel[icon] {\n"
"    margin-right: 10px;\n"
"    padding-left: 10px;\n"
"}\n"
"\n"
"   ")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 511, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.Txt_Codigo = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.Txt_Codigo.setObjectName("Txt_Codigo")
        self.verticalLayout.addWidget(self.Txt_Codigo)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(600, 10, 361, 421))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setToolTipDuration(-2)
        self.label_2.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.TxtSalida = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget_2)
        self.TxtSalida.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.TxtSalida.setMouseTracking(False)
        self.TxtSalida.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.TxtSalida.setObjectName("TxtSalida")
        self.verticalLayout_2.addWidget(self.TxtSalida)
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(670, 460, 261, 111))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Btn_Compilar = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.Btn_Compilar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        self.Btn_Compilar.setObjectName("Btn_Compilar")
        self.horizontalLayout.addWidget(self.Btn_Compilar)
        self.Btn_Ejecutar = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.Btn_Ejecutar.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.OpenHandCursor))
        self.Btn_Ejecutar.setObjectName("Btn_Ejecutar")
        self.horizontalLayout.addWidget(self.Btn_Ejecutar)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(30, 450, 511, 131))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_consola = QtWidgets.QLabel(parent=self.verticalLayoutWidget_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_consola.setFont(font)
        self.label_consola.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_consola.setObjectName("label_consola")
        self.verticalLayout_3.addWidget(self.label_consola)
        self.Txt_Consola = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget_3)
        self.Txt_Consola.setObjectName("Txt_Consola")
        self.verticalLayout_3.addWidget(self.Txt_Consola)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 986, 22))
        self.menubar.setObjectName("menubar")
        self.menuNuevo = QtWidgets.QMenu(parent=self.menubar)
        self.menuNuevo.setObjectName("menuNuevo")
        self.menuOpciones = QtWidgets.QMenu(parent=self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        self.menuEjemplos = QtWidgets.QMenu(parent=self.menubar)
        self.menuEjemplos.setObjectName("menuEjemplos")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAbrir = QtGui.QAction(parent=MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionNuevo = QtGui.QAction(parent=MainWindow)
        self.actionNuevo.setObjectName("actionNuevo")
        self.actionGuardar = QtGui.QAction(parent=MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_como = QtGui.QAction(parent=MainWindow)
        self.actionGuardar_como.setObjectName("actionGuardar_como")
        self.AFFuncion = QtGui.QAction(parent=MainWindow)
        self.AFFuncion.setObjectName("AFFuncion")
        self.AFProcedimiento = QtGui.QAction(parent=MainWindow)
        self.AFProcedimiento.setObjectName("AFProcedimiento")
        self.AFCondicionales = QtGui.QAction(parent=MainWindow)
        self.AFCondicionales.setObjectName("AFCondicionales")
        self.AFCondicionalesAnidados = QtGui.QAction(parent=MainWindow)
        self.AFCondicionalesAnidados.setObjectName("AFCondicionalesAnidados")
        self.AFCicloWhile = QtGui.QAction(parent=MainWindow)
        self.AFCicloWhile.setObjectName("AFCicloWhile")
        self.AFCicloFor = QtGui.QAction(parent=MainWindow)
        self.AFCicloFor.setObjectName("AFCicloFor")
        self.AFInsertComentario = QtGui.QAction(parent=MainWindow)
        self.AFInsertComentario.setObjectName("AFInsertComentario")
        self.AFInsertWhile = QtGui.QAction(parent=MainWindow)
        self.AFInsertWhile.setObjectName("AFInsertWhile")
        self.AFInsertFor = QtGui.QAction(parent=MainWindow)
        self.AFInsertFor.setObjectName("AFInsertFor")
        self.AFInsertMain = QtGui.QAction(parent=MainWindow)
        self.AFInsertMain.setObjectName("AFInsertMain")
        self.AFInsertFunction = QtGui.QAction(parent=MainWindow)
        self.AFInsertFunction.setObjectName("AFInsertFunction")
        self.AFInsertProcedure = QtGui.QAction(parent=MainWindow)
        self.AFInsertProcedure.setObjectName("AFInsertProcedure")
        self.AFSwitch = QtGui.QAction(parent=MainWindow)
        self.AFSwitch.setObjectName("AFSwitch")
        self.AFInsertInput = QtGui.QAction(parent=MainWindow)
        self.AFInsertInput.setObjectName("AFInsertInput")
        self.AFInsertOutput = QtGui.QAction(parent=MainWindow)
        self.AFInsertOutput.setObjectName("AFInsertOutput")
        self.AFOpenDocs = QtGui.QAction(parent=MainWindow)
        self.AFOpenDocs.setObjectName("AFOpenDocs")
        self.AFInsertVar = QtGui.QAction(parent=MainWindow)
        self.AFInsertVar.setObjectName("AFInsertVar")
        self.AFInsertPila = QtGui.QAction(parent=MainWindow)
        self.AFInsertPila.setObjectName("AFInsertPila")
        self.AFInsertLista = QtGui.QAction(parent=MainWindow)
        self.AFInsertLista.setObjectName("AFInsertLista")
        self.AFInsertSwitch = QtGui.QAction(parent=MainWindow)
        self.AFInsertSwitch.setObjectName("AFInsertSwitch")
        self.menuNuevo.addAction(self.actionAbrir)
        self.menuNuevo.addSeparator()
        self.menuNuevo.addAction(self.actionNuevo)
        self.menuNuevo.addSeparator()
        self.menuNuevo.addAction(self.actionGuardar)
        self.menuNuevo.addSeparator()
        self.menuNuevo.addAction(self.actionGuardar_como)
        self.menuNuevo.addSeparator()
        self.menuOpciones.addAction(self.AFInsertComentario)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertInput)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertWhile)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertFor)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertMain)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertFunction)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertProcedure)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertSwitch)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertOutput)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertVar)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertPila)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFInsertLista)
        self.menuOpciones.addSeparator()
        self.menuOpciones.addAction(self.AFOpenDocs)
        self.menuOpciones.addSeparator()
        self.menuEjemplos.addSeparator()
        self.menuEjemplos.addAction(self.AFFuncion)
        self.menuEjemplos.addSeparator()
        self.menuEjemplos.addAction(self.AFProcedimiento)
        self.menuEjemplos.addSeparator()
        self.menuEjemplos.addAction(self.AFCondicionales)
        self.menuEjemplos.addSeparator()
        self.menuEjemplos.addAction(self.AFCondicionalesAnidados)
        self.menuEjemplos.addSeparator()
        self.menuEjemplos.addAction(self.AFCicloWhile)
        self.menuEjemplos.addSeparator()
        self.menuEjemplos.addAction(self.AFCicloFor)
        self.menuEjemplos.addSeparator()
        self.menuEjemplos.addAction(self.AFSwitch)
        self.menuEjemplos.addSeparator()
        self.menubar.addAction(self.menuNuevo.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuEjemplos.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JÄGER-SCRIPT IDE"))
        self.label.setText(_translate("MainWindow", "Código:"))
        self.label_2.setText(_translate("MainWindow", "Salida:"))
        self.Btn_Compilar.setText(_translate("MainWindow", "Compilar"))
        self.Btn_Ejecutar.setText(_translate("MainWindow", "Ejecutar"))
        self.label_consola.setText(_translate("MainWindow", "Consola"))
        self.menuNuevo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuOpciones.setTitle(_translate("MainWindow", "Funcionalidades"))
        self.menuEjemplos.setTitle(_translate("MainWindow", "Ejemplos"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_como.setText(_translate("MainWindow", "Guardar como"))
        self.AFFuncion.setText(_translate("MainWindow", "Funcion"))
        self.AFProcedimiento.setText(_translate("MainWindow", "Procedimiento"))
        self.AFCondicionales.setText(_translate("MainWindow", "Condicionales"))
        self.AFCondicionalesAnidados.setText(_translate("MainWindow", "Condicionales anidados"))
        self.AFCicloWhile.setText(_translate("MainWindow", "Ciclo while"))
        self.AFCicloFor.setText(_translate("MainWindow", "Ciclo for"))
        self.AFInsertComentario.setText(_translate("MainWindow", "Insertar comentario"))
        self.AFInsertWhile.setText(_translate("MainWindow", "Insertar esqueleto while"))
        self.AFInsertFor.setText(_translate("MainWindow", "Insertar esqueleto for"))
        self.AFInsertMain.setText(_translate("MainWindow", "Insertar esqueleto main"))
        self.AFInsertFunction.setText(_translate("MainWindow", "Insertar esqueleto function"))
        self.AFInsertProcedure.setText(_translate("MainWindow", "Insertar esqueleto procedure"))
        self.AFSwitch.setText(_translate("MainWindow", "Switch"))
        self.AFInsertInput.setText(_translate("MainWindow", "Insertar input"))
        self.AFInsertOutput.setText(_translate("MainWindow", "Insertar output"))
        self.AFOpenDocs.setText(_translate("MainWindow", "Abrir Documentación del proyecto"))
        self.AFInsertVar.setText(_translate("MainWindow", "Insertar var def"))
        self.AFInsertPila.setText(_translate("MainWindow", "Insert pila def"))
        self.AFInsertLista.setText(_translate("MainWindow", "Insertar lista def"))
        self.AFInsertSwitch.setText(_translate("MainWindow", "Insertar esqueleto switch"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
