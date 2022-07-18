from cmath import nan
import numpy as np 
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import random


class Point:

    def __init__(self, x, y):
        self.x  = x
        self.y  = y
        

class Triangle:

    def __init__(self, p1, p2, p3):
        self.p1  = p1
        self.p2  = p2
        self.p3  = p3

    def perimeter(self):
        per =  length(self.p1,self.p2) + length(self.p2,self.p3) + length(self.p3,self.p1)
        if per == nan:
            return 0

        return per

    def print_points(self):
        print("***************************")
        print("p1 = ({},{})".format(self.p1.x,self.p1.y))
        print("p2 = ({},{})".format(self.p2.x,self.p2.y))
        print("p3 = ({},{})".format(self.p3.x,self.p3.y))
        print("perimeter = ", self.perimeter() )
        print("***************************")
        
    def draw_diagonals(self):

        dist1 = length(self.p1, self.p2)
        dist2 = length(self.p1, self.p3)
        dist3 = length(self.p2, self.p3)

        if dist1 > 0 and dist2 > 0 and dist3 > 0:

            if max(dist1,dist2,dist3) == dist1:
                plt.plot([self.p1.x, self.p2.x],[ self.p1.y, self.p2.y], "go--")

            if max(dist1,dist2,dist3) == dist2:
                plt.plot([self.p1.x, self.p3.x],[ self.p1.y, self.p3.y], "go--")

            if max(dist1,dist2,dist3) == dist3:
                plt.plot([self.p2.x, self.p3.x],[ self.p2.y, self.p3.y], "go--")




class Triangle_Group:

    def __init__(self, triangles):
        self.triangles = triangles
    
    def perimeter(self):
        per = 0
        for t in self.triangles:
            per += t.perimeter()
        return per 

    def add_triangle(self, t):
        self.triangles.append(t)

    def draw_diagonals(self):
        for t in self.triangles:
            t.draw_diagonals()

def length(p1, p2):
    return  np.sqrt((np.square(p2.x - p1.x) + (np.square(p2.y - p1.y) )))



def find_triangulation(points, num_points):

    print(num_points)

    if(num_points < 3):
        return 0

    triangles =[ [ None for y in range( num_points ) ]
            for x in range( num_points) ]

    for p in range(num_points):
        i = 0
        for j in range(p, num_points ):

            all_opt_ts = Triangle_Group([])

            if(j < i + 2):
                triangles[i][j] = Triangle(Point(0,0),Point(0,0),Point(0,0))

            else:
                triangles[i][j] = Triangle(Point(1000,1000),Point(100000,10000),Point(1000,10000))

                for k  in range(i+1, j):
                    
                    t = Triangle(points[i], points[j], points[k])

                    val = triangles[i][k].perimeter() + triangles[k][j].perimeter() + t.perimeter()

                    if(triangles[i][j].perimeter() >= val):
                        all_opt_ts.add_triangle(Triangle_Group([triangles[i][k], triangles[k][j], t]) )
                        triangles[i][j] = Triangle_Group([triangles[i][k], triangles[k][j], t]) 

            i+=1

    return triangles, all_opt_ts


def main():

    p1 = Point(6,0)
    p2 = Point(3, 3 * np.sqrt(3))
    p3 = Point(-3, 3 * np.sqrt(3))
    p4 = Point(-6,0)
    p5 = Point(-3, -3 * np.sqrt(3))
    p6 = Point(3, -3 * np.sqrt(3))


    points = [p1, p2, p3, p4, p5, p6]

    poly = Polygon([(p1.x, p1.y),
        (p2.x, p2.y),
        (p3.x, p3.y),
        (p4.x, p4.y),
        (p5.x, p5.y),
        (p6.x, p6.y)])

    x, y = poly.exterior.xy
    plt.plot(x, y, c="red")

    ts, tt = find_triangulation(points,6)

    tt.draw_diagonals()

    plt.show()

main()        