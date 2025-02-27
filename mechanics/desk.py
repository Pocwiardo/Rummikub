from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *


class ForegroundItem(QGraphicsItem):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.rect = QRectF(0, 0, self.width, self.height)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setBrush(QBrush(QColor(30, 30, 30)))
        painter.drawRect(self.rect)