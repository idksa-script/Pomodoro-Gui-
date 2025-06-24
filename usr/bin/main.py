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

    #Pantalla 1 la que sale al iniciar el programa
    #Pantalla donde se ingresa el tiempo y se inicia el temporizador
    def screen0(self):
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        contenedor.setStyleSheet("background-color: #0e0f11") 
        principalLayout = QVBoxLayout(contenedor)
        self.setLayout(principalLayout)

        #Creamos un QHBoxLayout para ingresar los datos
        self.ingresaQline = QHBoxLayout()

        #Agregamos un QlineEdit para ingresar el tiempo
        self.ingresar1 = QLineEdit()
        self.ingresar1.setPlaceholderText("Tiempo de trabajo: 00:00")
        self.ingresar1.setStyleSheet("color: white;")
        #Agregamos un QlineEdit para ingresar el descanso
        self.ingresar2 = QLineEdit()
        self.ingresar2.setPlaceholderText("Descanso (00:00)")
        self.ingresar2.setStyleSheet("color: white;")
        #Agregamos un QlineEdit para ingresar la cantidad de veces que se repetira el temporizador
        self.ingresar3 = QLineEdit()
        self.ingresar3.setPlaceholderText("Veces a repetir (4)")
        self.ingresar3.setStyleSheet("color: white;")

        #Agregamos con un for los QlineEdit al layout no tener tantas lineas de codigo
        for ingresar in (self.ingresar1, self.ingresar2, self.ingresar3):
            self.ingresaQline.addWidget(ingresar)

        principalLayout.addLayout(self.ingresaQline)

        #Agregamos un boton para iniciar el temporizador que llama a la segunda pantalla y tambien a la funcion iniciar
        self.boton0 = QPushButton("Iniciar")
        self.boton0.clicked.connect(self.screen1)
        self.boton0.clicked.connect(self.iniciar)
        principalLayout.addWidget(self.boton0)

        #inicializamos el temporizador QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.Encender)


    #Pantalla 2 la que sale cuando el temporizador llega a 0
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

        #agregamos dos botones uno para detener y otra para volver a la pantalla 1
        self.botonLayout = QHBoxLayout()
        #Boton para detener el temporizador
        self.boton1 = QPushButton("Detener")
        self.boton1.clicked.connect(self.Detener)

        #Boton para volver a la pantalla 1
        self.boton2 = QPushButton("Volver")
        self.boton2.clicked.connect(self.screen0)

        #for para agilizar agregar los botones al layout
        for boton in (self.boton1, self.boton2):
            boton.setStyleSheet("color: white;")
            self.botonLayout.addWidget(boton)

        self.layout.addLayout(self.botonLayout)

    ##########################################
    ###############PARTE LOGICA###############
  
    #Extremos el tiempo ingresado en el QlineEdit y lo convertimos a segundos
    def iniciar(self):
        valor = self.ingresar1.text()
        #Lo separamos en minutos y segundos
        minutos, segundos = map(int, valor.split(":"))
        #Convertimos los minutos a segundos y sumamos los segundos
        self.segundos = minutos * 60 + segundos
        self.label0.setText(f"{minutos:02}:{segundos:02}")
        if not self.timer.isActive():
            self.timer.start(1000)

    def Encender(self):
        #Verifica si segundos es mayor que 0
        #Si es asi, resta 1 segundo y actualiza el label
        if self.segundos > 0:
            self.segundos -= 1
            minutes = self.segundos // 60
            seconds = self.segundos % 60
            #Actualiza el label con el tiempo restante
            self.label0.setText(f"{minutes:02}:{seconds:02}")
        else:
            #Si segundo es 0, se detiene el temporizador y se muestra la pantalla 1
            self.timer.stop()
            self.screen0()

    def Detener(self):
        if self.timer.isActive():
           self.timer.stop()
        else:
            self.timer.start(1000)
     
app = QApplication(sys.argv)

windows = mainWindow()
windows.show()

app.exec()