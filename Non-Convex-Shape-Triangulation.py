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

    def draw_triangle(self):

        plt.plot([self.p1.x, self.p2.x],[ self.p1.y, self.p2.y], "go--")

        plt.plot([self.p2.x, self.p3.x],[ self.p2.y, self.p3.y], "go--")

        plt.plot([self.p3.x, self.p1.x],[ self.p3.y, self.p1.y], "go--")



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


def InTriangle( p,  a,  b, c):

            ab = b - a;
            bc = c - b;
            ca = a - c;

            ap = p - a;
            bp = p - b;
            cp = p - c;

            cross1 = np.cross(ab, ap);
            cross2 = np.cross(bc, bp);
            cross3 = np.cross(ca, cp);


            if cross1 > 0 or cross2 > 0 or  cross3 > 0:
        
                return False

            return True


def triangulate(points, n):

    indices = []

    for i in range(n):
        indices.append(i)


    totalTriangles = n - 2
    totalTriangleIndices = totalTriangles * 3

    triangles = [0 for x in range(totalTriangleIndices)]

    count = 0
    

    while(len(indices) > 3):

        for i in range (len(indices) ):

            a = indices[i]

            if i ==0:
                b = indices[ -1]
            else:
                b = indices[i - 1]

            if i == len(indices):
                c = indices[0]
            else:
                c = indices[i + 1]


            va = points[a]
            vb = points[b]
            vc = points[c]

            vab = vb - va
            vac = vc - va

            if np.cross(vab, vac) >= 0:
                
                isEar = True

                for j in range(n):

                    if j != a and j != b and j != c:

                        p = points[j]

                        if(InTriangle(p,vb,va,vc)):
                            isEar = False
                            break

                if(isEar):
                    t = Triangle(b,a,c)
                    triangles[count] = b;
                    count+=1
                    triangles[count] = a;
                    count+=1
                    triangles[count] = c;
                    count+=1

                    indices.pop(i)
                    break

    triangles[count] = indices[0];
    count+=1
    triangles[count] = indices[1];
    count+=1
    triangles[count] = indices[2];

    return triangles


def main():

    p1 = np.array([3,5.2])
    p2 = np.array([4,3.46])
    p3 = np.array([6.01,3.46])
    p4 = np.array([5.01,1.72])
    p5 = np.array([6,0])
    p6 = np.array([4.02,0])
    p7 = np.array([3.01,-1.74])
    p8 = np.array([2.01,0])
    p9 = np.array([0,0])
    p10 = np.array([1,1.75])
    p11 = np.array([0.01,3.46])
    p12 = np.array([2,3.46])
    
    points = [ p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p1]

    poly = Polygon([
        (p1[0], p1[1]),
        (p2[0], p2[1]),
        (p3[0], p3[1]),
        (p4[0], p4[1]),
        (p5[0], p5[1]),
        (p6[0], p6[1]),
        (p7[0], p7[1]),
        (p8[0], p8[1]),
        (p9[0], p9[1]),
        (p10[0], p10[1]),
        (p11[0], p11[1]),
        (p12[0], p12[1])])



    x, y = poly.exterior.xy
    plt.plot(x, y, c="red")

    ts = triangulate(points, 12)

    print(ts)


    for i in range(0, len(ts), 3):
        p = points[ts[i]]
        p2 = points[ts[i+1]]
        p3 = points[ts[i+2]]

        pp = Point(p[0], p[1])
        pp2 = Point(p2[0], p2[1])
        pp3 = Point(p3[0], p3[1])

        t = Triangle(pp3,pp,pp2)
        t.draw_triangle()

    plt.show()

main()






