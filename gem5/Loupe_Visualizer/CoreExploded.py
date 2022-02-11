from PyQt4 import QtGui, QtCore
from drawAttr import drawAttr
from networkAttr import networkAttr
from buffer import Buffer


class CoreExploded(QtGui.QWidget):
    CORE_EXP_X_OFFSET = 20
    CORE_EXP_Y_OFFSET = 20
    CORE_ID_Y_OFFSET = 35
    CORE_ID_X_OFFSET = -3

    def __init__(self, parent_widget, core_in):
        super(CoreExploded, self).__init__()
        self.setParent(parent_widget)
        # Core Information
        self.core_id = None
        self.buffers = []
        # # Row and Column
        self.draw_row = None
        self.draw_col = None
        # Graphics Options
        self.size = QtCore.QSizeF(drawAttr.CORE_SIZE_EXP, drawAttr.CORE_SIZE_EXP)
        self.setMinimumSize(drawAttr.CORE_SIZE_EXP, drawAttr.CORE_SIZE_EXP)
        # Pixel positions
        self.topLeftCorner = QtCore.QPointF(CoreExploded.CORE_EXP_X_OFFSET, CoreExploded.CORE_EXP_Y_OFFSET)
        # Core Rectangle Object
        self.rect = QtCore.QRectF(self.topLeftCorner, self.size)
        self.text_id = None
        self.text_id_pos = QtCore.QPointF()
        self.update_core(core_in)

    #Updates the core information based on the core select box
    def update_core(self, core_in):
        # Core Information
        self.core_id = core_in.core_id
        self.buffers = []
        # Row and Column
        self.draw_row = core_in.draw_row
        self.draw_col = core_in.draw_col
        # Graphics Options
        self.text_id = str(self.core_id)
        self.create_buffers()
        self.create_core_id_text()
        for index, buf in enumerate(core_in.buffers):
            self.buffers[index].flits = buf.flits

    #Draws the core and its buffers
    def draw_core(self, painter):
        painter.drawRect(self.rect)
        painter.drawText(self.text_id_pos, self.text_id)
        for buf in self.buffers:
            buf.draw_buffer(painter)

    #Creates the core id text
    def create_core_id_text(self):
        pos = self.rect.center()
        if networkAttr.CORE_VCS == 4:
            pos.setY(pos.y() + CoreExploded.CORE_ID_Y_OFFSET + 15)
        else:
            pos.setY(pos.y() + CoreExploded.CORE_ID_Y_OFFSET)
        pos.setX(pos.x() + CoreExploded.CORE_ID_X_OFFSET)
        self.text_id_pos = pos

    #Creates buffers with the correct locations for the exploded core
    def create_buffers(self):
        if self.draw_col + 1 < networkAttr.CORE_COLS:
            self.buffers.append(Buffer(self.core_id, self.topLeftCorner, "South", 1))
        if self.draw_col - 1 >= 0:
            self.buffers.append(Buffer(self.core_id, self.topLeftCorner, "North", 1))
        if self.draw_row + 1 < networkAttr.CORE_ROWS:
            self.buffers.append(Buffer(self.core_id, self.topLeftCorner, "East", 1))
        if self.draw_row - 1 >= 0:
            self.buffers.append(Buffer(self.core_id, self.topLeftCorner, "West", 1))
        self.buffers.append(Buffer(self.core_id, self.topLeftCorner, "Core", 1))

    #Paints the core
    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.draw_core(painter)
        painter.end()
