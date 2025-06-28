from PySide6.QtWidgets import QApplication, QVBoxLayout, QPushButton, QMainWindow, QHBoxLayout, QWidget, QLabel, QLineEdit
from PySide6.QtCore import QSize, QTimer, Qt, QUrl
from PySide6.QtMultimedia import QSoundEffect
import sys 

# Creamos la clase ventana
class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer type pomodoro")
        self.setGeometry(100, 100, 1000, 650)
        self.screen0()

        self.sonido0 = QSoundEffect()
        self.sonido0.setSource(QUrl.fromLocalFile("/home/idksa_script/Codigo/Proyectos/Pomodoro/usr/bin/Sounds/772763__jerryberumen__user-interface-fanfare-end-reached-success-victory-finished.wav"))
        self.sonido1 = QSoundEffect()
        self.sonido1.setSource(QUrl.fromLocalFile("/home/idksa_script/Codigo/Proyectos/Pomodoro/usr/bin/Sounds/613876__theplax__digital-alarm-clock.wav"))
        self.sonido0.setVolume(1.0)
        self.sonido1.setVolume(1.0)

    ###########################################
    ############### PANTALLAS #################

    # Pantalla 1: donde se ingresa el tiempo y se inicia el temporizador
    def screen0(self):
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        contenedor.setStyleSheet("background-color: #0e0f11") 
        principalLayout = QVBoxLayout(contenedor)
        self.setLayout(principalLayout)

        # Creamos un QHBoxLayout para ingresar los datos
        self.ingresaQline = QHBoxLayout()

        # QLineEdit para ingresar el tiempo de trabajo
        self.ingresar1 = QLineEdit()
        self.ingresar1.setPlaceholderText("Tiempo de trabajo: 00:00")
        self.ingresar1.setStyleSheet("color: white;")
        # QLineEdit para ingresar el descanso
        self.ingresar2 = QLineEdit()
        self.ingresar2.setPlaceholderText("Descanso (00:00)")
        self.ingresar2.setStyleSheet("color: white;")
        # QLineEdit para ingresar la cantidad de repeticiones
        self.ingresar3 = QLineEdit()
        self.ingresar3.setPlaceholderText("Veces a repetir (4)")
        self.ingresar3.setStyleSheet("color: white;")

        # Agregamos los QLineEdit al layout
        for ingresar in (self.ingresar1, self.ingresar2, self.ingresar3):
            self.ingresaQline.addWidget(ingresar)

        principalLayout.addLayout(self.ingresaQline)

        # Botón para iniciar el temporizador
        self.boton0 = QPushButton("Iniciar")
        self.boton0.clicked.connect(self.screen1)
        self.boton0.clicked.connect(self.iniciar)
        principalLayout.addWidget(self.boton0)

        # Inicializamos el temporizador QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.Encender)

    # Pantalla 2: la que sale cuando el temporizador está corriendo
    def screen1(self):
        contenedor = QWidget()
        self.layout = QVBoxLayout(contenedor)
        self.setCentralWidget(contenedor)
        contenedor.setStyleSheet("background-color: #0e0f11")
        self.setLayout(self.layout)

        # Label para mostrar el tiempo
        self.label0 = QLabel("00:00")
        self.label0.setStyleSheet("color:white;")
        self.layout.addWidget(self.label0)

        # Layout para los botones de control
        self.botonLayout = QHBoxLayout()
        # Botón para detener el temporizador
        self.boton1 = QPushButton("Detener")
        self.boton1.clicked.connect(self.Detener)
        # Botón para volver a la pantalla 1
        self.boton2 = QPushButton("Volver")
        self.boton2.clicked.connect(self.screen0)

        # Agregamos los botones al layout
        for boton in (self.boton1, self.boton2):
            boton.setStyleSheet("color: white;")
            self.botonLayout.addWidget(boton)

        self.layout.addLayout(self.botonLayout)

    ##########################################
    ############### PARTE LOGICA #############
  
    # Inicia el temporizador y guarda los valores ingresados
    def iniciar(self):
        # Guardamos los valores ingresados antes de cambiar de pantalla
        self.estadoTrabajo = self.ingresar1.text()
        self.estadoDescanso = self.ingresar2.text()
        try:
            self.repeticiones = int(self.ingresar3.text())
        except ValueError:
            self.repeticiones = 1  # Valor por defecto si no es válido

        self.estado = "Trabajo"  # Comenzamos en modo trabajo
        self.repeticionesCO = 0  # Contador de ciclos completados

        # Convertimos el tiempo de trabajo a segundos
        minutos, segundos = map(int, self.estadoTrabajo.split(":"))
        self.segundos = minutos * 60 + segundos
        self.label0.setText(f"{minutos:02}:{segundos:02}")

        if not self.timer.isActive():
            self.timer.start(1000)

    # Esta función se llama cada segundo por el QTimer
    def Encender(self):
        if self.segundos > 0:
            # Si quedan segundos, restamos uno y actualizamos el label
            self.segundos -= 1
            minutes = self.segundos // 60
            seconds = self.segundos % 60
            self.label0.setText(f"{minutes:02}:{seconds:02}")
        else:
            # Cuando el temporizador llega a 0
            if self.estado == "Trabajo":
                self.sonidoInicioDescanso()  # Reproducimos el sonido
                # Cambiamos a descanso
                self.estado = "Descanso"
                try:
                    minutos, segundos = map(int, self.estadoDescanso.split(":"))
                except Exception:
                    minutos, segundos = 0, 0
                self.segundos = minutos * 60 + segundos
                self.label0.setText(f"{minutos:02}:{segundos:02}")
            elif self.estado == "Descanso":
                # Terminó un ciclo completo (trabajo + descanso)
                self.repeticionesCO += 1
                if self.repeticionesCO >= self.repeticiones:
                    # Si ya se completaron las repeticiones, detenemos el timer y volvemos a la pantalla inicial
                    self.sonidoFinal()
                    self.timer.stop()
                    self.screen0()
                    return
                # Si no, volvemos a trabajo
                self.estado = "Trabajo"
                self.sonidoInicioDescanso()
                try:
                    minutos, segundos = map(int, self.estadoTrabajo.split(":"))
                except Exception:
                    minutos, segundos = 0, 0
                self.segundos = minutos * 60 + segundos
                self.label0.setText(f"{minutos:02}:{segundos:02}")
    
    # Detiene o reanuda el temporizador
    def Detener(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(1000)

    def sonidoInicioDescanso(self):
        self.sonido0.play()
     
    def sonidoFinal(self):
        self.sonido1.play()

app = QApplication(sys.argv)
windows = mainWindow()
windows.show()
app.exec()