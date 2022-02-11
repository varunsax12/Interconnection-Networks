import math
from PyQt4 import QtGui
from networkAttr import networkAttr


# Class for VC information tables
# Presents buffer information in the form of tables
# Shows flits in buffer and their relevant values
class BuffInfo(QtGui.QWidget):
    def __init__(self):
        super(BuffInfo, self).__init__()
        # Core Information
        self.current_core = None
        self.current_vn = None
        self.top_table = None
        self.bottom_table = None
        self.cur_buffer_index = None

    # Sets up the vc table headers and other attributes
    def setup_vc_tables(self, table, table_loc):
        if networkAttr.CORE_VCS > 4 and table_loc is "Top":
            self.top_table = table
            vc_range = math.ceil(networkAttr.CORE_VCS / 2)
            vc_start = 0
            vc_end = vc_range
        elif networkAttr.CORE_VCS > 4 and table_loc is "Bottom":
            self.bottom_table = table
            vc_range = math.floor(networkAttr.CORE_VCS / 2)
            vc_start = vc_range
            vc_end = networkAttr.CORE_VCS
        else:
            vc_range = networkAttr.CORE_VCS
            vc_start = 0
            vc_end = networkAttr.CORE_VCS

        table.setColumnCount(vc_range)
        table.setRowCount(6)

        item = QtGui.QTableWidgetItem()
        table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        table.setVerticalHeaderItem(5, item)
        # item = QtGui.QTableWidgetItem()
        # table.setVerticalHeaderItem(5, item)
        item = table.verticalHeaderItem(0)
        item.setText("Flit Id")
        item = table.verticalHeaderItem(1)
        item.setText("Flit Type")
        item = table.verticalHeaderItem(2)
        item.setText("Flit Route")
        item = table.verticalHeaderItem(3)
        item.setText("Flit Outport")
        # item = table.verticalHeaderItem(4)
        # item.setText("Flit Src Delay")
        item = table.verticalHeaderItem(4)
        item.setText("Cycles in Current VC")
        item = table.verticalHeaderItem(5)
        item.setText("Current Location")


        for index, vc_num in enumerate(range(vc_start, vc_end)):
            item = QtGui.QTableWidgetItem()
            table.setHorizontalHeaderItem(index, item)
            item = table.horizontalHeaderItem(index)
            item.setText("VC " + str(vc_num))

    # Updates the table for a change in cycle, core, buffer, or vn
    def update_tables(self, vn, core, buffer_index):
        self.current_vn = vn
        self.cur_buffer_index = buffer_index
        self.current_core = core
        # clears the table before each change
        self.clear_tables()
        buffer = self.current_core.buffers[self.cur_buffer_index]
        for flit in buffer.flits:
            flit_table_entries = self.setup_flit_table_items(flit)
            if flit.vc < self.top_table.columnCount():
                for row, entry in enumerate(flit_table_entries):
                    self.top_table.setItem(row, flit.vc, entry)
            else:
                for row, entry in enumerate(flit_table_entries):
                    self.bottom_table.setItem(row, flit.vc - self.top_table.columnCount(), entry)
        self.update()

    # creates table objects for each flit value for input into the table
    @staticmethod
    def setup_flit_table_items(flit):
        flit_qwidgets = []
        # flit Id
        flit_qwidgets.append(QtGui.QTableWidgetItem(str(flit.id)))
        # Flit Type
        flit_qwidgets.append(QtGui.QTableWidgetItem(flit.type))
        # flit Route
        string = str(flit.src) + " -> " + str(flit.dest)
        flit_qwidgets.append(QtGui.QTableWidgetItem(string))
        # Flit Outport
        flit_qwidgets.append(QtGui.QTableWidgetItem(flit.outport))
        # # Flit Source Delay
        # flit_qwidgets.append(QtGui.QTableWidgetItem(str(flit.src_delay)))
        # Flit stuck cycle
        flit_qwidgets.append(QtGui.QTableWidgetItem(str(flit.stuck_cycles)))
        flit_qwidgets.append(QtGui.QTableWidgetItem(str(flit.location)))
        return flit_qwidgets

    # sets the top table for the combined table widget
    def set_top_table(self, top_table):
        self.top_table = top_table

    # sets the bottom table for the combined table widget
    def set_bottom_table(self, bottom_table):
        self.bottom_table = bottom_table

    # clears the table of old information
    def clear_tables(self):
        if self.top_table is not None:
            self.top_table.clearContents()
        if self.bottom_table is not None:
            self.bottom_table.clearContents()
