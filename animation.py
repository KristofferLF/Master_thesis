#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkPolyData, vtkCellArray
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

def mkVtkIdList(it):
    """
    :param it: A python iterable.
    :return: A vtkIdList
    """
    vil = vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil

def main():
    colors = vtkNamedColors()
    
    centerAxisLeft = 200
    centerAxisRight = 200
    
    cylinderPoints = vtkPoints()
    leftDisplacerPoints = vtkPoints()
    rightDisplacerPoints = vtkPoints()
    expansionVolumePoints = vtkPoints()
    compressionVolumePoints = vtkPoints()
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
    
    leftDisplacerVertices = [(10, centerAxisLeft - 15, 1), (190, centerAxisLeft - 15, 1), (190, centerAxisLeft + 15, 1),        # 0, 1, 2
                         (10, centerAxisLeft + 15, 1), (90, centerAxisLeft + 15, 1), (110, centerAxisLeft + 15, 1),             # 3, 4, 5
                         (110, centerAxisLeft + 175, 1), (90, centerAxisLeft + 175, 1)]                                         # 6, 7
    
    rightDisplacerVertices = [(260, centerAxisRight - 15, 0), (440, centerAxisRight - 15, 0), (440, centerAxisRight + 15, 0),   # 0, 1, 2
                              (260, centerAxisRight + 15, 0), (340, centerAxisRight + 15, 0), (360, centerAxisRight + 15, 0),   # 3, 4, 5
                              (360, centerAxisRight + 175, 0), (340, centerAxisRight + 175, 0)]                                 # 6, 7
    
    expansionVolumeVertices = [(10, 110, 0), (190, 110, 0), (190, centerAxisLeft - 15, 0),      # 0, 1, 2
                               (10, centerAxisLeft - 15, 0)]                                    # 3
    
    compressionVolumeVertices = [(260, 110, 0), (440, 110, 0), (440, centerAxisRight - 15, 0),  # 0, 1, 2
                               (260, centerAxisRight - 15, 0)]                                  # 3
    
    regeneratorVertices = [(150, 40, 0), (300, 40, 0), (300, 80, 0),    # 0, 1, 2
                           (150, 80, 0), (190, 80, 0), (190, 110, 0),   # 3, 4, 5
                           (150, 110, 0), (260, 80, 0), (300, 110, 0),  # 6, 7, 8
                           (260, 110, 0)]
    
    for point in cylinderVertices:
        cylinderPoints.InsertNextPoint(point)
        
    for point in leftDisplacerVertices:
        leftDisplacerPoints.InsertNextPoint(point)
        
    for point in rightDisplacerVertices:
        rightDisplacerPoints.InsertNextPoint(point)
        
    for point in expansionVolumeVertices:
        expansionVolumePoints.InsertNextPoint(point)
        
    for point in compressionVolumeVertices:
        compressionVolumePoints.InsertNextPoint(point)
        
    for point in regeneratorVertices:
        regeneratorPoints.InsertNextPoint(point)

    cylinderFace = vtkCellArray()
    leftDisplacerFace = vtkCellArray()
    rightDisplacerFace = vtkCellArray()
    expansionVolumeFace = vtkCellArray()
    compressionVolumeFace = vtkCellArray()
    regeneratorFace = vtkCellArray()
    
    cylinderFaces = [(0, 1, 2, 3), (0, 4, 5, 6), (7, 22, 8, 9),
                     (6, 10, 11, 12), (13, 8, 14, 15), (16, 11, 17, 18),
                     (15, 19, 20, 21), (24, 25, 1, 23), (26, 27, 28, 24),
                     (7, 29, 30, 31), (32, 29, 33, 34), (27, 35, 36, 37),
                     (37, 38, 39, 40), (41, 38, 42, 43), (34, 44, 45, 46),
                     (47, 42, 48, 49), (50, 44, 51, 52), (47, 53, 54, 55)]
    
    leftDisplacerFaces = [(0, 1, 2, 3), (4, 5, 6, 7)]
    
    rightDisplacerFaces = [(0, 1, 2, 3), (4, 5, 6, 7)]
    
    expansionVolumeFaces = [(0, 1, 2, 3)]
    
    compressionVolumeFaces = [(0, 1, 2, 3)]
    
    regeneratorFaces = [(0, 1, 2, 3), (3, 4, 5, 6), (7, 2, 8, 9)]
    
    for face in cylinderFaces:
        cylinderFace.InsertNextCell(mkVtkIdList(face))
        
    for face in leftDisplacerFaces:
        leftDisplacerFace.InsertNextCell(mkVtkIdList(face))
        
    for face in rightDisplacerFaces:
        rightDisplacerFace.InsertNextCell(mkVtkIdList(face))
        
    for face in expansionVolumeFaces:
        expansionVolumeFace.InsertNextCell(mkVtkIdList(face))
        
    for face in compressionVolumeFaces:
        compressionVolumeFace.InsertNextCell(mkVtkIdList(face))
        
    for face in regeneratorFaces:
        regeneratorFace.InsertNextCell(mkVtkIdList(face))

    cylinderPolydata = vtkPolyData()
    cylinderPolydata.SetPoints(cylinderPoints)
    cylinderPolydata.SetPolys(cylinderFace)
    
    leftDisplacerPolydata = vtkPolyData()
    leftDisplacerPolydata.SetPoints(leftDisplacerPoints)
    leftDisplacerPolydata.SetPolys(leftDisplacerFace)
    
    rightDisplacerPolydata = vtkPolyData()
    rightDisplacerPolydata.SetPoints(rightDisplacerPoints)
    rightDisplacerPolydata.SetPolys(rightDisplacerFace)
    
    expansionVolumePolydata = vtkPolyData()
    expansionVolumePolydata.SetPoints(expansionVolumePoints)
    expansionVolumePolydata.SetPolys(expansionVolumeFace)
    
    compressionVolumePolydata = vtkPolyData()
    compressionVolumePolydata.SetPoints(compressionVolumePoints)
    compressionVolumePolydata.SetPolys(compressionVolumeFace)
    
    regeneratorPolydata = vtkPolyData()
    regeneratorPolydata.SetPoints(regeneratorPoints)
    regeneratorPolydata.SetPolys(regeneratorFace)

    # CHANGE FROM GLYPHFILTER
    glyphFilter = vtkVertexGlyphFilter()
    glyphFilter.SetInputData(cylinderPolydata)
    glyphFilter.Update()

    cylinderMapper = vtkPolyDataMapper2D()
    cylinderMapper.SetInputData(cylinderPolydata)
    cylinderMapper.Update()
    
    leftDisplacerMapper = vtkPolyDataMapper2D()
    leftDisplacerMapper.SetInputData(leftDisplacerPolydata)
    leftDisplacerMapper.Update()
    
    rightDisplacerMapper = vtkPolyDataMapper2D()
    rightDisplacerMapper.SetInputData(rightDisplacerPolydata)
    rightDisplacerMapper.Update()
    
    expansionVolumeMapper = vtkPolyDataMapper2D()
    expansionVolumeMapper.SetInputData(expansionVolumePolydata)
    expansionVolumeMapper.Update()
    
    compressionVolumeMapper = vtkPolyDataMapper2D()
    compressionVolumeMapper.SetInputData(compressionVolumePolydata)
    compressionVolumeMapper.Update()
    
    regeneratorMapper = vtkPolyDataMapper2D()
    regeneratorMapper.SetInputData(regeneratorPolydata)
    regeneratorMapper.Update()

    cylinderActor = vtkActor2D()
    cylinderActor.SetMapper(cylinderMapper)
    cylinderActor.GetProperty().SetColor(colors.GetColor3d('Grey'))
    cylinderActor.GetProperty().SetPointSize(8)
    
    leftDisplacerActor = vtkActor2D()
    leftDisplacerActor.SetMapper(leftDisplacerMapper)
    leftDisplacerActor.GetProperty().SetColor(colors.GetColor3d('SlateGray'))
    leftDisplacerActor.GetProperty().SetPointSize(8)
    
    rightDisplacerActor = vtkActor2D()
    rightDisplacerActor.SetMapper(rightDisplacerMapper)
    rightDisplacerActor.GetProperty().SetColor(colors.GetColor3d('SlateGray'))
    rightDisplacerActor.GetProperty().SetPointSize(8)
    
    expansionVolumeActor = vtkActor2D()
    expansionVolumeActor.SetMapper(expansionVolumeMapper)
    expansionVolumeActor.GetProperty().SetColor(colors.GetColor3d('Red'))
    expansionVolumeActor.GetProperty().SetPointSize(8)
    
    compressionVolumeActor = vtkActor2D()
    compressionVolumeActor.SetMapper(compressionVolumeMapper)
    compressionVolumeActor.GetProperty().SetColor(colors.GetColor3d('Blue'))
    compressionVolumeActor.GetProperty().SetPointSize(8)
    
    regeneratorActor = vtkActor2D()
    regeneratorActor.SetMapper(regeneratorMapper)
    regeneratorActor.GetProperty().SetColor(colors.GetColor3d('Purple'))
    regeneratorActor.GetProperty().SetPointSize(8)

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(cylinderActor)
    renderer.AddActor(leftDisplacerActor)
    renderer.AddActor(rightDisplacerActor)
    renderer.AddActor(expansionVolumeActor)
    renderer.AddActor(compressionVolumeActor)
    renderer.AddActor(regeneratorActor)
    renderWindow.SetSize(450, 600)
    renderer.SetBackground(colors.GetColor3d('White'))

    renderWindow.SetWindowName('Animation of Stirling Engine')

    # Render and interact
    renderWindow.Render()
    # w2if = vtkWindowToImageFilter()
    # w2if.SetInput(renderWindow)
    # w2if.Update()
    #
    # writer = vtkPNGWriter()
    # writer.SetFileName('TestActor2D.png')
    # writer.SetInputConnection(w2if.GetOutputPort())
    # writer.Write()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()