from PyQt5 import QtCore
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QPushButton, QApplication, QDialog, QWidget, QProgressBar, QSpinBox, QSlider
import sys
from PyQt5.QtCore import pyqtSignal, pyqtProperty, QPropertyAnimation, Qt
from PyQt5 import QtGui, QtOpenGL
from filemanager import readFromJSON, writeToJSON, writeResultsToCSV
from analysis import *
from animation import StirlingAnimation
import pyqtgraph as pg
import sys

def checkValues(values):
    """Checks the validity of the given values.

    Args:
        values (float): Values collected from manual input.

    Returns:
        Bool: Verdict of whether the values are valid.
    """
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

class Intro(QDialog):
    """Introductionary window to the program. Presents the user with the options of how to enter the input-data.

    Args:
        QDialog (PyQt5.QtWidgets.QDialog): Instance to initialize.
    """
    
    def __init__(self, parent=None):
        """Initialization-function for the 'Intro'-class.

        Args:
            parent (PyQt5.QtWidgets.QDialog, optional): Optional parent of the instance. Defaults to None.
        """
        super(Intro, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Stirling engine analysis-program")
        
        # Create widgets
        self.greeting = QLabel("STIRLING ENGINE ANALYSIS-PROGRAM")
        self.greeting.setAlignment(QtCore.Qt.AlignCenter)
        self.greeting.setFixedSize(750, 50)
        self.greeting.setObjectName("greeting")
        self.defaultOrCustomPrompt = QLabel("Please press the 'Default'-button for example values or the 'Custom'-button to use the custom JSON-file.")
        self.defaultOrCustomPrompt.setAlignment(QtCore.Qt.AlignCenter)
        self.defaultOrCustomPrompt.setFixedSize(750, 100)
        self.defaultOrCustomPrompt.setObjectName("prompt")
        self.orLabel = QLabel("or")
        self.orLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.orLabel.setFixedSize(150, 50)
        self.orLabel.setObjectName("prompt")
        self.manualInputPrompt = QLabel("Press the 'Manual input'-button to manually enter values for calculation.")
        self.manualInputPrompt.setAlignment(QtCore.Qt.AlignCenter)
        self.manualInputPrompt.setFixedSize(750, 100)
        self.manualInputPrompt.setObjectName("prompt")
        self.inputButton = QPushButton("Manual input")
        self.inputButton.setFixedSize(150, 50)
        self.inputButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.defaultButton = QPushButton("Default")
        self.defaultButton.setFixedSize(150, 50)
        self.defaultButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.customButton = QPushButton("Custom")
        self.customButton.setFixedSize(150, 50)
        self.customButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.greeting, 0, 0, 1, 5)
        layout.addWidget(self.defaultOrCustomPrompt, 1, 0, 1, 5)
        layout.addWidget(self.defaultButton, 2, 1, 1, 1)
        layout.addWidget(self.orLabel, 2, 2, 1, 1)
        layout.addWidget(self.customButton, 2, 3, 1, 1)
        layout.addWidget(self.manualInputPrompt, 3, 0, 1, 5)
        layout.addWidget(self.inputButton, 4, 2, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect button 
        self.defaultButton.clicked.connect(self.useDefaultValues)
        self.customButton.clicked.connect(self.useCustomValues)
        self.inputButton.clicked.connect(self.manualInput)

    #region Methods for navigation

    def manualInput(self):
        """Navigates the user to the 'Manual input'-window.
        """
        
        self.manualInput = ManualInput(self)
        self.manualInput.show()
        
        if self.isVisible():
            self.hide()
            
    def useDefaultValues(self):
        """Lets the user use default-values for analysis obtained from JSON-file.
        """
        
        values = readFromJSON("assets/default.json")
        
        #isApproved = checkValues(values)

        if (True):
            writeToJSON("inputValues", values)
            self.stateVisualization = VisualizationWindow(self)
            self.stateVisualization.show()
            self.hide()
            
    def useCustomValues(self):
        """Lets the user use custom values for analysis obtained from JSON-file.
        """
        values = readFromJSON("assets/custom.json")
        
        isApproved = checkValues(values)

        if (isApproved):
            writeToJSON("inputValues", values)
            self.stateVisualization = VisualizationWindow(self)
            self.stateVisualization.show()
            self.hide()
    #endregion
    
class ManualInput(QDialog):
    """Presents the user with and gathers the required input-values to perform the analysis.

    Args:
        QDialog (PyQt5.QtWidgets.QDialog): Instance to initialize.
    """
    
    def __init__(self, parent=None):
        """Initialization-function for the 'ManualInput'-class.

        Args:
            parent (PyQt5.QtWidgets.QDialog, optional): Optional parent of the instance. Defaults to None.
        """
        
        super(ManualInput, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Manual input")
        
        # Create widgets
        self.prompt = QLabel("Please enter the values below.")
        self.prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt.setFixedSize(750, 100)
        self.prompt.setObjectName("prompt")
        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(150, 50)
        self.returnButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.continueButton = QPushButton("Continue")
        self.continueButton.setFixedSize(150, 50)
        self.continueButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create form
        self.volume = QLabel("Volume [mm^3]")
        self.volume.setAlignment(QtCore.Qt.AlignCenter)
        self.volume.setFixedSize(750, 50)
        self.v_cyl_prompt = QLabel("Cylinder:")
        self.v_cyl_prompt.setFixedSize(150, 30)
        self.v_cyl = QLineEdit()
        self.v_cyl.setFixedSize(150, 30)
        self.v_reg_prompt = QLabel("Regenerator:")
        self.v_reg_prompt.setFixedSize(150, 30)
        self.v_reg = QLineEdit()
        self.v_reg.setFixedSize(150, 30)
        self.v_cyl_avg_prompt = QLabel("Cylinder average:")
        self.v_cyl_avg_prompt.setFixedSize(150, 30)
        self.v_cyl_avg = QLineEdit()
        self.v_cyl_avg.setFixedSize(150, 30)

        self.area = QLabel("Area [mm^2]")
        self.area.setAlignment(QtCore.Qt.AlignCenter)
        self.area.setFixedSize(750, 50)
        self.piston_rod_area_prompt = QLabel("Piston rod surface:")
        self.piston_rod_area_prompt.setFixedSize(150, 30)
        self.piston_rod_area = QLineEdit()
        self.piston_rod_area.setFixedSize(150, 30)
        self.piston_cyl_area_prompt = QLabel("Piston cylinder:")
        self.piston_cyl_area_prompt.setFixedSize(150, 30)
        self.piston_cyl_area = QLineEdit()
        self.piston_cyl_area.setFixedSize(150, 30)
        
        self.temperature = QLabel("Temperature [C]")
        self.temperature.setAlignment(QtCore.Qt.AlignCenter)
        self.temperature.setFixedSize(750, 50)
        self.t_exp_prompt = QLabel("Expansion:")
        self.t_exp_prompt.setFixedSize(150, 30)
        self.t_exp = QLineEdit()
        self.t_exp.setFixedSize(150, 30)
        self.t_reg_prompt = QLabel("Regenerator:")
        self.t_reg_prompt.setFixedSize(150, 30)
        self.t_reg = QLineEdit()
        self.t_reg.setFixedSize(150, 30)
        self.t_com_prompt = QLabel("Compression:")
        self.t_com_prompt.setFixedSize(150, 30)
        self.t_com = QLineEdit()
        self.t_com.setFixedSize(150, 30)
        
        self.additional = QLabel("Additional values")
        self.additional.setAlignment(QtCore.Qt.AlignCenter)
        self.additional.setFixedSize(750, 50)
        self.phaseangle_prompt = QLabel("Phase-angle \u03B2:")
        self.phaseangle_prompt.setFixedSize(150, 30)
        self.phaseangle = QLineEdit()
        self.phaseangle.setFixedSize(150, 30)
        self.mass_prompt = QLabel("Mass:")
        self.mass_prompt.setFixedSize(150, 30)
        self.mass = QLineEdit()
        self.mass.setFixedSize(150, 30)
        self.gas_constant_prompt = QLabel("Gas constant:")
        self.gas_constant_prompt.setFixedSize(150, 30)
        self.gas_constant = QLineEdit()
        self.gas_constant.setFixedSize(150, 30)
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.prompt, 0, 0, 1, 5)
        
        layout.addWidget(self.volume, 1, 0, 1, 5)
        layout.addWidget(self.v_cyl_prompt, 2, 1, 1, 1)
        layout.addWidget(self.v_cyl, 2, 3, 1, 1)
        layout.addWidget(self.v_reg_prompt, 3, 1, 1, 1)
        layout.addWidget(self.v_reg, 3, 3, 1, 1)
        layout.addWidget(self.v_cyl_avg_prompt, 4, 1, 1, 1)
        layout.addWidget(self.v_cyl_avg, 4, 3, 1, 1)
        
        layout.addWidget(self.temperature, 5, 0, 1, 5)
        layout.addWidget(self.t_exp_prompt, 6, 1, 1, 1)
        layout.addWidget(self.t_exp, 6, 3, 1, 1)
        layout.addWidget(self.t_reg_prompt, 7, 1, 1, 1)
        layout.addWidget(self.t_reg, 7, 3, 1, 1)
        layout.addWidget(self.t_com_prompt, 8, 1, 1, 1)
        layout.addWidget(self.t_com, 8, 3, 1, 1)

        layout.addWidget(self.area, 9, 0, 1, 5)
        layout.addWidget(self.piston_rod_area_prompt, 10, 1, 1, 1)
        layout.addWidget(self.piston_rod_area, 10, 3, 1, 1)
        layout.addWidget(self.piston_cyl_area_prompt, 11, 1, 1, 1)
        layout.addWidget(self.piston_cyl_area, 11, 3, 1, 1)
        
        layout.addWidget(self.additional, 12, 0, 1, 5)
        layout.addWidget(self.mass_prompt, 13, 1, 1, 1)
        layout.addWidget(self.mass, 13, 3, 1, 1)
        layout.addWidget(self.gas_constant_prompt, 14, 1, 1, 1)
        layout.addWidget(self.gas_constant, 14, 3, 1, 1)
        layout.addWidget(self.phaseangle_prompt, 15, 1, 1, 1)
        layout.addWidget(self.phaseangle, 15, 3, 1, 1)
        
        layout.addWidget(QLabel(""), 16, 1, 1, 5)
        
        layout.addWidget(self.returnButton, 17, 1, 1, 1)
        layout.addWidget(self.continueButton, 17, 3, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect buttons
        self.returnButton.clicked.connect(self.returnToIntro)
        self.continueButton.clicked.connect(self.continueToVisualization)
        
    #region Methods for navigation
    def returnToIntro(self):
        """Navigates the user to the 'Intro'-window.
        """
        
        self.intro = Intro(self)
        self.intro.show()
        self.hide()
    
    def continueToVisualization(self):
        """Navigates the user to the 'VisualizationWindow'-window if the input-data is valid.
        """
        
        valueList = [self.gas_constant, self.mass, self.t_exp, self.t_reg, self.t_com, self.v_cyl, self.v_reg, self.v_cyl_avg, self.piston_rod_area, self.piston_cyl_area, self.phaseangle, self.gas_constant]
        values = []

        for item in valueList:
            values.append(item.text())

        isApproved = checkValues(values)

        if (isApproved):
            values = {
                "gasconstant": self.gas_constant.text(),
                "mass": self.mass.text(),
                "tExpansion": self.t_exp.text(),
                "tRegenerator": self.t_reg.text(),
                "tCompression": self.t_com.text(),
                "vSwept": self.v_cyl.text(),
                "vRegenerator": self.v_reg.text(),
                "vAverage": self.v_cyl_avg.text(),
                "aPiston": self.piston_rod_area.text(),
                "aCylinder": self.piston_cyl_area.text(),
                "phaseangle": self.phaseangle.text()
            }
            
            writeToJSON("inputValues", values)
            self.stateVisualization = VisualizationWindow(self)
            self.stateVisualization.show()
            self.hide()
        else:
            self.manualInput = ManualInput(self)
            self.manualInput.show()
            self.hide()
    #endregion

class VisualizationWindow(QDialog):
    """Presents the user with a visualization of the results of the analyses, in addition to an animation.

    Args:
        QDialog (PyQt5.QtWidgets.QDialog): Instance to initialize.

    Returns:
        Int: The current number of degrees to display in the visualization.
    """
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self, parent=None):
        """Initialization-function for the 'VisualizationWindow'-class.

        Args:
            parent (PyQt5.QtWidgets.QDialog, optional): Optional parent of the instance. Defaults to None.
        """
        
        super(VisualizationWindow, self).__init__(parent)
        window = QtOpenGL.QGLWidget()
        self.setWindowTitle("Stirling engine state visualization")
        
        self.widget = QVTKRenderWindowInteractor(window)
        self.widget.setFixedSize(450, 800)
        self.widget.Initialize()
        self._degree = 0
        
        self.stirlingAnimation = StirlingAnimation()
        self.ren = self.stirlingAnimation.getRenderer()
        self.widget.GetRenderWindow().AddRenderer(self.ren)
        
        actorList = self.stirlingAnimation.getActors()
        
        self.cylinderActor = actorList[0]
        self.leftPistonActor = actorList[1]
        self.rightPistonActor = actorList[2]
        self.expansionVolumeActor = actorList[3]
        self.compressionVolumeActor = actorList[4]
        self.regeneratorActor = actorList[5]
        self.flywheelActor = actorList[6]
        self.flywheelCenterActor = actorList[7]
        self.flywheelCenterRadiusActor = actorList[8]
        self.expansionPistonRodActor = actorList[9]
        self.expansionPistonAnchorActor = actorList[10]
        self.compressionPistonRodActor = actorList[11]
        self.compressionPistonAnchorActor = actorList[12]
        
        self.ren.AddActor(self.cylinderActor)
        self.ren.AddActor(self.leftPistonActor)
        self.ren.AddActor(self.rightPistonActor)
        self.ren.AddActor(self.expansionVolumeActor)
        self.ren.AddActor(self.compressionVolumeActor)
        self.ren.AddActor(self.regeneratorActor)
        self.ren.AddActor(self.flywheelActor)
        self.ren.AddActor(self.flywheelCenterActor)
        self.ren.AddActor(self.flywheelCenterActor)
        self.ren.AddActor(self.flywheelCenterRadiusActor)
        self.ren.AddActor(self.expansionPistonRodActor)
        self.ren.AddActor(self.expansionPistonAnchorActor)
        self.ren.AddActor(self.compressionPistonRodActor)
        self.ren.AddActor(self.compressionPistonAnchorActor)
        
        self.ren.Render()
        
        self.animation = QPropertyAnimation(self, b"degree")
        self.animation.setLoopCount(100)
        self.animation.setEndValue(360)
        self.animation.setDuration(10000)
        self.animation.start()
        
        # Create widgets
        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(100, 50)
        self.returnButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.continueButton = QPushButton("Continue")
        self.continueButton.setFixedSize(100, 50)
        self.continueButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        self.spinBox = QSpinBox(self)
        #self.spinBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.spinBox.valueChanged.connect(self.showFrame)
        self.spinBox.setFixedSize(90, 30)
        self.spinBox.setRange(0, 360)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 360)
        self.progressBar.setValue(self._degree)
        self.progressBar.setFixedSize(450, 30)
        self.progressBar.setFormat("Degree: " + str(self._degree) + "\N{DEGREE SIGN}")
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(5000, 15000)
        self.slider.setFixedSize(360, 30)
        self.slider.setValue(10000)
        
        # Create navigation-buttons
        self.playButton = QPushButton("Play")
        self.playButton.setFixedSize(90, 50)
        self.playButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pauseButton = QPushButton("Pause")
        self.pauseButton.setFixedSize(90, 50)
        self.pauseButton.setFocusPolicy(QtCore.Qt.NoFocus)

        # Create plots
        self.createPlots()
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.widget, 0, 0, 10, 5)
        layout.addWidget(self.playButton, 13, 1, 1, 1)
        layout.addWidget(self.pauseButton, 13, 3, 1, 1)
        layout.addWidget(self.returnButton, 13, 8, 1, 1)
        layout.addWidget(self.continueButton, 13, 10, 1, 1)
        layout.addWidget(self.spinBox, 12, 0, 1, 1)
        layout.addWidget(self.progressBar, 11, 0, 1, 5)
        layout.addWidget(self.slider, 12, 1, 1, 3)
        layout.addWidget(self.canvas, 0, 5, 13, 10)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect buttons
        self.playButton.clicked.connect(self.playAnimation)
        self.pauseButton.clicked.connect(self.pauseAnimation)
        self.returnButton.clicked.connect(self.returnToIntro)
        self.continueButton.clicked.connect(self.continueToResults)
        
    #region Methods for animation
    def createPlots(self):
        """Creates the plots used for visualization of the results of the analyses.
        """
        
        calculationValues = readFromJSON("assets/inputValues.json")
        print("These values were read from the JSON-file containing input-values:")
        print(calculationValues)
        self.schmidtAnalysis = schmidtAnalysis(calculationValues)
        
        self.canvas = pg.GraphicsLayoutWidget(size=(1000, 800))
        self.canvas.setBackground('w')
        self.plotMarkers = []
        print(self.plotMarkers)
        
        createInternalSchmidtPlots(self, self.schmidtAnalysis)
        
        self.canvas.setFocusPolicy(QtCore.Qt.NoFocus)
        
    @pyqtProperty(int)
    def degree(self):
        """Returns the current number of degrees.

        Returns:
            Int: Current number of degrees.
        """
        return self._degree
    
    @degree.setter
    def degree(self, degree):
        """Sets the current number of degrees and notifies the observers.

        Args:
            degree (int): Current number of degrees.
        """
        if (degree != self._degree):
            self._degree = degree
            self.updateValues(self._degree)
            self.valueChanged.emit(degree)
                        
    def updateValues(self, degree):
        """Updates the position for each vertex in the VTK-animation.

        Args:
            degree (int): The degree used to calculate the position.
        """
        
        self.updatePlots(degree)
        self.updateActors(degree)
        self.spinBox.setValue(degree)
        self.progressBar.setValue(degree)
        self.animation.setDuration(self.slider.value())
        self.progressBar.setFormat("Degree: " + str(self._degree) + "\N{DEGREE SIGN}")
        
    def updateActors(self, degree):
        """Updates the position for each vertex in the VTK-animation.

        Args:
            degree (int): The degree used to calculate the position.
        """
        
        self.leftPistonActor.SetPosition([0, self.stirlingAnimation.calculateHeight(degree)])
        self.rightPistonActor.SetPosition([0, - self.stirlingAnimation.calculateHeight(degree)])
        
        self.expansionVolumeActor.SetMapper(self.stirlingAnimation.generateExpansionVolumeMapper(self.stirlingAnimation.calculateHeight(degree) + 1, self.stirlingAnimation.calculateColorScale(degree)))
        self.compressionVolumeActor.SetMapper(self.stirlingAnimation.generateCompressionVolumeMapper(- self.stirlingAnimation.calculateHeight(degree) + 1, self.stirlingAnimation.calculateColorScale(-degree)))
        
        self.expansionPistonAnchorActor.SetMapper(self.stirlingAnimation.generateExpansionPistonAnchorMapper(degree))
        self.compressionPistonAnchorActor.SetMapper(self.stirlingAnimation.generateCompressionPistonAnchorMapper(degree))
        
        self.expansionPistonRodActor.SetMapper(self.stirlingAnimation.generateExpansionPistonRodMapper(degree))
        self.compressionPistonRodActor.SetMapper(self.stirlingAnimation.generateCompressionPistonRodMapper(degree))
        
        self.ren.Render()
        
        self.widget.update()
            
    def updatePlots(self, degree):
        """Updates the degree-marker for each plot.

        Args:
            degree (int): The degree used to calculate the position.
        """
        
        for marker in self.plotMarkers:
            marker.setValue(degree)
        
    def playAnimation(self):
        """Starts or resumes the animation.
        """
        
        self.animation.start()
        
    def pauseAnimation(self):
        """Pauses the animation.
        """
        
        self.animation.pause()
    
    def showFrame(self):
        """Updates the current number of degrees in the spinbox and the animation.
        """
        
        self._degree = self.spinBox.value()
        self.updateValues(self._degree)
            
    def getDegree(self):
        """Returns the current number of degrees.

        Returns:
            Int: Current number of degrees.
        """
        
        return self._degree
    #endregion
        
    #region Methods for navigation
    def returnToIntro(self):
        """Navigates the user to the 'Intro'-window.
        """
        
        self.animation.stop()
        self.intro = Intro(self)
        self.intro.show()
        self.hide()
        
    def continueToResults(self):
        """Navigates the user to the 'Results'-window.
        """
        
        self.animation.stop()
        self.results = ResultWindow(self)
        self.results.show()
        self.hide()
    #endregion
        
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        """Closes the window and its widgets (including animation).

        Args:
            a0 (QtGui.QCloseEvent): The window's closing event.
        """
        
        super().closeEvent(a0)
        self.widget.closeEvent()
        self.canvas.closeEvent()
        self.widget.Finalize()
        
