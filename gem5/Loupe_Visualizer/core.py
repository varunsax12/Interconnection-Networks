import math
from PyQt4 import QtCore, QtGui
from buffer import Buffer
from networkAttr import networkAttr
from drawAttr import drawAttr
from flit import Flit

# Core Implementation
class Core(QtGui.QWidget):
    def __init__(self, core_id):
        super(Core, self).__init__()
        # Core Information
        self.core_id = core_id
        self.buffers = []
        self.link_ids = []
        self.draw_row = core_id % networkAttr.CORE_COLS
        self.draw_col = math.floor(core_id / networkAttr.CORE_COLS)
        self.row = None
        self.col = None
        # Graphics Options
        self.size = QtCore.QSizeF(drawAttr.CORE_SIZE, drawAttr.CORE_SIZE)
        self.setMinimumSize(drawAttr.CORE_SIZE, drawAttr.CORE_SIZE)
        # Pixel positions
        self.top_left_corner = QtCore.QPointF(self.draw_row * drawAttr.CORE_SIZE + self.draw_row * drawAttr.LINK_LENGTH,
                                              self.draw_col * drawAttr.CORE_SIZE + self.draw_col * drawAttr.LINK_LENGTH)
        # Core Rectangle Object
        self.rect = QtCore.QRectF(self.top_left_corner, self.size)
        self.text_id = str(self.core_id)
        self.text_id_pos = QtCore.QPointF()
        self.create_buffers()
        self.create_core_id_text()
        self.color = QtGui.QColor(0, 0, 0, 0)

    # Creates the core ID text and location
    def create_core_id_text(self):
        pos = self.rect.center()
        if networkAttr.CORE_VCS == 4:
            pos.setY(pos.y() + 25)  # 15
        else:
            pos.setY(pos.y() + 15)  # 15
        pos.setX(pos.x() - 4)
        self.text_id_pos = pos

    # Creates Buffers based on location
    # Mesh dependent
    def create_buffers(self):
        # Create Buffers
        if self.draw_col + 1 < networkAttr.CORE_COLS:
            self.buffers.append(Buffer(self.core_id, self.top_left_corner, "South"))
        if self.draw_col - 1 >= 0:
            self.buffers.append(Buffer(self.core_id, self.top_left_corner, "North"))
        if self.draw_row + 1 < networkAttr.CORE_ROWS:
            self.buffers.append(Buffer(self.core_id, self.top_left_corner, "East"))
        if self.draw_row - 1 >= 0:
            self.buffers.append(Buffer(self.core_id, self.top_left_corner, "West"))
        self.buffers.append(Buffer(self.core_id, self.top_left_corner, "Core"))

    # Draws the Core
    def draw_core(self, painter):
        painter.drawRect(self.rect)
        painter.fillRect(self.rect, self.color)
        painter.drawText(self.text_id_pos, self.text_id)
        for buf in self.buffers:
            buf.draw_buffer(painter)

    # Updates the core using parsed data divided into location (router, link)
    def update_core(self, updated_router_flits, possible_link_flits, updated_exit_flits, cycle_num, deadlock_check_cont):
        for buf in self.buffers:
            flits_per_buffer = []
            for flit in updated_router_flits:
                if flit.in_dir == buf.link_dir:
                    flits_per_buffer.append(flit)
            if not deadlock_check_cont:
                for buf_flit in buf.flits:
                    if not buf_flit.has_exited:
                        if buf_flit.cycle <= cycle_num:
                            if (Flit.FLIT_CYCLES_DEADLOCK is not None and cycle_num - buf_flit.cycle > Flit.FLIT_CYCLES_DEADLOCK):
                                buf_flit.deadlocked = True
                            else:
                                buf_flit.deadlocked = False
                            buf_flit.src_delay += 1
                            flits_per_buffer.append(buf_flit)
            else:
                for buf_flit in buf.flits:
                    if not buf_flit.has_exited:
                        if buf_flit.cycle <= cycle_num:
                            buf_flit.src_delay += 1
                            flits_per_buffer.append(buf_flit)

            # checks to see if a buffer is driving a link
            # keeps the flit in buffer to show the VC driving the link
            # print("\nCore: " + str(self.core_id))
            # print("Cycle: " + str(cycle_num))
            # print("Possible link flits")
            # print(possible_link_flits)
            # print("Buf flits")
            # print(buf.flits)
            for link_flit in possible_link_flits:
                for buf_flit in buf.flits:
                    if buf_flit.id == link_flit.id:
                        buf_flit.has_exited = True
                        buf_flit.cycle_exited = cycle_num
            # Maintain flit state if this is not their destination core
            for buf_flit in buf.flits:
                if buf_flit.id in updated_exit_flits:
                    buf_flit.has_exited = True
                    buf_flit.cycle_exited = cycle_num
            buf.update_buffer(flits_per_buffer)


    # Sets the core id based on the garnet id method rather than pyQT orientation
    def set_core_id(self, core_id):
        self.core_id = core_id
        self.text_id = str(self.core_id)
        self.col = core_id % networkAttr.CORE_COLS
        self.row = math.floor(core_id / networkAttr.CORE_COLS)

    # Adds to the list of link_ids for use in driving buffer check
    def add_link_id(self, link_id):
        self.link_ids.append(link_id)

    def change_color(self, color):
        print(color)
        self.color = QtGui.QColor(color[0], color[1], color[2], color[3])
        #painter.fillRect(self.rect, QtGui.QColor(color[0], color[1], color[2], 110))

    def __str__(self):
        string = "[Core::"
        string += " Id:" + str(self.core_id)
        string += " Row:" + str(self.row)
        string += " Col:" + str(self.col)
        string += " Draw_Row:" + str(self.draw_row)
        string += " Draw_Col:" + str(self.draw_col)
        string += "\n\r"
        return string

    def __repr__(self):
        string = "[Core::"
        string += " Id:" + str(self.core_id)
        string += " Row:" + str(self.row)
        string += " Col:" + str(self.col)
        string += " Draw_Row:" + str(self.draw_row)
        string += " Draw_Col:" + str(self.draw_col)
        string += "\n\r"
        return string
