# mesh.py
# Rutu Patel
# rpatel53@stu.parkland.edu
# CSC 220, Spring 2017

from positional_list import PositionalList

class Mesh:
    '''A polygonal mesh class. Contains a Python list of vertex tuples and
    a positional list of faces that are themselves Python lists.
    '''
    def __init__(self):
        self.__verts = list()
        self.__faces = PositionalList()
        self.__polygon_types = list() # RP: shape of polygon or the name of n-gon
        self.__numberOfVertices = 0 # RP: total number of vertices
        self.__totalPolygons = 0 # RP: total number of faces
        self.__polygons = dict() # RP: count of each type of faces, 3 squares, 5 pentagons etc
        self.__x_minimum = 0 # RP: minimum of x co-ordinates
        self.__y_minimum = 0 # RP: minimum of y co-ordinates
        self.__z_minimum = 0 # RP: minimum of z co-ordinates
        self.__x_maximum = 0 # RP: maximim of x co-ordinates
        self.__y_maximum = 0 # RP: maximim of y co-ordinates
        self.__z_maximum = 0 # RP: maximim of z co-ordinates

    def loadOBJ(self, f):
        '''Loads data from an OBJ file and stores it in the __verts and __faces
        data members. Also calculates the X,Y,Z bounds and the counts of
        face's index sizes.
        '''
        with open(f, 'r') as infile:
            text = infile.read()
            lines = text.split('\n')
            for line_number, line_value in enumerate(lines):
                if line_value is not '':
                    elements = line_value.split()
                    if elements[0] == 'v':
                        self.__verts += [(float(elements[1]),float(elements[2]),float(elements[3]))]
                        self.__numberOfVertices += 1
                    if elements[0] == 'f':
                        face = list()
                        for vertex_index in elements[1:]:
                            face.append(int(vertex_index))
                        self.__faces.add_last(face) # RP: ist of vertex indexs, face
                        # RP: In len(face) if-statement, counting the number of each type of polygon, if len(face)=3 or
                        # RP: say triangle already exist, add one to it, else start count from 1
                        if len(face) in self.__polygon_types:
                            # RP: self.__polygons is the dictionary of total number of each polygons
                            self.__polygons[len(face)] += 1
                        else:
                            self.__polygon_types.append(len(face))
                            self.__polygons[len(face)] = 1
                        # RP: Adding all types of polygon all in the total polygons
                        self.__totalPolygons += 1

    def get_stats(self):
        '''Gets the stats of the Mesh data:
           - the total number of vertices
           - the total number of polygons
           - the number of polygons of each number of sides
           - the mininum and maximum X, Y, and Z coordinates for
             the entire mesh
        '''
        # MVM: Hint for the total number of polys of each number of
        # of sides, use a dictionary.

        # RP: Made a list of x,y and z elements/coordinates, to get minimum and maximum of each co-ordinates individually

        x_elements = list()
        y_elements = list()
        z_elements = list()

        for vertex in self.__verts:
            x_elements.append(vertex[0])
            y_elements.append(vertex[1])
            z_elements.append(vertex[2])

        self.__x_minimum = min(x_elements)
        self.__y_minimum = min(y_elements)
        self.__z_minimum = min(z_elements)

        self.__x_maximum = max(x_elements)
        self.__y_maximum = max(y_elements)
        self.__z_maximum = max(z_elements)

        stats = {"totalVertices": self.__numberOfVertices, "totalPolygon" : self.__totalPolygons,
                 "numberOfPolygons" : self.__polygons, "minimumXCoordinates" : self.__x_minimum ,
                 "minimumYCoordinates" : self.__y_minimum , "minimumZCoordinates" : self.__z_minimum ,
                 "maximumXCoordinates" : self.__x_maximum , "maximumYCoordinates" : self.__y_maximum ,
                 "maximumZCoordinates" : self.__z_maximum}

        return stats

    def writeVTK(self,outfile):
        '''Writes a VTK legacy ASCII format file from data stored in __verts
        and __faces.
        '''
        with open(outfile, 'w') as outfile:
            # RP: First part of vtk file, uptil vertices
            outfile.write('# vtk DataFile Version 3.0\n')
            outfile.write('An object\n')
            outfile.write('ASCII\n')
            outfile.write('DATASET POLYDATA\n')
            outfile.write('POINTS ' + str(self.__numberOfVertices) + ' float\n')
            for vertex in self.__verts:
                outfile.write(str(vertex[0]) + ' ' + str(vertex[1]) + ' ' + str(vertex[2]) + '\n')
            outfile.write('\n')

            # RP: As in the dictionary {key:value}, typeOfPolygon(tri/4/penta...gon) is the key and numberOfThosePolygon
            # is the value, which together is used to calculate total points for vtk file.
            total_points = 0
            for typeOfPolygon, numberOfThosePolygon in self.__polygons.items():
                total_points += (typeOfPolygon+1) * numberOfThosePolygon

            outfile.write('POLYGONS ' + str(self.__totalPolygons) + ' ' + str(total_points) + '\n')

            for face in self.__faces:
                outfile.write(str(len(face)) + ' ')
                for vertex_index in face:
                    outfile.write(str(vertex_index -1) + ' ')
                outfile.write('\n')

    def triangularize(self):
        '''Triangularizes any non-triangles in the face list. It modifes
        the list be replacing non-triangles with two or more triangles. The
        modifcation occurs at the site of the non-triangle.'''

        # RP: Because in Triangulation, we only need to print number of triangles
        if 3 not in self.__polygon_types:
            self.__polygons[3] = 0
            self.__polygon_types.append(3)
        pos = self.__faces.first() # RP: setting position of the first list in the PositionalList(self.__faces)
        while pos is not None: # RP: will do one face at a time
            face = pos.element() # RP: accessing the elements in that position of the list calling it face
            if len(face)>3:
                for n in range(2,len(face)-1): # RP: if face is [1 2 3 4] say in square
                    triangle = list()
                    triangle.append(face[0]) # RP: here goes, face[0]=1
                    triangle.extend(face[n:n+2]) # RP: here goes a slice of face[2:4], which is 3,4, and is
                    # extended to previous one, making it [1 3 4] face as triangle
                    self.__faces.add_before(pos,triangle) # RP: Now adding that face [1 3 4] before [1 2 3], similarly all the
                    # triangle face is added before the place where it is cut
                    self.__polygons[3] += 1
                    self.__totalPolygons += 1
                self.__faces.replace(pos,face[0:3]) # RP: Slice of face [1 2 3]
                self.__polygons[3] += 1
            pos = self.__faces.after(pos) # RP: Giving the position to the next one
        new_polygons = {3:self.__polygons[3]}
        self.__polygons = new_polygons

    def __repr__(self):
        '''Print user-friendly representation of the Mesh object.'''
        # MVM: have this call get_stats()

        output = 'This is a 3D object which consists of {} type(s) of polygon(s).\n'.format(len(self.__polygons))
        output += 'Polygon stats:\n'
        try:
            output += '\tTotal Vertices:{0:>16}\n'.format(self.get_stats()['totalVertices'])
            output += '\tTotal Polygons:{0:>16}\n'.format(self.get_stats()['totalPolygon'])
            for key,values in self.get_stats()['numberOfPolygons'].items():
                output += '\tTotal {0} sided polygon:{1:>9}\n'.format(key,values)
            output += '\tMinimum x coordinate:{0:>10.2f}\n'.format(self.get_stats()['minimumXCoordinates'])
            output += '\tMaximum x coordinate:{0:>10.2f}\n'.format(self.get_stats()['maximumXCoordinates'])
            output += '\tMinimum y coordinate:{0:>10.2f}\n'.format(self.get_stats()['minimumYCoordinates'])
            output += '\tMaximum y coordinate:{0:>10.2f}\n'.format(self.get_stats()['maximumYCoordinates'])
            output += '\tMinimum z coordinate:{0:>10.2f}\n'.format(self.get_stats()['minimumZCoordinates'])
            output += '\tMaximum z coordinate:{0:>10.2f}\n'.format(self.get_stats()['maximumZCoordinates'])
        except:
            output += 'NO DATA\n'
        return output

if __name__ == '__main__':
    print('Mesh class file does not contain tests.')