class ResultWindow(QDialog):
    """Confirms to the user that the analyses have been completed and shows where the results are stored.

    Args:
        QDialog (PyQt5.QtWidgets.QDialog): Instance to initialize.
    """
    
    def __init__(self, parent=None):
        """Initialization-function for the 'ResultWindow'-class.

        Args:
            parent (QDialog, optional): Optional parent of the instance. Defaults to None.
        """
        
        super(ResultWindow, self).__init__(parent)
        window = QWidget()
        self.setWindowTitle("Results of analysis")
        
        # Create widgets
        self.complete_message = QLabel("The analysis is complete.")
        self.complete_message.setAlignment(QtCore.Qt.AlignCenter)
        self.complete_message.setFixedSize(750, 100)
        self.complete_message.setObjectName("complete_message")
        self.complete_message.setStyleSheet("font-weight: bold; font-size: 30px;")

        self.schmidtAnalysisFilename = "schmidtanalysis"
        self.schmidtResultsFilename = "schmidtanalysis"
        self.adiabaticAnalysisFilename = "adiabaticanalysis"
        self.adiabaticResultsFilename = "adiabaticanalysis"
        self.combinedAnalysisFilename = "combinedanalysis"

        self.result_message = QLabel("The plots are stored under: 'results/" + self.schmidtAnalysisFilename + ".pdf', 'results/" + self.adiabaticAnalysisFilename + ".pdf'")
        self.result_message.setAlignment(QtCore.Qt.AlignCenter)
        self.result_message.setFixedSize(750, 100)
        self.result_message.setObjectName("result_message")
        
        self.combinedplots_message = QLabel("The combined plots from each analysis-method are stored under: 'results/" + self.combinedAnalysisFilename + ".pdf'")
        self.combinedplots_message.setAlignment(QtCore.Qt.AlignCenter)
        self.combinedplots_message.setFixedSize(750, 100)
        self.combinedplots_message.setObjectName("combinedplots_message")

        self.csv_message = QLabel("The results are stored under: 'results/" + self.schmidtResultsFilename + ".csv', 'results/" + self.adiabaticResultsFilename + ".csv'")
        self.csv_message.setAlignment(QtCore.Qt.AlignCenter)
        self.csv_message.setFixedSize(750, 100)
        self.csv_message.setObjectName("result_message")

        self.returnButton = QPushButton("Return")
        self.returnButton.setFixedSize(150, 50)
        self.returnButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
          
        self.exitButton = QPushButton("Exit application")
        self.exitButton.setFixedSize(150, 50)
        self.exitButton.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Create layout and add widgets
        layout = QGridLayout(window)

        # Calculate results
        calculationValues = readFromJSON("assets/inputValues.json")
        #print("These values were read from the JSON-file containing input-values:")
        #print(calculationValues)
        schmidt = schmidtAnalysis(calculationValues)
        adiabatic = adiabaticAnalysis(calculationValues, schmidt)

        # Plot results
        plotSchmidtAnalysis(self.schmidtAnalysisFilename, schmidt)
        plotAdiabaticAnalysis(self.adiabaticAnalysisFilename, adiabatic)
        plotCombinedAnalysis(self.combinedAnalysisFilename, schmidt, adiabatic)

        # Save results
        writeResultsToCSV(self.schmidtResultsFilename, schmidt)
        writeResultsToCSV(self.adiabaticResultsFilename, adiabatic)
        
        # Create layout and add widgets
        layout = QGridLayout(window)
        layout.addWidget(self.complete_message, 0, 0, 2, 5)
        
        layout.addWidget(self.result_message, 2, 0, 1, 5)
        layout.addWidget(self.combinedplots_message, 3, 0, 1, 5)
        layout.addWidget(self.csv_message, 4, 0, 1, 5)
        
        layout.addWidget(self.returnButton, 5, 1, 1, 1)
        layout.addWidget(self.exitButton, 5, 3, 1, 1)
        
        # Set layout
        self.setLayout(layout)
        
        # Connect buttons
        self.returnButton.clicked.connect(self.returnToStateVisualization)
        self.exitButton.clicked.connect(self.exitApplication)
    
    def returnToStateVisualization(self):
        """Navigates the user to the 'VisualizationWindow'-window.
        """
        
        self.stateVisualization = VisualizationWindow(self)
        self.stateVisualization.show()
        self.hide()
        
    def exitApplication(self):
        """Exits the application.
        """
        
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