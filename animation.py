#!/usr/bin/env python

"""
This is (almost) a direct C++ to Python transliteration of
 <VTK-root>/Examples/DataManipulation/Cxx/Cube.cxx from the VTK
 source distribution, which "shows how to manually create vtkPolyData"

A convenience function, mkVtkIdList(), has been added and one if/else
 so the example also works in version 6 or later.
If your VTK version is 5.x then remove the line: colors = vtkNamedColors()
 and replace the set background parameters with (1.0, 0.9688, 0.8594)

"""

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIdList,
    vtkPoints
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def mkVtkIdList(it):
    """
    Makes a vtkIdList from a Python iterable. I'm kinda surprised that
     this is necessary, since I assumed that this kind of thing would
     have been built into the wrapper and happen transparently, but it
     seems not.

    :param it: A python iterable.
    :return: A vtkIdList
    """
    vil = vtkIdList()
    for i in it:
        vil.InsertNextId(int(i))
    return vil


def animation():
    colors = vtkNamedColors()

    # x = array of 8 3-tuples of float representing the vertices of a cube:
    bottomPlateVertices = [(0.0, 0.0, 0.0), (50.0, 0.0, 0.0), (50.0, 50.0, 0.0), (0.0, 50.0, 0.0),
         (0.0, 0.0, 1.0), (50.0, 0.0, 1.0), (50.0, 50.0, 1.0), (0.0, 50.0, 1.0)]

    # pts = array of 6 4-tuples of vtkIdType (int) representing the faces
    #     of the cube in terms of the above vertices
    bottomPlateFaces = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4),
           (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    
    leftPlateVertices = [(0.0, 0.0, 1.0), (50.0, 0.0, 1.0), (50.0, 1.0, 1.0), (0.0, 1.0, 1.0),
                         (0.0, 0.0, 50.0), (50.0, 0.0, 50.0), (50.0, 1.0, 50.0), (0.0, 1.0, 50.0)]
    
    leftPlateFaces = [(0, 4, 7, 3)]

    # We'll create the building blocks of polydata including data attributes.
    bottomPlate = vtkPolyData()
    bottomPlatePoints = vtkPoints()
    bottomPlatePolys = vtkCellArray()
    bottomPlateScalars = vtkFloatArray()
    
    # We'll create the building blocks of polydata including data attributes.
    leftPlate = vtkPolyData()
    leftPlatePoints = vtkPoints()
    leftPlatePolys = vtkCellArray()
    leftPlateScalars = vtkFloatArray()

    # Load the point, cell, and data attributes.
    for i, xi in enumerate(bottomPlateVertices):
        bottomPlatePoints.InsertPoint(i, xi)
    for pt in bottomPlateFaces:
        bottomPlatePolys.InsertNextCell(mkVtkIdList(pt))
    for i, _ in enumerate(bottomPlateVertices):
        bottomPlateScalars.InsertTuple1(i, i)

    # We now assign the pieces to the vtkPolyData.
    bottomPlate.SetPoints(bottomPlatePoints)
    bottomPlate.SetPolys(bottomPlatePolys)
    bottomPlate.GetPointData().SetScalars(bottomPlateScalars)

    # Now we'll look at it.
    bottomPlateMapper = vtkPolyDataMapper()
    bottomPlateMapper.SetInputData(bottomPlate)
    bottomPlateMapper.SetScalarRange(bottomPlate.GetScalarRange())
    bottomPlateActor = vtkActor()
    bottomPlateActor.SetMapper(bottomPlateMapper)
    
    # Load the point, cell, and data attributes.
    for i, xi in enumerate(leftPlateVertices):
        leftPlatePoints.InsertPoint(i, xi)
    for pt in leftPlateFaces:
        leftPlatePolys.InsertNextCell(mkVtkIdList(pt))
    for i, _ in enumerate(leftPlateVertices):
        leftPlateScalars.InsertTuple1(i, i)

    # We now assign the pieces to the vtkPolyData.
    leftPlate.SetPoints(leftPlatePoints)
    leftPlate.SetPolys(leftPlatePolys)
    leftPlate.GetPointData().SetScalars(leftPlateScalars)

    # Now we'll look at it.
    leftPlateMapper = vtkPolyDataMapper()
    leftPlateMapper.SetInputData(leftPlate)
    leftPlateMapper.SetScalarRange(leftPlate.GetScalarRange())
    leftPlateActor = vtkActor()
    leftPlateActor.SetMapper(leftPlateMapper)

    # The usual rendering stuff.
    camera = vtkCamera()
    camera.SetPosition(1, 1, 1)
    camera.SetFocalPoint(0, 0, 0)

    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    renderer.AddActor(bottomPlateActor)
    renderer.AddActor(leftPlateActor)
    renderer.SetActiveCamera(camera)
    renderer.ResetCamera()
    renderer.SetBackground(colors.GetColor3d("Cornsilk"))

    renWin.SetSize(600, 600)
    renWin.SetWindowName("Stirling engine")

    # interact with data
    renWin.Render()
    iren.Start()


if __name__ == "__main__":
    animation()