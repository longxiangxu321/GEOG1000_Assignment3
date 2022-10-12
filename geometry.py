# GEO1000 - Assignment 3
# Authors: Longxiang Xu, Mengying Chen
# Studentnumbers: 5722918,

import math

# __all__ leaves out _test method and only makes
# the classes available for "from geometry import *":
__all__ = ["Point", "Circle", "Rectangle"] 


class Point(object):

    def __init__(self, x, y):
        """Constructor. 
        Takes the x and y coordinates to define the Point instance.
        """
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        """Returns WKT String "POINT (x y)".
        """
        wkt = "POINT({} {})".format(self.x, self.y)
        return wkt

    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        returns - True / False
        """
        if type(other) == Point:
            if self.distance(other) == 0:
                return True
            else:
                return False
        elif type(other) == Circle:
            if self.distance(other.center) <= other.radius:
                return True
            else:
                return False
        elif type(other) == Rectangle:
            if (other.ll.x <= self.x <= other.ur.x) and (other.ur.y >= self.y >= other.ll.y):
                return True
            else:
                return False

    def distance(self, other):
        """Returns cartesian distance between self and other Point
        """
        dist = math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
        return dist


class Circle(object):

    def __init__(self, center, radius):
        """Constructor. 
        Takes the center point and radius defining the Circle.
        """
        assert float(radius) > 0
        assert isinstance(center, Point)
        self.center = center
        self.radius = float(radius)

    def __str__(self):
        """Returns WKT str, discretizing the boundary of the circle 
        into straight line segments
        """
        N = 400
        step = 2 * math.pi / N
        pts = []
        for i in range(N):
            pts.append(Point(self.center.x + math.cos(i * step) * self.radius, 
                             self.center.y + math.sin(i * step) * self.radius))
        pts.append(pts[0])
        coordinates = ["{0} {1}".format(pt.x, pt.y) for pt in pts]
        coordinates = ", ".join(coordinates)
        return "POLYGON (({0}))".format(coordinates)

    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        Returns - True / False
        """
        if type(other) == Point:
            return other.intersects(self)
        elif type(other) == Circle:
            if self.center.distance(other.center) <= (self.radius + other.radius):
                return True
            else:
                return False
        elif type(other) == Rectangle:
            # draw the outer boundary that are made of the intersecting circles' centers
            new_ll, new_ur = Point(0,0), Point(0,0)
            angle = math.pi / 4
            outer_width = self.radius * math.cos(angle)
            new_ll.x = other.ll.x - outer_width
            new_ll.y = other.ll.y - outer_width
            new_ur.x = other.ur.x + outer_width
            new_ur.y = other.ur.y + outer_width

            new_rectangle = Rectangle(new_ll, new_ur)
            if self.center.intersects(new_rectangle):
                return True
            else:
                return False


class Rectangle(object):

    def __init__(self, pt_ll, pt_ur):
        """Constructor. 
        Takes the lower left and upper right point defining the Rectangle.
        """
        assert isinstance(pt_ll, Point)
        assert isinstance(pt_ur, Point)
        self.ll = pt_ll
        self.ur = pt_ur

    def __str__(self):
        """Returns WKT String "POLYGON ((x0 y0, x1 y1, ..., x0 y0))"
        """
        lr = Point(self.ur.x, self.ll.y)
        ul = Point(self.ll.x, self.ur.y)
        pts = [self.ll, lr, self.ur, ul]
        coordinates = ["{0} {1}".format(pt.x, pt.y) for pt in pts]
        coordinates = ", ".join(coordinates)
        return "POLYGON (({0}))".format(coordinates)


    def intersects(self, other):
        """Checks whether other shape has any interaction with
        interior or boundary of self shape. Uses type based dispatch.
        
        other - Point, Circle or Rectangle
        
        Returns - True / False
        """
        if type(other) == Point or type(other) == Circle:
            return other.intersects(self)
        elif type(other) == Rectangle:
            new_ll = Point(self.ll.x - other.width(), self.ll.y - other.height())
            new_rectangle = Rectangle(new_ll, self.ur)
            return other.ll.intersects(new_rectangle)

    def width(self):
        """Returns the width of the Rectangle.
        
        Returns - float
        """
        return float(math.fabs(self.ll.x - self.ur.x))

    def height(self):
        """Returns the height of the Rectangle.
        
        Returns - float
        """
        return float(math.fabs(self.ll.y - self.ur.y))

def _test():
    """Test whether your implementation of all methods works correctly.
    """
    pt0 = Point(0, 0)
    pt1 = Point(0, 0)
    pt2 = Point(10, 10)
    assert pt0.intersects(pt1)
    assert pt1.intersects(pt0)
    assert not pt0.intersects(pt2)
    assert not pt2.intersects(pt0)

    c = Circle(Point(-1, -1), 1)
    r = Rectangle(Point(0,0), Point(10,10))
    assert not c.intersects(r)

    # Extend this method to be sure that you test all intersects methods!
    # Read Section 16.5 of the book if you have never seen the assert statement


if __name__ == "__main__":
    _test()

