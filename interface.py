import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QLineF
from PyQt5.QtCore import QTimer
from geometry import Point, solve_closest_distance_nlog, solve_closest_distance_quadratic

inf = 1000000

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Click to Add Points"
        self.top = 100
        self.left = 100
        self.width = 400
        self.height = 300
        self.shortestLine = None  # To store the shortest line found
        self.comparison_lines = []
        self.distance = 1000000
        self.points = []  # Store the points
        self.submitClicked = False  # Flag to track if submit has been clicked
        self.timer = QTimer(self)  # Create a QTimer instance
        self.timer.timeout.connect(self.performComparison)  # Connect the timer to the comparison method
        self.initWindow()

    def initWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        
        # Create and position the submit button
        self.button = QPushButton('Submit', self)
        self.button.move(150, 260)  # Position the button
        self.button.clicked.connect(self.onSubmitClick)  # Connect button click to function
        
        self.show()

    def onSubmitClick(self):
        # Hide the submit button
        self.button.hide()
        self.submitClicked = True  # Set the flag to True when submit is clicked
        
        # Create a label to show the distance, starting with a default value
        self.distance = inf
        self.distanceLabel = QLabel(f"Best current distance: {self.distance}", self)
        self.distanceLabel.move(100, 260)  # Position the label
        self.distanceLabel.resize(210, 30)  # Optionally resize the label if needed
        self.distanceLabel.show()
        self.quadratic()
        self.solve_closest_distance()  # Call the method to solve the closest distance
        self.timer.start(700)  # Start the timer to perform comparisons every 100ms
        
    def quadratic(self):
        pts = [Point(event.x(), event.y()) for event in self.points]
        reply = solve_closest_distance_quadratic(pts, self.distance)
        print(f"quadratic: {reply['min_distance']}")

    def mousePressEvent(self, event):
        if self.submitClicked:  # Check if submit has been clicked
            return
        # Add point where mouse is clicked
        self.points.append(event.pos())
        print(event.pos())
        print(f"Point added at: ({event.x()}, {event.y()})")
        self.update()  # Trigger paint event

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 5, Qt.SolidLine))
        for point in self.points:
            painter.drawPoint(point)

        if self.shortestLine:
            dist, line = self.shortestLine
            pen_color = Qt.green if dist < self.distance else Qt.gray
            self.distanceLabel.setText(f"Best current distance: {dist}")
            self.distance = dist
            painter.setPen(QPen(pen_color, 2, Qt.SolidLine))
            painter.drawLine(line)
        
    
    def performComparison(self):
        # Method to perform a single comparison from the list of tasks
        if not self.comparison_lines:
            self.timer.stop()  # Stop the timer if there are no more tasks
            return
        
        dist,line = self.comparison_lines.pop(0)  # Get the first task
        self.shortestLine = (dist,QLineF(*line))  # Store the line and distance
        self.update()  # Trigger a repaint to draw the current line

    def solve_closest_distance(self):
        pts = [Point(event.x(), event.y()) for event in self.points]
        reply = solve_closest_distance_nlog(pts, self.distance)
        self.comparison_lines = reply["comparison_lines"]
        print(f"nlog: {reply['min_distance']}")
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())

