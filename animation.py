#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import PyQt5
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import time
import math
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from PyQt5.QtCore import QUrl, QTimer, QObject, pyqtSignal, pyqtProperty


class StirlingAnimation():
    
    def __init__(self, parent=None):
        self.offsetCenterAxis = 195
        self.flywheelHorizontalCenter = 225
        self.flywheelVerticalCenter = 675
        self.flywheelRadius = 120
        self.pistonHeight = self.offsetCenterAxis + 240
        
        degree = 0
        
        colors = vtkNamedColors()
        
        cylinderPoints = vtkPoints()
        leftPistonPoints = vtkPoints()
        rightPistonPoints = vtkPoints()
        regeneratorPoints = vtkPoints()
        
        cylinderVertices = [(0, 100, 0), (150, 100, 0), (150, 110, 0),  # 0, 1, 2
                    (0, 110, 0), (10, 100, 0), (10, 300, 0),            # 3, 4, 5
                    (0, 300, 0), (190, 80, 0), (200, 300, 0),           # 6, 7, 8
                    (190, 300, 0), (90, 300, 0), (90, 310, 0),          # 9, 10, 11
                    (0, 310, 0), (110, 300, 0), (200, 310, 0),          # 12, 13, 14
                    (110, 310, 0), (80, 310, 0), (90, 320, 0),          # 15, 16, 17
                    (80, 320, 0), (120, 310, 0), (120, 320, 0),         # 18, 19, 20
                    (110, 320, 0), (200, 80, 0), (140, 100, 0),         # 21, 22, 23
                    (140, 40, 0), (150, 40, 0), (140, 30, 0),           # 24, 25, 26
                    (300, 30, 0), (300, 40, 0), (260, 80, 0),           # 27, 28, 29
                    (260, 90, 0), (190, 90, 0), (250, 80, 0),           # 30, 31, 32
                    (260, 300, 0), (250, 300, 0), (310, 30, 0),         # 33, 34, 35
                    (310, 100, 0), (300, 100, 0), (450, 100, 0),        # 36, 37, 38
                    (450, 110, 0), (300, 110, 0), (440, 100, 0),        # 39, 40, 41
                    (450, 300, 0), (440, 300, 0), (340, 300, 0),        # 42, 43, 44
                    (340, 310, 0), (250, 310, 0), (360, 300, 0),        # 45, 46, 47
                    (450, 310, 0), (360, 310, 0), (330, 300, 0),        # 48, 49, 50
                    (340, 320, 0), (330, 320, 0), (370, 300, 0),        # 51, 52, 53
                    (370, 320, 0), (360, 320, 0)]                       # 54, 55
        
        leftPistonVertices = [(10, self.offsetCenterAxis, 1), (190, self.offsetCenterAxis, 1), (190, self.offsetCenterAxis + 30, 1),                   # 0, 1, 2
                            (10, self.offsetCenterAxis + 30, 1), (90, self.offsetCenterAxis + 30, 1), (110, self.offsetCenterAxis + 30, 1),           # 3, 4, 5
                            (110, self.offsetCenterAxis + 240, 1), (90, self.offsetCenterAxis + 240, 1)]                                         # 6, 7
        
        rightPistonVertices = [(260, self.offsetCenterAxis, 0), (440, self.offsetCenterAxis, 0), (440, self.offsetCenterAxis + 30, 0),                 # 0, 1, 2
                                (260, self.offsetCenterAxis + 30, 0), (340, self.offsetCenterAxis + 30, 0), (360, self.offsetCenterAxis + 30, 0),    # 3, 4, 5
                                (360, self.offsetCenterAxis + 240, 0), (340, self.offsetCenterAxis + 240, 0)]                                   # 6, 7
        
        regeneratorVertices = [(150, 40, 0), (300, 40, 0), (300, 80, 0),    # 0, 1, 2
                            (150, 80, 0), (190, 80, 0), (190, 110, 0),   # 3, 4, 5
                            (150, 110, 0), (260, 80, 0), (300, 110, 0),  # 6, 7, 8
                            (260, 110, 0)]                               # 9
        
        for point in cylinderVertices:
            cylinderPoints.InsertNextPoint(point)
            
        for point in leftPistonVertices:
            leftPistonPoints.InsertNextPoint(point)
            
        for point in rightPistonVertices:
            rightPistonPoints.InsertNextPoint(point)
            
        for point in regeneratorVertices:
            regeneratorPoints.InsertNextPoint(point)

        cylinderFace = vtkCellArray()
        leftPistonFace = vtkCellArray()
        rightPistonFace = vtkCellArray()
        regeneratorFace = vtkCellArray()

        cylinderFaces = [(0, 1, 2, 3), (0, 4, 5, 6), (7, 22, 8, 9),
                        (6, 10, 11, 12), (13, 8, 14, 15), (16, 11, 17, 18),
                        (15, 19, 20, 21), (24, 25, 1, 23), (26, 27, 28, 24),
                        (7, 29, 30, 31), (32, 29, 33, 34), (27, 35, 36, 37),
                        (37, 38, 39, 40), (41, 38, 42, 43), (34, 44, 45, 46),
                        (47, 42, 48, 49), (50, 44, 51, 52), (47, 53, 54, 55)]
        
        leftPistonFaces = [(0, 1, 2, 3), (4, 5, 6, 7)]
        
        rightPistonFaces = [(0, 1, 2, 3), (4, 5, 6, 7)]
        
        regeneratorFaces = [(0, 1, 2, 3), (3, 4, 5, 6), (7, 2, 8, 9)]
        
        for face in cylinderFaces:
            cylinderFace.InsertNextCell(self.mkVtkIdList(face))
            
        for face in leftPistonFaces:
            leftPistonFace.InsertNextCell(self.mkVtkIdList(face))
            
        for face in rightPistonFaces:
            rightPistonFace.InsertNextCell(self.mkVtkIdList(face))
        
        for face in regeneratorFaces:
            regeneratorFace.InsertNextCell(self.mkVtkIdList(face))
        
        regeneratorColors = vtkUnsignedCharArray()
        regeneratorColors.SetNumberOfComponents(3)
        regeneratorColors.SetName("Regenerator colors")
        regeneratorColors.InsertNextTuple3(50.0, 0.0, 50.0)
        regeneratorColors.InsertNextTuple3(50.0, 0.0, 50.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)
        regeneratorColors.InsertNextTuple3(75.0, 0.0, 75.0)

        cylinderPolydata = vtkPolyData()
        cylinderPolydata.SetPoints(cylinderPoints)
        cylinderPolydata.SetPolys(cylinderFace)
        
        leftPistonPolydata = vtkPolyData()
        leftPistonPolydata.SetPoints(leftPistonPoints)
        leftPistonPolydata.SetPolys(leftPistonFace)
        
        rightPistonPolydata = vtkPolyData()
        rightPistonPolydata.SetPoints(rightPistonPoints)
        rightPistonPolydata.SetPolys(rightPistonFace)
        
        regeneratorPolydata = vtkPolyData()
        regeneratorPolydata.SetPoints(regeneratorPoints)
        regeneratorPolydata.SetPolys(regeneratorFace)
        regeneratorPolydata.GetPointData().SetScalars(regeneratorColors)

        flywheelSource = vtkRegularPolygonSource()
        flywheelSource.SetNumberOfSides(50)
        flywheelSource.SetRadius(self.flywheelRadius)
        flywheelSource.SetCenter(self.flywheelHorizontalCenter, self.flywheelVerticalCenter, 0.0)
        
        flywheelCenterSource = vtkRegularPolygonSource()
        flywheelCenterSource.SetNumberOfSides(50)
        flywheelCenterSource.SetRadius(50.0)
        flywheelCenterSource.SetCenter(self.flywheelHorizontalCenter, self.flywheelVerticalCenter, 0.0)
        
        flywheelCenterRadiusSource = vtkRegularPolygonSource()
        flywheelCenterRadiusSource.GeneratePolygonOff()
        flywheelCenterRadiusSource.SetNumberOfSides(50)
        flywheelCenterRadiusSource.SetRadius(50.0)
        flywheelCenterRadiusSource.SetCenter(self.flywheelHorizontalCenter, self.flywheelVerticalCenter, 0.0)

        cylinderMapper = vtkPolyDataMapper2D()
        cylinderMapper.SetInputData(cylinderPolydata)
        cylinderMapper.Update()
        
        leftPistonMapper = vtkPolyDataMapper2D()
        leftPistonMapper.SetInputData(leftPistonPolydata)
        leftPistonMapper.Update()
        
        rightPistonMapper = vtkPolyDataMapper2D()
        rightPistonMapper.SetInputData(rightPistonPolydata)
        rightPistonMapper.Update()
        
        expansionVolumeMapper = self.generateExpansionVolumeMapper(self.calculateHeight(degree), self.calculateColorScale(degree))    
        compressionVolumeMapper = self.generateCompressionVolumeMapper(- self.calculateHeight(degree), self.calculateColorScale(-degree))
        
        regeneratorMapper = vtkPolyDataMapper2D()
        regeneratorMapper.SetInputData(regeneratorPolydata)
        regeneratorMapper.Update()

        flywheelMapper = vtkPolyDataMapper2D()
        flywheelMapper.SetInputConnection(flywheelSource.GetOutputPort())
        
        flywheelCenterMapper = vtkPolyDataMapper2D()
        flywheelCenterMapper.SetInputConnection(flywheelCenterSource.GetOutputPort())
        
        flywheelCenterRadiusMapper = vtkPolyDataMapper2D()
        flywheelCenterRadiusMapper.SetInputConnection(flywheelCenterRadiusSource.GetOutputPort())

        self.cylinderActor = vtkActor2D()
        self.cylinderActor.SetMapper(cylinderMapper)
        self.cylinderActor.GetProperty().SetColor(colors.GetColor3d('Grey'))
        self.cylinderActor.GetProperty().SetPointSize(8)
        
        self.leftPistonActor = vtkActor2D()
        self.leftPistonActor.SetMapper(leftPistonMapper)
        self.leftPistonActor.GetProperty().SetColor(colors.GetColor3d('DarkSlateGray'))
        self.leftPistonActor.GetProperty().SetPointSize(8)
        
        self.rightPistonActor = vtkActor2D()
        self.rightPistonActor.SetMapper(rightPistonMapper)
        self.rightPistonActor.GetProperty().SetColor(colors.GetColor3d('DarkSlateGray'))
        self.rightPistonActor.GetProperty().SetPointSize(8)
        
        self.expansionVolumeActor = vtkActor2D()
        self.expansionVolumeActor.SetMapper(expansionVolumeMapper)
        self.expansionVolumeActor.GetProperty().SetPointSize(8)
        
        self.compressionVolumeActor = vtkActor2D()
        self.compressionVolumeActor.SetMapper(compressionVolumeMapper)
        self.compressionVolumeActor.GetProperty().SetPointSize(8)
        
        self.regeneratorActor = vtkActor2D()
        self.regeneratorActor.SetMapper(regeneratorMapper)
        self.regeneratorActor.GetProperty().SetPointSize(8)

        self.flywheelActor = vtkActor2D()
        self.flywheelActor.SetMapper(flywheelMapper)
        self.flywheelActor.GetProperty().SetColor(colors.GetColor3d('DarkGray'))
        
        self.flywheelCenterActor = vtkActor2D()
        self.flywheelCenterActor.SetMapper(flywheelCenterMapper)
        self.flywheelCenterActor.GetProperty().SetColor(colors.GetColor3d('LightGrey'))
        
        self.flywheelCenterRadiusActor = vtkActor2D()
        self.flywheelCenterRadiusActor.SetMapper(flywheelCenterRadiusMapper)
        self.flywheelCenterRadiusActor.GetProperty().SetColor(colors.GetColor3d('Black'))
        
        self.expansionPistonAnchorActor = vtkActor2D()
        self.expansionPistonAnchorActor.SetMapper(self.generateExpansionPistonAnchorMapper(degree))
        self.expansionPistonAnchorActor.GetProperty().SetColor(colors.GetColor3d('LightGrey'))
        
        self.compressionPistonAnchorActor = vtkActor2D()
        self.compressionPistonAnchorActor.SetMapper(self.generateCompressionPistonAnchorMapper(degree))
        self.compressionPistonAnchorActor.GetProperty().SetColor(colors.GetColor3d('LightGrey'))
        
        self.expansionPistonRodActor = vtkActor2D()
        self.expansionPistonRodActor.SetMapper(self.generateExpansionPistonRodMapper(degree))
        self.expansionPistonRodActor.GetProperty().SetColor(colors.GetColor3d('DarkSlateGray'))
        
        self.compressionPistonRodActor = vtkActor2D()
        self.compressionPistonRodActor.SetMapper(self.generateCompressionPistonRodMapper(degree))
        self.compressionPistonRodActor.GetProperty().SetColor(colors.GetColor3d('DarkSlateGray'))
        
        # Create a renderer, render window, and interactor
        self.renderer = vtkRenderer()
        self.renderWindow = vtkRenderWindow()
        self.renderWindow.AddRenderer(self.renderer)
        self.renderWindow.SetWindowName("Stirling engine animation")
        self.renderWindowInteractor = vtkRenderWindowInteractor()
        self.renderWindowInteractor.SetRenderWindow(self.renderWindow)

        # Add the actor to the scene
        self.renderer.AddActor(self.cylinderActor)
        self.renderer.AddActor(self.leftPistonActor)
        self.renderer.AddActor(self.rightPistonActor)
        self.renderer.AddActor(self.expansionVolumeActor)
        self.renderer.AddActor(self.compressionVolumeActor)
        self.renderer.AddActor(self.regeneratorActor)
        self.renderer.AddActor(self.flywheelActor)
        self.renderer.AddActor(self.flywheelCenterActor)
        self.renderer.AddActor(self.flywheelCenterRadiusActor)
        self.renderer.AddActor(self.expansionPistonRodActor)
        self.renderer.AddActor(self.expansionPistonAnchorActor)
        self.renderer.AddActor(self.compressionPistonRodActor)
        self.renderer.AddActor(self.compressionPistonAnchorActor)
        self.renderWindow.SetSize(450, 800)
        self.renderer.SetBackground(colors.GetColor3d('White'))
        self.renderWindow.SetWindowName('Animation of Stirling Engine')

        #self.renderWindowInteractor.Initialize()

        # Render and interact
        #self.renderWindow.Render()
        
        # TODO Remove 'While'-loop and place it outside the function
        # TODO Add input-values for 'degree' / 'degree' and potentially other values.
        # TODO Add descriptions and documentation
        
        # w2if = vtkWindowToImageFilter()
        # w2if.SetInput(renderWindow)
        # w2if.Update()
        # writer = vtkPNGWriter()
        # writer.SetFileName('TestActor2D.png')
        # writer.SetInputConnection(w2if.GetOutputPort())
        # writer.Write()
        
        # TODO Needed to display a single image. Maybe use 'start' and 'stop' to show?
        # Eventually just animate a single frame with a long sleep-function
        #self.renderWindowInteractor.Start()
        
    def animateStep(self, degree):
            self.leftPistonActor.SetPosition([0, self.calculateHeight(degree)])
            self.rightPistonActor.SetPosition([0, - self.calculateHeight(degree)])
            
            # TODO Add preloading of the next mapper and save it for hotswap
            self.expansionVolumeActor.SetMapper(self.generateExpansionVolumeMapper(self.calculateHeight(degree) + 1, self.calculateColorScale(degree)))
            self.compressionVolumeActor.SetMapper(self.generateCompressionVolumeMapper(- self.calculateHeight(degree) + 1, self.calculateColorScale(-degree)))
            
            self.expansionPistonAnchorActor.SetMapper(self.generateExpansionPistonAnchorMapper(degree))
            self.compressionPistonAnchorActor.SetMapper(self.generateCompressionPistonAnchorMapper(degree))
            
            self.expansionPistonRodActor.SetMapper(self.generateExpansionPistonRodMapper(degree))
            self.compressionPistonRodActor.SetMapper(self.generateCompressionPistonRodMapper(degree))
            
            self.renderWindow.Render()
    
    def mkVtkIdList(self, it):
        """
        :param it: A python iterable.
        :return: A vtkIdList
        """
        vtkIdL = vtkIdList()
        for i in it:
            vtkIdL.InsertNextId(int(i))
        return vtkIdL
        
    def calculateHeight(self, degree):
        return math.sin(degree * (2 * math.pi / 360)) * 75

    def calculateColorScale(self, degree):
        return (math.sin(degree * (2 * math.pi / 360)) + 1) * 0.5

    def calculateHorizontalMovement(self, degree, phaseShift = 0):
        return math.cos((degree + phaseShift) * (2 * math.pi / 360)) * 85
        
    def calculateVerticalMovement(self, degree, phaseShift = 0):
        if (math.sin(degree * 2 * math.pi / 360) < 0):
            return - math.sqrt(85 ** 2 - self.calculateHorizontalMovement(degree, phaseShift) ** 2)
        else:
            return math.sqrt(85 ** 2 - self.calculateHorizontalMovement(degree, phaseShift) ** 2)

    def generateExpansionVolumeMapper(self, expansionVolumeHeight, colorScale):
        expansionVolumePoints = vtkPoints()
        
        expansionVolumeVertices = [(10, 110, 0), (190, 110, 0), (190, expansionVolumeHeight + self.offsetCenterAxis, 0),
                                (10, expansionVolumeHeight + self.offsetCenterAxis, 0)]
        
        for point in expansionVolumeVertices:
            expansionVolumePoints.InsertNextPoint(point)
            
        expansionVolumeFace = vtkCellArray()
        expansionVolumeFaces = [(0, 1, 2, 3)]
        
        for face in expansionVolumeFaces:
            expansionVolumeFace.InsertNextCell(self.mkVtkIdList(face))
            
        expansionColors = vtkUnsignedCharArray()
        expansionColors.SetNumberOfComponents(3)
        expansionColors.SetName("Expansion colors")
        expansionColors.InsertNextTuple3(75.0, 0.0, 75.0)
        expansionColors.InsertNextTuple3(75.0, 0.0, 75.0)
        expansionColors.InsertNextTuple3(255.0 * colorScale, 0.0, 0.0)
        expansionColors.InsertNextTuple3(255.0 * colorScale, 0.0, 0.0)
        
        expansionVolumePolydata = vtkPolyData()
        expansionVolumePolydata.SetPoints(expansionVolumePoints)
        expansionVolumePolydata.SetPolys(expansionVolumeFace)
        expansionVolumePolydata.GetPointData().SetScalars(expansionColors)
        
        expansionVolumeMapper = vtkPolyDataMapper2D()
        expansionVolumeMapper.SetInputData(expansionVolumePolydata)
        expansionVolumeMapper.Update()
        
        return expansionVolumeMapper
        
    def generateCompressionVolumeMapper(self, compressionVolumeHeight, colorScale):
        compressionVolumePoints = vtkPoints()
        
        compressionVolumeVertices = [(260, 110, 0), (440, 110, 0), (440, compressionVolumeHeight + self.offsetCenterAxis, 0),
                                (260, compressionVolumeHeight + self.offsetCenterAxis, 0)]
        
        for point in compressionVolumeVertices:
            compressionVolumePoints.InsertNextPoint(point)
            
        compressionVolumeFace = vtkCellArray()
        compressionVolumeFaces = [(0, 1, 2, 3)]
        
        for face in compressionVolumeFaces:
            compressionVolumeFace.InsertNextCell(self.mkVtkIdList(face))
            
        compressionColors = vtkUnsignedCharArray()
        compressionColors.SetNumberOfComponents(3)
        compressionColors.SetName("Compression colors")
        compressionColors.InsertNextTuple3(75.0, 0.0, 75.0)
        compressionColors.InsertNextTuple3(75.0, 0.0, 75.0)
        compressionColors.InsertNextTuple3(0.0, 0.0, 255.0 * colorScale)
        compressionColors.InsertNextTuple3(0.0, 0.0, 255.0 * colorScale)
        
        compressionVolumePolydata = vtkPolyData()
        compressionVolumePolydata.SetPoints(compressionVolumePoints)
        compressionVolumePolydata.SetPolys(compressionVolumeFace)
        compressionVolumePolydata.GetPointData().SetScalars(compressionColors)
        
        compressionVolumeMapper = vtkPolyDataMapper2D()
        compressionVolumeMapper.SetInputData(compressionVolumePolydata)
        compressionVolumeMapper.Update()
        
        return compressionVolumeMapper

    def generateExpansionPistonAnchorMapper(self, degree):
        expansionPistonAnchorSource = vtkRegularPolygonSource()
        expansionPistonAnchorSource.SetNumberOfSides(50)
        expansionPistonAnchorSource.SetRadius(15.0)
        
        expansionPistonAnchorSource.SetCenter(self.calculateHorizontalMovement(degree) + self.flywheelHorizontalCenter, self.calculateVerticalMovement(degree) + self.flywheelVerticalCenter, 0.0)
        
        expansionPistonAnchorMapper = vtkPolyDataMapper2D()
        expansionPistonAnchorMapper.SetInputConnection(expansionPistonAnchorSource.GetOutputPort())
        
        return expansionPistonAnchorMapper

    def generateCompressionPistonAnchorMapper(self, degree):
        compressionPistonAnchorSource = vtkRegularPolygonSource()
        compressionPistonAnchorSource.SetNumberOfSides(50)
        compressionPistonAnchorSource.SetRadius(15.0)
        compressionPistonAnchorSource.SetCenter(- self.calculateHorizontalMovement(degree) + self.flywheelHorizontalCenter, - self.calculateVerticalMovement(degree) + self.flywheelVerticalCenter, 0.0)
        
        compressionPistonAnchorMapper = vtkPolyDataMapper2D()
        compressionPistonAnchorMapper.SetInputConnection(compressionPistonAnchorSource.GetOutputPort())
        
        return compressionPistonAnchorMapper

    def generateExpansionPistonRodMapper(self, degree):
        expansionPistonRodPoints = vtkPoints()
        
        expansionPistonRodVertices = [(90, self.calculateHeight(degree) + self.pistonHeight - 1, 1), (110, self.calculateHeight(degree) + self.pistonHeight - 1, 1),
                                    (self.calculateHorizontalMovement(degree) + self.flywheelHorizontalCenter + 10, self.calculateVerticalMovement(degree) + self.flywheelVerticalCenter, 0),
                                    (self.calculateHorizontalMovement(degree) + self.flywheelHorizontalCenter - 10, self.calculateVerticalMovement(degree) + self.flywheelVerticalCenter, 0)]
        
        for point in expansionPistonRodVertices:
            expansionPistonRodPoints.InsertNextPoint(point)
            
        expansionPistonRodFace = vtkCellArray()
        expansionPistonRodFaces = [(0, 1, 2, 3)]
        
        for face in expansionPistonRodFaces:
            expansionPistonRodFace.InsertNextCell(self.mkVtkIdList(face))
        
        expansionPistonRodPolydata = vtkPolyData()
        expansionPistonRodPolydata.SetPoints(expansionPistonRodPoints)
        expansionPistonRodPolydata.SetPolys(expansionPistonRodFace)
        
        expansionPistonRodMapper = vtkPolyDataMapper2D()
        expansionPistonRodMapper.SetInputData(expansionPistonRodPolydata)
        expansionPistonRodMapper.Update()
        
        return expansionPistonRodMapper

    def generateCompressionPistonRodMapper(self, degree):
        compressionPistonRodPoints = vtkPoints()
        
        compressionPistonRodVertices = [(340, - self.calculateHeight(degree) + self.pistonHeight - 1, 1), (360, - self.calculateHeight(degree) + self.pistonHeight - 1, 1),
                                    (- self.calculateHorizontalMovement(degree) + self.flywheelHorizontalCenter + 10, - self.calculateVerticalMovement(degree) + self.flywheelVerticalCenter, 0),
                                    (- self.calculateHorizontalMovement(degree) + self.flywheelHorizontalCenter - 10, - self.calculateVerticalMovement(degree) + self.flywheelVerticalCenter, 0)]
        
        for point in compressionPistonRodVertices:
            compressionPistonRodPoints.InsertNextPoint(point)
            
        compressionPistonRodFace = vtkCellArray()
        compressionPistonRodFaces = [(0, 1, 2, 3)]
        
        for face in compressionPistonRodFaces:
            compressionPistonRodFace.InsertNextCell(self.mkVtkIdList(face))
        
        compressionPistonRodPolydata = vtkPolyData()
        compressionPistonRodPolydata.SetPoints(compressionPistonRodPoints)
        compressionPistonRodPolydata.SetPolys(compressionPistonRodFace)
        
        compressionPistonRodMapper = vtkPolyDataMapper2D()
        compressionPistonRodMapper.SetInputData(compressionPistonRodPolydata)
        compressionPistonRodMapper.Update()
        
        return compressionPistonRodMapper
    
    def getActors(self):
        actorList = []
        
        actorList.append(self.cylinderActor)
        actorList.append(self.leftPistonActor)
        actorList.append(self.rightPistonActor)
        actorList.append(self.expansionVolumeActor)
        actorList.append(self.compressionVolumeActor)
        actorList.append(self.regeneratorActor)
        actorList.append(self.flywheelActor)
        actorList.append(self.flywheelCenterActor)
        actorList.append(self.flywheelCenterRadiusActor)
        actorList.append(self.expansionPistonRodActor)
        actorList.append(self.expansionPistonAnchorActor)
        actorList.append(self.compressionPistonRodActor)
        actorList.append(self.compressionPistonAnchorActor)
        
        return actorList
    
    def getRenderer(self):
        return self.renderer
    
