from PySide6.QtWidgets import QApplication,QVBoxLayout, QPushButton, QMainWindow, QHBoxLayout, QWidget, QLabel, QLineEdit
from PySide6.QtCore import QSize, QTimer, Qt 
import sys 


#Creamos la clase ventana
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #El titulo y tamaño y coordenadas donde aparecera la ventana
        self.setWindowTitle("Timer type pomodoro")
        self.setGeometry(100, 100, 1000, 650)

        self.screen0()

        

    ###########################################
    ###############PANTALLAS###################

    def screen0(self):
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        contenedor.setStyleSheet("background-color: #0e0f11") 
        principalLayout = QVBoxLayout(contenedor)
        self.setLayout(principalLayout)

        #Agregamos un QlineEdit para ingresar el tiempo
        self.ingresar = QLineEdit()
        self.ingresar.setPlaceholderText("00:00")
        self.ingresar.setStyleSheet("color: white;")
        principalLayout.addWidget(self.ingresar)

        #Agregamos un boton para iniciar el temporizador
        self.boton1 = QPushButton("Iniciar")
        self.boton1.clicked.connect(self.screen1)
        self.boton1.clicked.connect(self.Encender)
        principalLayout.addWidget(self.boton1)

        #self.timer = QTimer()
        #self.timer.timeout.connect(self.Encender)
    
    def screen1(self):
        contenedor = QWidget()
        self.layout = QVBoxLayout(contenedor)
        self.setCentralWidget(contenedor)
        contenedor.setStyleSheet("background-color: #0e0f11")
        self.setLayout(self.layout)

        #agregamos un label
        self.label0 = QLabel("00:00")
        self.label0.setStyleSheet("color:white;")
        self.layout.addWidget(self.label0)



    ##########################################
    ###############PARTE LOGICA###############
  
    def iniciar(self):
        if not self.timer.isActive():
            self.timer.start(1000)

    def Encender(self):
        valor = self.ingresar.text()
        print(valor)

    def Detener(self):
        if self.timer.isActive():
           self.timer.stop()
     
app = QApplication(sys.argv)

windows = mainWindow()
windows.show()

app.exec()
