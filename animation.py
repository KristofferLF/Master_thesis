#!/usr/bin/env python

# noinspection PyUnresolvedReferences
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

offsetCenterAxis = 195
flywheelHorizontalCenter = 225
flywheelVerticalCenter = 675
flywheelRadius = 120

def mkVtkIdList(it):
    """
    :param it: A python iterable.
    :return: A vtkIdList
    """
    vtkIL = vtkIdList()
    for i in it:
        vtkIL.InsertNextId(int(i))
    return vtkIL

def animateStirlingEngine():
    step = 0
    maxSteps = 360
    
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
    
    leftPistonVertices = [(10, offsetCenterAxis, 1), (190, offsetCenterAxis, 1), (190, offsetCenterAxis + 30, 1),                   # 0, 1, 2
                         (10, offsetCenterAxis + 30, 1), (90, offsetCenterAxis + 30, 1), (110, offsetCenterAxis + 30, 1),           # 3, 4, 5
                         (110, offsetCenterAxis + 240, 1), (90, offsetCenterAxis + 240, 1)]                                         # 6, 7
    
    rightPistonVertices = [(260, offsetCenterAxis, 0), (440, offsetCenterAxis, 0), (440, offsetCenterAxis + 30, 0),                 # 0, 1, 2
                              (260, offsetCenterAxis + 30, 0), (340, offsetCenterAxis + 30, 0), (360, offsetCenterAxis + 30, 0),    # 3, 4, 5
                              (360, offsetCenterAxis + 240, 0), (340, offsetCenterAxis + 240, 0)]                                   # 6, 7
    
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
        cylinderFace.InsertNextCell(mkVtkIdList(face))
        
    for face in leftPistonFaces:
        leftPistonFace.InsertNextCell(mkVtkIdList(face))
        
    for face in rightPistonFaces:
        rightPistonFace.InsertNextCell(mkVtkIdList(face))
    
    for face in regeneratorFaces:
        regeneratorFace.InsertNextCell(mkVtkIdList(face))
    
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
    flywheelSource.SetRadius(flywheelRadius)
    flywheelSource.SetCenter(flywheelHorizontalCenter, flywheelVerticalCenter, 0.0)
    
    flywheelCenterSource = vtkRegularPolygonSource()
    flywheelCenterSource.GeneratePolygonOff()
    flywheelCenterSource.SetNumberOfSides(50)
    flywheelCenterSource.SetRadius(50.0)
    flywheelCenterSource.SetCenter(flywheelHorizontalCenter, flywheelVerticalCenter, 0.0)

    cylinderMapper = vtkPolyDataMapper2D()
    cylinderMapper.SetInputData(cylinderPolydata)
    cylinderMapper.Update()
    
    leftPistonMapper = vtkPolyDataMapper2D()
    leftPistonMapper.SetInputData(leftPistonPolydata)
    leftPistonMapper.Update()
    
    rightPistonMapper = vtkPolyDataMapper2D()
    rightPistonMapper.SetInputData(rightPistonPolydata)
    rightPistonMapper.Update()
    
    expansionVolumeMapper = generateExpansionVolumeMapper(calculateHeight(step), calculateColorScale(step))    
    compressionVolumeMapper = generateCompressionVolumeMapper(- calculateHeight(step), calculateColorScale(-step))
    
    regeneratorMapper = vtkPolyDataMapper2D()
    regeneratorMapper.SetInputData(regeneratorPolydata)
    regeneratorMapper.Update()

    flywheelMapper = vtkPolyDataMapper2D()
    flywheelMapper.SetInputConnection(flywheelSource.GetOutputPort())
    
    flywheelCenterMapper = vtkPolyDataMapper2D()
    flywheelCenterMapper.SetInputConnection(flywheelCenterSource.GetOutputPort())

    cylinderActor = vtkActor2D()
    cylinderActor.SetMapper(cylinderMapper)
    cylinderActor.GetProperty().SetColor(colors.GetColor3d('Grey'))
    cylinderActor.GetProperty().SetPointSize(8)
    
    leftPistonActor = vtkActor2D()
    leftPistonActor.SetMapper(leftPistonMapper)
    leftPistonActor.GetProperty().SetColor(colors.GetColor3d('DarkSlateGray'))
    leftPistonActor.GetProperty().SetPointSize(8)
    
    rightPistonActor = vtkActor2D()
    rightPistonActor.SetMapper(rightPistonMapper)
    rightPistonActor.GetProperty().SetColor(colors.GetColor3d('DarkSlateGray'))
    rightPistonActor.GetProperty().SetPointSize(8)
    
    expansionVolumeActor = vtkActor2D()
    expansionVolumeActor.SetMapper(expansionVolumeMapper)
    expansionVolumeActor.GetProperty().SetPointSize(8)
    
    compressionVolumeActor = vtkActor2D()
    compressionVolumeActor.SetMapper(compressionVolumeMapper)
    compressionVolumeActor.GetProperty().SetPointSize(8)
    
    regeneratorActor = vtkActor2D()
    regeneratorActor.SetMapper(regeneratorMapper)
    regeneratorActor.GetProperty().SetPointSize(8)

    flywheelActor = vtkActor2D()
    flywheelActor.SetMapper(flywheelMapper)
    flywheelActor.GetProperty().SetColor(colors.GetColor3d('DarkGray'))
    
    flywheelCenterActor = vtkActor2D()
    flywheelCenterActor.SetMapper(flywheelCenterMapper)
    flywheelCenterActor.GetProperty().SetColor(colors.GetColor3d('Black'))
    
    expansionPistonAnchorActor = vtkActor2D()
    expansionPistonAnchorActor.SetMapper(generateExpansionPistonAnchorMapper(step))
    expansionPistonAnchorActor.GetProperty().SetColor(colors.GetColor3d('LightGrey'))
    
    compressionPistonAnchorActor = vtkActor2D()
    compressionPistonAnchorActor.SetMapper(generateCompressionPistonAnchorMapper(step))
    compressionPistonAnchorActor.GetProperty().SetColor(colors.GetColor3d('LightGrey'))
    
    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetWindowName("Stirling engine animation")
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(cylinderActor)
    renderer.AddActor(leftPistonActor)
    renderer.AddActor(rightPistonActor)
    renderer.AddActor(expansionVolumeActor)
    renderer.AddActor(compressionVolumeActor)
    renderer.AddActor(regeneratorActor)
    renderer.AddActor(flywheelActor)
    renderer.AddActor(flywheelCenterActor)
    renderer.AddActor(expansionPistonAnchorActor)
    renderer.AddActor(compressionPistonAnchorActor)
    renderWindow.SetSize(450, 800)
    renderer.SetBackground(colors.GetColor3d('White'))

    renderWindow.SetWindowName('Animation of Stirling Engine')

    renderWindowInteractor.Initialize()

    # Render and interact
    renderWindow.Render()
    
    continueAnimation = True
    
    # TODO Remove 'While'-loop and place it outside the function
    # TODO Add input-values for 'step' / 'degree' and potentially other values.
    # TODO Add descriptions and documentation
    
    while continueAnimation:
        time.sleep(0.025)
        leftPistonActor.SetPosition([0, calculateHeight(step)])
        rightPistonActor.SetPosition([0, - calculateHeight(step)])
        
        # TODO Add preloading of the next mapper and save it for hotswap
        expansionVolumeActor.SetMapper(generateExpansionVolumeMapper(calculateHeight(step) + 1, calculateColorScale(step)))
        compressionVolumeActor.SetMapper(generateCompressionVolumeMapper(- calculateHeight(step) + 1, calculateColorScale(-step)))
        
        expansionPistonAnchorActor.SetMapper(generateExpansionPistonAnchorMapper(step))
        compressionPistonAnchorActor.SetMapper(generateCompressionPistonAnchorMapper(step))
        
        renderWindow.Render()
        step += 1
        if (step == maxSteps):
            break
    
    # w2if = vtkWindowToImageFilter()
    # w2if.SetInput(renderWindow)
    # w2if.Update()
    # writer = vtkPNGWriter()
    # writer.SetFileName('TestActor2D.png')
    # writer.SetInputConnection(w2if.GetOutputPort())
    # writer.Write()
    
    renderWindowInteractor.Start()
    
