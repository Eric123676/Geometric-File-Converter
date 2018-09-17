# project2.py driver file
# Mark Van Moer
# mvanmoer@parkland.edu
# CSC 220, Spring 2017

import sys
from mesh import Mesh

def testMesh(objfile):
    basename = objfile[:-4]
    meshdata = Mesh()
    meshdata.loadOBJ(objfile)
   
    print('-'*80)
    print('Original stats:')
    print(meshdata)

    meshdata.writeVTK(basename + '.vtk')
    
    meshdata.triangularize()

    print('-'*80)
    print('Triangularized stats:')
    print(meshdata)

    meshdata.writeVTK(basename + '-triangularized.vtk')

if __name__ == '__main__':
    try:
        testMesh(sys.argv[1]) 
    except NotImplementedError:
        print('Some method still needs to be implemented!')
    except Exception as e:
        print(e.args)
