from typing import List
from sortedcontainers import SortedSet

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __lt__(self, other):
        return self.x < other.x

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def __repr__(self):
        return f"({self.x}, {self.y})"


def solve_closest_distance_nlog(points: List[Point]):
    points.sort()
    s = SortedSet()
    closest_distance = 1000000
    comparison_lines = []

    for ix, pt in enumerate(points):
        x, y = pt.x, pt.y
        s.add((pt.y, pt.x, ix))
        to_delete = []

        for delta in [-1, 1]:
            index = s.index((y, x, ix)) + delta
            while index < len(s) and index >= 0:
                yy, xx, ii = s[index]
                if x - xx >= closest_distance:
                    to_delete.append((yy, xx, ii))
                    break
                if abs(yy - y) >= closest_distance:
                    break
                comparison_lines.append((closest_distance,(x, y, xx, yy)))
                if pt.distance(Point(xx, yy)) < closest_distance:
                    closest_distance = pt.distance(Point(xx, yy))
                    comparison_lines.append((closest_distance,(x, y, xx, yy)))
                index += delta
        for d in to_delete:
            s.remove(d)
    
    return comparison_lines