class LeftPiston(QObject):
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self._mapper = 0
    
    @pyqtProperty(int)
    def mapper(self):
        return self._mapper
    
    @mapper.setter
    def mapper(self, mapper):
        if (mapper != self._mapper):
            self._mapper = mapper
            self.valueChanged.emit(mapper)
    
class ActorTroup(QObject):
    
    valueChanged = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self._degree = 0
        
        self.stirlingAnimation = StirlingAnimation()
        
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
    
    @pyqtProperty(int)
    def degree(self):
        return self._degree
    
    @degree.setter
    def degree(self, degree):
        if (degree != self._degree):
            self._degree = degree
            self.updateActors(degree)
            self.valueChanged.emit(degree)
            
    def updateActors(self, degree):
        self.leftPistonActor.SetPosition([0, self.stirlingAnimation.calculateHeight(degree)])
        self.rightPistonActor.SetPosition([0, - self.stirlingAnimation.calculateHeight(degree)])
        
        self.expansionVolumeActor.SetMapper(self.stirlingAnimation.generateExpansionVolumeMapper(self.stirlingAnimation.calculateHeight(degree) + 1, self.stirlingAnimation.calculateColorScale(degree)))
        self.compressionVolumeActor.SetMapper(self.stirlingAnimation.generateCompressionVolumeMapper(- self.stirlingAnimation.calculateHeight(degree) + 1, self.stirlingAnimation.calculateColorScale(-degree)))
        
        self.expansionPistonAnchorActor.SetMapper(self.stirlingAnimation.generateExpansionPistonAnchorMapper(degree))
        self.compressionPistonAnchorActor.SetMapper(self.stirlingAnimation.generateCompressionPistonAnchorMapper(degree))
        
        self.expansionPistonRodActor.SetMapper(self.stirlingAnimation.generateExpansionPistonRodMapper(degree))
        self.compressionPistonRodActor.SetMapper(self.stirlingAnimation.generateCompressionPistonRodMapper(degree))
        
        print("Degree: " + str(degree))

if __name__ == '__main__':
    stirlingClass = StirlingAnimation()
    degree = 0
    maxStep = 1080
    
    while (degree < maxStep):
        time.sleep(0.015)
        stirlingClass.animateStep(degree)
        degree += 1