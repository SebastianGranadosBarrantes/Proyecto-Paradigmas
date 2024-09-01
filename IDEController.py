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
        MainWindow.resize(978, 657)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        MainWindow.setFont(font)
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    background-color: rgb(75, 75, 75);\n"
"}\n"
"QMenuBar{\n"
"    \n"
"    background-color: rgb(156, 255, 26);\n"
"}\n"
"\n"
"QVBoxLayout{\n"
"background-color: rgb(156, 255, 26);\n"
"\n"
"}\n"
"\n"
"QLabel{\n"
"background-color: rgb(156, 255, 26);\n"
"}\n"
"\n"
"QMenu{\n"
"background-color: rgb(41, 178, 190);\n"
"}\n"
"\n"
"QPushButton{\n"
"background-color: rgb(41, 178, 190);\n"
"}")
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
        self.Txt_Codigo.setStyleSheet("background-color: rgb(255, 255, 255);")
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
        self.Txt_Salida = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget_2)
        self.Txt_Salida.setObjectName("Txt_Salida")
        self.verticalLayout_2.addWidget(self.Txt_Salida)
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(640, 440, 261, 111))
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 978, 21))
        self.menubar.setObjectName("menubar")
        self.menuNuevo = QtWidgets.QMenu(parent=self.menubar)
        self.menuNuevo.setObjectName("menuNuevo")
        self.menuOpciones = QtWidgets.QMenu(parent=self.menubar)
        self.menuOpciones.setObjectName("menuOpciones")
        self.menuSalir = QtWidgets.QMenu(parent=self.menubar)
        self.menuSalir.setObjectName("menuSalir")
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
        self.menuNuevo.addSeparator()
        self.menuNuevo.addAction(self.actionAbrir)
        self.menuNuevo.addAction(self.actionNuevo)
        self.menuNuevo.addAction(self.actionGuardar)
        self.menuNuevo.addAction(self.actionGuardar_como)
        self.menubar.addAction(self.menuNuevo.menuAction())
        self.menubar.addAction(self.menuOpciones.menuAction())
        self.menubar.addAction(self.menuSalir.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "JÄGER-SCRIPT IDE"))
        self.label.setText(_translate("MainWindow", "Código:"))
        self.label_2.setText(_translate("MainWindow", "Salida:"))
        self.Btn_Compilar.setText(_translate("MainWindow", "Compilar"))
        self.Btn_Ejecutar.setText(_translate("MainWindow", "Ejecutar"))
        self.menuNuevo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuOpciones.setTitle(_translate("MainWindow", "Opciones"))
        self.menuSalir.setTitle(_translate("MainWindow", "Salir"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionNuevo.setText(_translate("MainWindow", "Nuevo"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_como.setText(_translate("MainWindow", "Guardar como"))