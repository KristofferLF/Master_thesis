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
    
    centerCylinderAxis = 100
    centerPistonAxis = 225
    
    cylinderPoints = vtkPoints()
    displacerPoints = vtkPoints()
    pistonPoints = vtkPoints()
    cylinderCompressionPoints = vtkPoints()
    cylinderExpansionPoints = vtkPoints()
    pistonCompressionPoints = vtkPoints()
    pistonExpansionPoints = vtkPoints()
    
    cylinderVertices = [(0, 0, 0), (300, 0, 0), (0, 10, 0),             # 0, 1, 2
                (300, 10, 0), (0, 200, 0), (10, 200, 0),                # 3, 4, 5
                (10, 0, 0), (290, 0, 0), (300, 200, 0),                 # 6, 7, 8
                (290, 200, 0), (140, 200, 0), (140, 210, 0),            # 9, 10, 11
                (0, 210, 0), (160, 200, 0), (190, 200, 0),              # 12, 13, 14
                (190, 210, 0), (160, 210, 0), (280, 200, 0),            # 15, 16, 17
                (300, 210, 0), (280, 210, 0), (200, 200, 0),            # 18, 19, 20
                (200, 250, 0), (190, 250, 0), (270, 200, 0),            # 21, 22, 23
                (280, 250, 0), (270, 250, 0), (130, 200, 0),            # 24, 25, 26
                (140, 225, 0), (130, 225, 0), (170, 200, 0),            # 27, 28, 29
                (170, 225, 0), (160, 225, 0)]                           # 30, 31
    
    displacerVertices = [(10, centerCylinderAxis - 25, 0), (290, centerCylinderAxis - 25, 0), (290, centerCylinderAxis + 25, 0),    # 0, 1, 2
                         (10, centerCylinderAxis + 25, 0), (140, centerCylinderAxis + 25, 0), (160, centerCylinderAxis + 25, 0),    # 3, 4, 5
                         (160, centerCylinderAxis + 175, 0), (140, centerCylinderAxis + 175, 0)]                                    # 6, 7
    
    pistonVertices = [(200, centerPistonAxis - 7.5, 0), (270, centerPistonAxis - 7.5, 0), (270, centerPistonAxis + 7.5, 0),     # 0, 1, 2
                    (200, centerPistonAxis + 7.5, 0), (232.5, centerPistonAxis + 7.5, 0), (237.5, centerPistonAxis + 7.5, 0),   # 3, 4, 5
                    (237.5, centerPistonAxis + 50, 0), (232.5, centerPistonAxis + 50, 0)]                                       # 6, 7
    
    for point in cylinderVertices:
        cylinderPoints.InsertNextPoint(point)
        
    for point in displacerVertices:
        displacerPoints.InsertNextPoint(point)
        
    for point in pistonVertices:
        pistonPoints.InsertNextPoint(point)

    cylinderFace = vtkCellArray()
    displacerFace = vtkCellArray()
    pistonFace = vtkCellArray()
    
    cylinderFaces = [(0, 1, 3, 2), (0, 6, 5, 4), (7, 1, 8, 9),
           (4, 10, 11, 12), (13, 14, 15, 16), (17, 8, 18, 19),
           (14, 20, 21, 22), (23, 17, 24, 25), (26, 10, 27, 28),
           (13, 29, 30, 31)]
    
    displacerFaces = [(0, 1, 2, 3), (4, 5, 6, 7)]
    
    pistonFaces = [(0, 1, 2, 3), (4, 5, 6, 7)]
    
    for pt in cylinderFaces:
        cylinderFace.InsertNextCell(mkVtkIdList(pt))
        
    for pt in displacerFaces:
        displacerFace.InsertNextCell(mkVtkIdList(pt))
        
    for pt in pistonFaces:
        pistonFace.InsertNextCell(mkVtkIdList(pt))

    cylinderPolydata = vtkPolyData()
    cylinderPolydata.SetPoints(cylinderPoints)
    cylinderPolydata.SetPolys(cylinderFace)
    
    displacerPolydata = vtkPolyData()
    displacerPolydata.SetPoints(displacerPoints)
    displacerPolydata.SetPolys(displacerFace)
    
    pistonPolydata = vtkPolyData()
    pistonPolydata.SetPoints(pistonPoints)
    pistonPolydata.SetPolys(pistonFace)

    # CHANGE FROM GLYPHFILTER
    glyphFilter = vtkVertexGlyphFilter()
    glyphFilter.SetInputData(cylinderPolydata)
    glyphFilter.Update()

    cylinderMapper = vtkPolyDataMapper2D()
    cylinderMapper.SetInputData(cylinderPolydata)
    cylinderMapper.Update()
    
    displacerMapper = vtkPolyDataMapper2D()
    displacerMapper.SetInputData(displacerPolydata)
    displacerMapper.Update()
    
    pistonMapper = vtkPolyDataMapper2D()
    pistonMapper.SetInputData(pistonPolydata)
    pistonMapper.Update()

    cylinderActor = vtkActor2D()
    cylinderActor.SetMapper(cylinderMapper)
    cylinderActor.GetProperty().SetColor(colors.GetColor3d('Grey'))
    cylinderActor.GetProperty().SetPointSize(8)
    
    displacerActor = vtkActor2D()
    displacerActor.SetMapper(displacerMapper)
    displacerActor.GetProperty().SetColor(colors.GetColor3d('SlateGray'))
    displacerActor.GetProperty().SetPointSize(8)
    
    pistonActor = vtkActor2D()
    pistonActor.SetMapper(pistonMapper)
    pistonActor.GetProperty().SetColor(colors.GetColor3d('SlateGray'))
    pistonActor.GetProperty().SetPointSize(8)

    # Create a renderer, render window, and interactor
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Add the actor to the scene
    renderer.AddActor(cylinderActor)
    renderer.AddActor(displacerActor)
    renderer.AddActor(pistonActor)
    renderWindow.SetSize(300, 400)
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