from netgen.occ import *
from ngsolve import *


# All lengths are in units of millimeters!!!!

def buildGeometry():

    LArWidth = 300.
    LArHeight = 300.
    driftLength = 300.

    anodeThickness = 5.
    cathodeThickness = 5.
    
    shapeLAr = Box(Pnt(-LArWidth/2, -LArHeight/2, 0),
                   Pnt(LArWidth/2, LArHeight/2, driftLength))
    shapeLAr.name = "LAr"
    shapeAnode = Box(Pnt(-LArWidth/2, -LArHeight/2, -anodeThickness),
                     Pnt(LArWidth/2, LArHeight/2, 0))
    shapeAnode.name = "anode"
    shapeCathode = Box(Pnt(-LArWidth/2, -LArHeight/2, driftLength),
                       Pnt(LArWidth/2, LArHeight/2, driftLength + cathodeThickness))
    shapeCathode.name = "Cathode"
    
    # Input for Glue
    shape = []

    shape.append(shapeLAr)
    shape.append(shapeAnode)
    shape.append(shapeCathode)

    return shape


def mesh(shape, folderName, meshFineness):
    # Meshing
    geo = OCCGeometry(Glue(shape))
    mesh = Mesh(geo.GenerateMesh(maxh=meshFineness))
    mesh.ngmesh.Export(folderName, "Elmer Format")

    # Make solver file (I think this is only necessary when running the elmer GUI)
    solver = open("./" + folderName + "/ELMERSOLVER_STARTINFO", 'w')
    solver.write("case.sif\n1\n")
    solver.close()


def main(args):
    # Builds the geometry and then meshes it
    Shape = buildGeometry()
    mesh(Shape, args.outFolderName, int(args.MeshFineness)) # I had issues when trying to use too coarse of a mesh
    # (30 mm), however, even a 10mm mesh took close to 2 hours to run on our cluster


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description = 'Create ND LAr geometry and export mesh')
    parser.add_argument('-o', '--outFolderName',
                        default = 'singleCube',
                        help = 'output folder name (default: singleCube)')
    # parser.add_argument('StripWidth',
    #                     help = 'Set the width of each strip')
    # parser.add_argument('StripSpacing',
    #                     help = 'Set the spacing between each strip')
    # parser.add_argument('StripNumber',
    #                     help = 'Set the number of strips (on one side of the box)')
    parser.add_argument('MeshFineness',
                        help='Set the fineness of the mesh')
    
    args = parser.parse_args()

    main(args)
