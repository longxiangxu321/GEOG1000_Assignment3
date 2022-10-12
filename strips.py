# GEO1000 - Assignment 3
# Authors: Longxiang Xu, Mengying Chen
# Studentnumbers: 5722918

from geometry import Point, Rectangle


class Strip(object):
    def __init__(self, rectangle):
        """Constructor. Inits a Strip instance with a Rectangle describing 
        its shape and an empty points list.
        """
        self.rect = rectangle
        self.points = []


class StripStructure(object):
    def __init__(self, extent, no_strips):
        """Constructor. Inits a StripStructure instance with the correct
        number of Strip instances and makes sure that the domain is 
        correctly divided over the strips.
        """
        self.strips = []
        # Extend this method,
        # so that the right number of strip objects (with the correct extent)
        # are appended to the strips list
        width = (extent[2] - extent[0]) / no_strips

        for i in range(0, no_strips):
            pt_ll = Point((extent[0] + i * width), extent[1])
            pt_ur = Point((extent[0] + (i + 1) * width), extent[3])
            temp = Strip(Rectangle(pt_ll, pt_ur))
            self.strips.append(temp)

    def find_overlapping_strips(self, shape):
        """Returns a list of strip objects for which their rectangle intersects 
        with the shape given.
        
        Returns - list of Strips
        """
        temp = []
        for strip in self.strips:
            if strip.rect.intersects(shape):
                temp.append(strip)
            # breakpoint()
        return temp

    def query(self, shape):
        """Returns a list of points that overlaps the given shape.
        
        For this it first finds the strips that overlap the shape,
        using the find_overlapping_strips method.

        Then, all points of the selected strips are checked for intersection
        with the query shape.
        
        Returns - list of Points
        """
        overlapping_strips = self.find_overlapping_strips(shape)
        overlapping_points = []

        for strip in overlapping_strips:
            for point in strip.points:
                if point.intersects(shape):
                    overlapping_points.append(point)
        return overlapping_points

    def append_point(self, pt):
        """Appends a point object to the list of points of the correct strip
        (i.e. the strip the Point intersects).

        For this it first finds the strips that overlap the point,
        using the find_overlapping_strips method.

        In case multiple strips overlap the point, the point is added
        to the strip with the left most coordinate.
        
        Returns - None
        """

        for i in range(0, len(self.strips)):
            if pt.intersects(self.strips[i].rect):
                self.strips[i].points.append(pt)
                break


    def print_strip_statistics(self):
        """Prints:
        * how many strips there are in the structure

        And then, for all the strips in the structure:
        * an id (starting at 1),
        * the number of points in a strip, 
        * the lower left point of a strip and 
        * the upper right point of a strip.
        
        Returns - None
        """
        print("{} strips".format(len(self.strips)))
        for strip in self.strips:
            print("#{} with {} points, ll: POINT ({} {}), ur: POINT ({} {})".format(
                self.strips.index(strip),
                len(strip.points),
                strip.rect.ll.x,
                strip.rect.ll.y,
                strip.rect.ur.x,
                strip.rect.ur.y
            ))

    def dumps_strips(self):
        """Dumps the strips of this structure to a str, 
        which (if saved in a text file) can be loaded as 
        delimited text layer in QGIS.
        
        Returns - str
        """
        lines = "strip;wkt\n"
        for i, strip in enumerate(self.strips, start=1):
            t = "{0};{1}\n".format(i, strip.rect)
            lines += t
        return lines

    def dumps_points(self):
        """Dumps the points of this structure to a str, 
        which (if saved in a text file) can be loaded as 
        delimited text layer in QGIS.
        
        Returns - str
        """
        lines = "strip;wkt\n"
        for i, strip in enumerate(self.strips, start=1):
            for pt in strip.points:
                t = "{0};{1}\n".format(i, pt)
                lines += t
        return lines
