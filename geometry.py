from typing import List
from sortedcontainers import SortedSet

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __lt__(self, other):
        return self.x < other.x

    def distance(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5

    def __repr__(self):
        return f"({self.x}, {self.y})"


def solve_closest_distance_nlog(points: List[Point], inf: float = 1000000) -> dict:
    points.sort()
    s = SortedSet()
    closest_distance = inf
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
                if abs(yy - y) >= closest_distance:
                    break
                comparison_lines.append((closest_distance,(x, y, xx, yy)))
                if pt.distance(Point(xx, yy)) < closest_distance:
                    closest_distance = pt.distance(Point(xx, yy))
                    comparison_lines.append((closest_distance,(x, y, xx, yy)))
                index += delta
        for d in to_delete:
            s.remove(d)
    
    return {
        "min_distance": closest_distance,
        "comparison_lines": comparison_lines,
    }

def solve_closest_distance_quadratic(points: List[Point], inf: float = 1000000) -> dict:
    min_dist = inf 
    comparison_lines = []
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            x1, y1 = points[i].x, points[i].y
            x2, y2 = points[j].x, points[j].y
            dist = (x1-x2)**2 + (y1-y2)**2
            comparison_lines.append((dist, (x1, y1, x2, y2)))
            if dist < min_dist:
                min_dist = dist
    return {
        "min_distance": min_dist**0.5,
        "comparison_lines": comparison_lines,
    }


if __name__ == "__main__":
    pts = [
    Point(354, 236),
    Point(34, 233),
    Point(39, 36),
    Point(336, 47),
    Point(75, 146),
    Point(297, 130),
    Point(181, 138),
    Point(173, 51),
    Point(190, 225),
    Point(253, 187)
]
    print(solve_closest_distance_nlog(pts)["min_distance"])
    print(solve_closest_distance_quadratic(pts)["min_distance"])