def calculateHeight(degree):
    return math.sin(degree * (2 * math.pi / 360)) * 75

def calculateColorScale(degree):
    return (math.sin(degree * (2 * math.pi / 360)) + 1) * 0.5

def calculateHorizontalMovement(degree, phaseShift = 0):
    return math.cos((degree + phaseShift) * (2 * math.pi / 360)) * 85
    
def calculateVerticalMovement(degree, phaseShift = 0):
    if (math.sin(degree * 2 * math.pi / 360) < 0):
        return - math.sqrt(85 ** 2 - calculateHorizontalMovement(degree, phaseShift) ** 2)
    else:
        return math.sqrt(85 ** 2 - calculateHorizontalMovement(degree, phaseShift) ** 2)

def generateExpansionVolumeMapper(expansionVolumeHeight, colorScale):
    expansionVolumePoints = vtkPoints()
    
    expansionVolumeVertices = [(10, 110, 0), (190, 110, 0), (190, expansionVolumeHeight + offsetCenterAxis, 0),
                               (10, expansionVolumeHeight + offsetCenterAxis, 0)]
    
    for point in expansionVolumeVertices:
        expansionVolumePoints.InsertNextPoint(point)
        
    expansionVolumeFace = vtkCellArray()
    expansionVolumeFaces = [(0, 1, 2, 3)]
    
    for face in expansionVolumeFaces:
        expansionVolumeFace.InsertNextCell(mkVtkIdList(face))
        
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
    
