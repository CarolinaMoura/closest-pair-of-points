import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QLineF
from PyQt5.QtCore import QTimer
from geometry import (
    Point,
    solve_closest_distance_nlog_line_sweep,
    solve_closest_distance_nlog_divide_conquer,
    solve_closest_distance_quadratic,
)

inf = 1000000


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Click to Add Points"
        self.ini_top = 100
        self.ini_left = 100
        self.ini_width = 400
        self.ini_height = 300
        self.shortestLine = None  # To store the shortest line found
        self.comparison_lines = []
        self.distance = 1000000
        self.points = []  # Store the points
        self.submitClicked = False  # Flag to track if submit has been clicked
        self.timer = QTimer(self)  # Create a QTimer instance
        self.timer.timeout.connect(
            self.performComparison
        )  # Connect the timer to the comparison method
        self.distanceLabel = None
        self.dashed_line = None
        self.initWindow()

    def center_horizontally(self, width, height, obj):
        obj.resize(
            min(width - 20, obj.width()), obj.height()
        )  # Optionally resize the label if needed
        obj_width = obj.width()
        obj.move((width - obj_width) // 2, round(height) - 50)

    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        self.center_horizontally(width, height, self.button)
        if self.distanceLabel is not None:
            self.center_horizontally(width, height, self.distanceLabel)

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.ini_top, self.ini_left, self.ini_width, self.ini_height)

        # Create and position the submit button
        self.button = QPushButton("Submit", self)
        self.button.move(150, 260)  # Position the button
        self.button.clicked.connect(
            self.onSubmitClick
        )  # Connect button click to function

        self.show()

    def onSubmitClick(self):
        # Hide the submit button
        self.button.hide()
        self.submitClicked = True  # Set the flag to True when submit is clicked

        # Create a label to show the distance, starting with a default value
        self.distance = inf
        self.distanceLabel = QLabel(f"Best current distance: {self.distance}", self)
        self.distanceLabel.resize(
            self.width() - 20, 30
        )  # Optionally resize the label if needed
        self.center_horizontally(self.width(), self.height(), self.distanceLabel)
        self.distanceLabel.show()
        self.quadratic()
        self.solve_closest_distance()
        self.timer.start(300)

    def quadratic(self):
        pts = [Point(event.x(), event.y()) for event in self.points]
        reply = solve_closest_distance_quadratic(pts, self.distance)
        print(f"quadratic: {reply['min_distance']}")

    def mousePressEvent(self, event):
        if self.submitClicked:
            return
        self.points.append(event.pos())
        print(event.pos())
        print(f"Point added at: ({event.x()}, {event.y()})")
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        for point in self.points:
            painter.drawPoint(point)

        if self.dashed_line != None:
            painter.setPen(QPen(Qt.black, 2, Qt.DashLine))
            painter.drawLine(
                QLineF(self.dashed_line, 0, self.dashed_line, self.height())
            )

        if self.shortestLine:
            dist, line = self.shortestLine
            if self.dashed_line != None:
                painter.setBrush(
                QBrush(QColor(100, 100, 200, 51))
                )  # RGBA: Blue with 80% transparency
                painter.setPen(
                    QColor(50, 50, 50, 51)
                )  # RGBA: Gray pen with 80% transparency (for the rectangle's border)
                painter.drawRect(
                    self.dashed_line - round(min(dist, self.distance)),
                    0,
                    2*round(min(dist, self.distance)),
                    self.height(),
                )
            pen_color = Qt.green if dist < self.distance else Qt.gray
            if dist < self.distance:
                self.distance = dist
            self.distanceLabel.setText(f"Best current distance: {self.distance}")
            painter.setPen(QPen(pen_color, 2, Qt.SolidLine))
            painter.drawLine(line)

    def performComparison(self):
        # Method to perform a single comparison from the list of tasks
        if not self.comparison_lines:
            self.timer.stop()  # Stop the timer if there are no more tasks
            return

        if isinstance(self.comparison_lines[0], float) or isinstance(
            self.comparison_lines[0], int
        ):
            self.dashed_line = self.comparison_lines.pop(0)
            self.update()
            return

        dist, line = self.comparison_lines.pop(0)  # Get the first task
        self.shortestLine = (dist, QLineF(*line))  # Store the line and distance
        self.update()  # Trigger a repaint to draw the current line

    def solve_closest_distance(self):
        pts = [Point(event.x(), event.y()) for event in self.points]
        reply = solve_closest_distance_nlog_divide_conquer(pts, self.distance)
        self.comparison_lines = reply["comparison_lines"]
        print(f"nlog: {reply['min_distance']}")
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
