from PySide2 import QtCore
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QApplication, QDialog, QWidget
import sys
from functools import partial
from PySide2.QtMultimediaWidgets import QVideoWidget
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtCore import QUrl
from filemanager import readFromCSV, writeValuesToCSV, writeResultsToCSV
from schmidt import schmidtAnalysis, plotSchmidtAnalysis
import sys


class Intro(QDialog):
    def __init__(self, parent=None):
        super(Intro, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Stirling engine calculator")
        
        # Create widgets
        self.greeting = QLabel("Welcome to the stirling engine calculator!")
        self.greeting.setAlignment(QtCore.Qt.AlignCenter)
        self.greeting.setFixedSize(600, 50)
        self.greeting.setObjectName("greeting")
        self.prompt = QLabel("Please press the 'Manual input'-button to enter the input-values.")
        self.prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt.setFixedSize(600, 100)
        self.prompt.setObjectName("prompt")
        self.inputButton = QPushButton("Manual input")
        self.inputButton.setFixedSize(100, 50)
        self.inputButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.greeting, 0, 0, 1, 5)
        layout.addWidget(self.prompt, 1, 0, 1, 5)
        layout.addWidget(self.inputButton, 2, 2, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect button 
        self.inputButton.clicked.connect(self.manualInput)

    # Method for navigation

    def manualInput(self):
        self.manualInput = ManualInput(self)
        self.manualInput.show()
        
        if self.isVisible():
            self.hide()


class ManualInput(QDialog):
    def __init__(self, parent=None):
        super(ManualInput, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Manual input")
        
        # Create widgets
        self.prompt = QLabel("Please enter the values below.")
        self.prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt.setFixedSize(600, 100)
        self.prompt.setObjectName("prompt")
        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(100, 50)
        self.returnButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.continueButton = QPushButton("Continue")
        self.continueButton.setFixedSize(100, 50)
        self.continueButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create form
        self.volume = QLabel("Volume [mm^3]")
        self.volume.setAlignment(QtCore.Qt.AlignCenter)
        self.volume.setFixedSize(600, 50)
        self.v_cyl_prompt = QLabel("Cylinder:")
        self.v_cyl_prompt.setFixedSize(100, 30)
        self.v_cyl = QLineEdit()
        self.v_cyl.setFixedSize(100, 30)
        self.v_reg_prompt = QLabel("Regenerator:")
        self.v_reg_prompt.setFixedSize(100, 30)
        self.v_reg = QLineEdit()
        self.v_reg.setFixedSize(100, 30)
        self.v_c_avg_prompt = QLabel("Cylinder average:")
        self.v_c_avg_prompt.setFixedSize(100, 30)
        self.v_c_avg = QLineEdit()
        self.v_c_avg.setFixedSize(100, 30)

        self.area = QLabel("Area [mm^2]")
        self.area.setAlignment(QtCore.Qt.AlignCenter)
        self.area.setFixedSize(600, 50)
        self.piston_rod_area_prompt = QLabel("Piston rod surface:")
        self.piston_rod_area_prompt.setFixedSize(100, 30)
        self.piston_rod_area = QLineEdit()
        self.piston_rod_area.setFixedSize(100, 30)
        self.piston_cyl_area_prompt = QLabel("Piston cylinder:")
        self.piston_cyl_area_prompt.setFixedSize(100, 30)
        self.piston_cyl_area = QLineEdit()
        self.piston_cyl_area.setFixedSize(100, 30)
        
        self.temperature = QLabel("Temperature [C]")
        self.temperature.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature.setFixedSize(600, 50)
        self.th_prompt = QLabel("Hot side:")
        self.th_prompt.setFixedSize(100, 30)
        self.th = QLineEdit()
        self.th.setFixedSize(100, 30)
        self.tr_prompt = QLabel("Regenerator:")
        self.tr_prompt.setFixedSize(100, 30)
        self.tr = QLineEdit()
        self.tr.setFixedSize(100, 30)
        self.tc_prompt = QLabel("Cold side:")
        self.tc_prompt.setFixedSize(100, 30)
        self.tc = QLineEdit()
        self.tc.setFixedSize(100, 30)
        
        self.additional = QLabel("Additional values")
        self.additional.setAlignment(QtCore.Qt.AlignCenter)
        self.additional.setFixedSize(600, 50)
        self.beta_prompt = QLabel("Phase-angle beta:")
        self.beta_prompt.setFixedSize(100, 30)
        self.beta = QLineEdit()
        self.beta.setFixedSize(100, 30)
        self.m_prompt = QLabel("Mass:")
        self.m_prompt.setFixedSize(100, 30)
        self.m = QLineEdit()
        self.m.setFixedSize(100, 30)
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.prompt, 0, 0, 1, 5)
        
        layout.addWidget(self.volume, 1, 0, 1, 5)
        layout.addWidget(self.v_cyl_prompt, 2, 1, 1, 1)
        layout.addWidget(self.v_cyl, 2, 3, 1, 1)
        layout.addWidget(self.v_reg_prompt, 3, 1, 1, 1)
        layout.addWidget(self.v_reg, 3, 3, 1, 1)
        layout.addWidget(self.v_c_avg_prompt, 4, 1, 1, 1)
        layout.addWidget(self.v_c_avg, 4, 3, 1, 1)
        
        layout.addWidget(self.temperature, 5, 0, 1, 5)
        layout.addWidget(self.th_prompt, 6, 1, 1, 1)
        layout.addWidget(self.th, 6, 3, 1, 1)
        layout.addWidget(self.tr_prompt, 7, 1, 1, 1)
        layout.addWidget(self.tr, 7, 3, 1, 1)
        layout.addWidget(self.tc_prompt, 8, 1, 1, 1)
        layout.addWidget(self.tc, 8, 3, 1, 1)

        layout.addWidget(self.area, 9, 0, 1, 5)
        layout.addWidget(self.piston_rod_area_prompt, 10, 1, 1, 1)
        layout.addWidget(self.piston_rod_area, 10, 3, 1, 1)
        layout.addWidget(self.piston_cyl_area_prompt, 11, 1, 1, 1)
        layout.addWidget(self.piston_cyl_area, 11, 3, 1, 1)
        
        layout.addWidget(self.additional, 12, 0, 1, 5)
        layout.addWidget(self.m_prompt, 13, 1, 1, 1)
        layout.addWidget(self.m, 13, 3, 1, 1)
        layout.addWidget(self.beta_prompt, 14, 1, 1, 1)
        layout.addWidget(self.beta, 14, 3, 1, 1)
        
        layout.addWidget(QLabel(""), 15, 1, 1, 5)
        
        layout.addWidget(self.returnButton, 16, 1, 1, 1)
        layout.addWidget(self.continueButton, 16, 3, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect buttons
        self.returnButton.clicked.connect(self.returnToIntro)
        self.continueButton.clicked.connect(self.continueToCalculation)
        
    def returnToIntro(self):
        self.intro = Intro(self)
        self.intro.show()
        self.hide()
        
    def continueToCalculation(self):
        valueList = [self.m, self.th, self.tr, self.tc, self.v_cyl, self.v_reg, self.v_c_avg, self.piston_rod_area, self.piston_cyl_area, self.beta]
        values = []

        for item in valueList:
            values.append(item.text())

        isApproved = self.checkValues(values)

        if (isApproved):
            writeValuesToCSV("inputValues", values)
            self.stateVisualization = StateWindow(self)
            self.stateVisualization.show()
            self.hide()
        else:
            self.manualInput = ManualInput(self)
            self.manualInput.show()
            self.hide()
        
    def checkValues(self, values):
        for value in values:
            if (value is not None and value != ''):
                try:    
                    fValue = float(value)
                    if (fValue < 0):
                        return False
                except:
                    return False
            else:
                return False

        return True


class StateWindow(QDialog):
    number = 1

    Position1Text = "The transfer medium is displaced to the bottom of the cylinder. Here, it is exposed to a higher temperature, which results in an increase in pressure."
    Position2Text = "The continuous motion of the flywheel results in the piston being moved to its lowest position. The pressure is still increasing, but the displacer is moving upwards in the cylinder."
    Position3Text = "The increase in pressure is moving the piston upwards, and has moved the displacer to the top of the cylinder. This relative increase in volume results in a decrease in pressure."
    Position4Text = "The piston is at its maximal height due to the continuous motion of the flywheel and the internal pressure of the cylinder. The displacer is moving downwards in the cylinder."
    
    def __init__(self, parent=None):
        super(StateWindow, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Stirling engine state visualization")
        
        # Create widgets
        self.prompt = QLabel("Steps in a stirling engine.")
        self.prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt.setFixedSize(300, 100)
        self.prompt.setObjectName("prompt")
        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(100, 50)
        self.returnButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.continueButton = QPushButton("Continue")
        self.continueButton.setFixedSize(100, 50)
        self.continueButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.displayButton = QPushButton("Display animation")
        self.displayButton.setFixedSize(300, 50)
        self.displayButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.textDescription = QLabel(self.addPositionText(StateWindow.number))
        self.textDescription.setFixedSize(300, 200)
        self.textDescription.setWordWrap(True)
        
        # Create navigation-buttons
        self.nav1Button = QPushButton("1")
        self.nav1Button.setFixedSize(30, 30)
        self.nav1Button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nav2Button = QPushButton("2")
        self.nav2Button.setFixedSize(30, 30)
        self.nav2Button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nav3Button = QPushButton("3")
        self.nav3Button.setFixedSize(30, 30)
        self.nav3Button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.nav4Button = QPushButton("4")
        self.nav4Button.setFixedSize(30, 30)
        self.nav4Button.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create pixmap
        self.image = QLabel(self)
        pixmap = QPixmap("assets/Position" + str(StateWindow.number) + ".png")
        pixmap = pixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(pixmap)
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.image, 0, 0, 4, 6)
        
        layout.addWidget(self.nav1Button, 5, 1, 1, 1)
        layout.addWidget(self.nav2Button, 5, 2, 1, 1)
        layout.addWidget(self.nav3Button, 5, 3, 1, 1)
        layout.addWidget(self.nav4Button, 5, 4, 1, 1)
        
        layout.addWidget(self.prompt, 0, 7, 1, 5)
        layout.addWidget(self.displayButton, 1, 8, 1, 3)
        layout.addWidget(self.textDescription, 2, 8, 3, 3)
        layout.addWidget(self.returnButton, 5, 8, 1, 1)
        layout.addWidget(self.continueButton, 5, 10, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect buttons
        self.nav1Button.clicked.connect(partial(self.navigateToImage, 1))
        self.nav2Button.clicked.connect(partial(self.navigateToImage, 3))
        self.nav3Button.clicked.connect(partial(self.navigateToImage, 5))
        self.nav4Button.clicked.connect(partial(self.navigateToImage, 7))
        self.displayButton.clicked.connect(self.displayAnimation)
        self.returnButton.clicked.connect(self.returnToIntro)
        self.continueButton.clicked.connect(self.continueToResults)
        
    def returnToIntro(self):
        self.intro = Intro(self)
        self.intro.show()
        self.hide()
    
    def displayAnimation(self):
        self.animation = AnimationWindow(self)
        self.animation.show()
        self.hide()
        
    def navigateToImage(self, num):
        StateWindow.number = num
        self.displayImage = StateWindow(self)
        self.displayImage.show()
        self.hide()
        
    def continueToResults(self):
        self.results = ResultWindow(self)
        self.results.show()
        self.hide()
        
    def addPositionText(self, number):
        switcher = {
            1: StateWindow.Position1Text,
            3: StateWindow.Position2Text,
            5: StateWindow.Position3Text,
            7: StateWindow.Position4Text
        }
        return switcher.get(number, "Invalid position.")


class AnimationWindow(QDialog):
    def __init__(self, parent=None):
        super(AnimationWindow, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Stirling engine animation")
        
        # Create widgets
        self.prompt = QLabel("Steps in a Stirling cycle.")
        self.prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt.setFixedSize(300, 100)
        self.prompt.setObjectName("prompt")
        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(100, 50)
        self.returnButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.continueButton = QPushButton("Continue")
        self.continueButton.setFixedSize(100, 50)
        self.continueButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.displayButton = QPushButton("Display state visualization")
        self.displayButton.setFixedSize(300, 50)
        self.displayButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.textDescription = QLabel("This is an animation of a complete thermodynamic cycle in a simplified Stirling engine. Each step can be reviewed individually by pressing 'Display state visualization'.")
        self.textDescription.setFixedSize(300, 200)
        self.textDescription.setWordWrap(True)
        
        # Create navigation-buttons
        self.playButton = QPushButton("Play")
        self.playButton.setFixedSize(100, 50)
        self.playButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pauseButton = QPushButton("Pause")
        self.pauseButton.setFixedSize(100, 50)
        self.pauseButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create video widget
        self.mediaPlayer = QMediaPlayer()
        self.video = QVideoWidget()
        self.video.setFixedSize(854, 480)
        self.mediaPlayer.setVideoOutput(self.video)
        self.mediaPlayer.setSource(QUrl("assets/stirling_animation.mp4"))
        self.video.show()
        self.mediaPlayer.setLoops(100)
        #self.mediaPlayer.play()
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.video, 0, 0, 4, 8)
        
        layout.addWidget(self.playButton, 5, 2, 2, 1)
        layout.addWidget(self.pauseButton, 5, 5, 2, 1)
        
        layout.addWidget(self.prompt, 0, 9, 1, 5)
        layout.addWidget(self.displayButton, 1, 10, 1, 3)
        layout.addWidget(self.textDescription, 2, 10, 3, 3)
        layout.addWidget(self.returnButton, 5, 10, 1, 1)
        layout.addWidget(self.continueButton, 5, 12, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect buttons
        self.playButton.clicked.connect(self.playVideo)
        self.pauseButton.clicked.connect(self.pauseVideo)
        self.displayButton.clicked.connect(self.displayStateVisualization)
        self.returnButton.clicked.connect(self.returnToManualInput)
        self.continueButton.clicked.connect(self.continueToResults)
        
    def returnToManualInput(self):
        self.manualInput = ManualInput(self)
        self.manualInput.show()
        self.hide()
    
    def displayStateVisualization(self):
        self.stateVisualization = StateWindow(self)
        self.stateVisualization.show()
        self.hide()
        
    def playVideo(self):
        self.mediaPlayer.play()
        
    def pauseVideo(self):
        self.mediaPlayer.pause()
        
    def continueToResults(self):
        self.results = ResultWindow(self)
        self.results.show()
        self.hide()


class ResultWindow(QDialog):
    def __init__(self, parent=None):
        super(ResultWindow, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Results of analysis")
        
        # Create widgets
        self.complete_message = QLabel("The analysis is complete.")
        self.complete_message.setAlignment(QtCore.Qt.AlignCenter)
        self.complete_message.setFixedSize(500, 100)
        self.complete_message.setObjectName("complete_message")

        self.schmidtAnalysisFilename = "schmidtanalysis"
        self.schmidtResultsFilename = "schmidtanalysis"

        self.result_message = QLabel("The plots are stored under 'results/" + self.schmidtAnalysisFilename + ".pdf'.")
        self.result_message.setAlignment(QtCore.Qt.AlignCenter)
        self.result_message.setFixedSize(500, 100)
        self.result_message.setObjectName("result_message")

        self.csv_message = QLabel("The results are stored under 'results/" + self.schmidtResultsFilename + ".csv'.")
        self.csv_message.setAlignment(QtCore.Qt.AlignCenter)
        self.csv_message.setFixedSize(500, 100)
        self.csv_message.setObjectName("result_message")

        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(100, 50)
        self.returnButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.exitButton = QPushButton("Exit application")
        self.exitButton.setFixedSize(100, 50)
        self.exitButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create layout and add widgets
        layout = QGridLayout(window)

        # Calculate results
        calculationValues = readFromCSV("assets/inputValues.csv")
        print("These values were read from the CSV-file containing input-values:")
        print(calculationValues)
        cycleAnalysis = schmidtAnalysis(calculationValues)

        # Plot results
        plotSchmidtAnalysis(self.schmidtAnalysisFilename, cycleAnalysis)

        # Save results
        writeResultsToCSV(self.schmidtResultsFilename, cycleAnalysis)
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.complete_message, 0, 0, 2, 5)
        
        layout.addWidget(self.result_message, 2, 0, 1, 5)
        layout.addWidget(self.csv_message, 3, 0, 1, 5)
        
        layout.addWidget(self.returnButton, 4, 1, 1, 1)
        layout.addWidget(self.exitButton, 4, 3, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect buttons
        self.returnButton.clicked.connect(self.returnToStateVisualization)
        self.exitButton.clicked.connect(self.exitApplication)
        
    
    def returnToStateVisualization(self):
        self.stateVisualization = StateWindow(self)
        self.stateVisualization.show()
        self.hide()
        
    def exitApplication(self):
        sys.exit()


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    
    # Create and show the window
    main = Intro()
    main.show()
    
    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)
        
    # Run the main Qt loop
    sys.exit(app.exec_())