def generateCompressionVolumeMapper(compressionVolumeHeight, colorScale):
    compressionVolumePoints = vtkPoints()
    
    compressionVolumeVertices = [(260, 110, 0), (440, 110, 0), (440, compressionVolumeHeight + offsetCenterAxis, 0),
                               (260, compressionVolumeHeight + offsetCenterAxis, 0)]
    
    for point in compressionVolumeVertices:
        compressionVolumePoints.InsertNextPoint(point)
        
    compressionVolumeFace = vtkCellArray()
    compressionVolumeFaces = [(0, 1, 2, 3)]
    
    for face in compressionVolumeFaces:
        compressionVolumeFace.InsertNextCell(mkVtkIdList(face))
        
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

def generateExpansionPistonAnchorMapper(degree):
    expansionPistonAnchorSource = vtkRegularPolygonSource()
    expansionPistonAnchorSource.SetNumberOfSides(50)
    expansionPistonAnchorSource.SetRadius(15.0)
    expansionPistonAnchorSource.SetCenter(calculateHorizontalMovement(degree) + flywheelHorizontalCenter, calculateVerticalMovement(degree) + flywheelVerticalCenter, 0.0)
    
    expansionPistonAnchorMapper = vtkPolyDataMapper2D()
    expansionPistonAnchorMapper.SetInputConnection(expansionPistonAnchorSource.GetOutputPort())
    
    return expansionPistonAnchorMapper

def generateCompressionPistonAnchorMapper(degree):
    # Calculate horizontal movement
    
    compressionPistonAnchorSource = vtkRegularPolygonSource()
    compressionPistonAnchorSource.SetNumberOfSides(50)
    compressionPistonAnchorSource.SetRadius(15.0)
    compressionPistonAnchorSource.SetCenter(- calculateHorizontalMovement(degree) + flywheelHorizontalCenter, - calculateVerticalMovement(degree) + flywheelVerticalCenter, 0.0)
    
    compressionPistonAnchorMapper = vtkPolyDataMapper2D()
    compressionPistonAnchorMapper.SetInputConnection(compressionPistonAnchorSource.GetOutputPort())
    
    return compressionPistonAnchorMapper

if __name__ == '__main__':
    animateStirlingEngine()