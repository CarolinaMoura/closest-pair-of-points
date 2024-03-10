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


def solve_closest_distance_nlog_divide_conquer(points: List[Point], inf: float = 1000000) -> dict:
    points.sort()
    for ix, pt in enumerate(points):
        pt.id = ix
    points_sorted_by_y = sorted(points, key=lambda x: x.y)
    points.sort()
    comparison_lines = []

    def divide_and_conquer(points: List[Point], by_y: List[Point]) -> float:
        if len(points) <= 1:
            return inf
        mid = len(points) // 2
        mid_x = points[mid].id
    
        dist_left = divide_and_conquer(points[:mid], [pt for pt in by_y if pt.id <= mid_x])
        dist_right = divide_and_conquer(points[mid:], [pt for pt in by_y if pt.id > mid_x])
        closest_distance = min(dist_left, dist_right)

        within_distance = [pt for pt in by_y if abs(pt.x - points[mid].x) < closest_distance]
        
        for ix,pt in enumerate(within_distance):
            ptr = ix+1
            while ptr < len(within_distance):
                if within_distance[ptr].y - pt.y >= closest_distance:
                    break
                comparison_lines.append((closest_distance, \
                                            (pt.x, pt.y, within_distance[ptr].x, within_distance[ptr].y)))
                if pt.distance(within_distance[ptr]) < closest_distance:
                    closest_distance = pt.distance(within_distance[ptr])
                    comparison_lines.append((closest_distance, \
                                            (pt.x, pt.y, within_distance[ptr].x, within_distance[ptr].y)))
                ptr += 1
        return closest_distance
    
    dist = divide_and_conquer(points, points_sorted_by_y)
    return {
        "min_distance": dist,
        "comparison_lines": comparison_lines,
    }



def solve_closest_distance_nlog_line_sweep(points: List[Point], inf: float = 1000000) -> dict:
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