from PyQt4 import QtGui
from link import Link
from networkAttr import networkAttr
import math


class duplexLink(QtGui.QWidget):
    def __init__(self, core1, core2, direction):
        super(duplexLink, self).__init__()
        self.core1 = core1
        self.core2 = core2
        self.direction = direction
        self.links = []
        self.link_id = None
        self.updated_link_flits = []
        self.create_links()

    #Creates a bi directional link out of 2 links
    #Allows for the consolidation of link ids
    def create_links(self):
        link1 = Link(self.core1, self.core2)
        self.links.append(link1)
        link2 = Link(self.core2, self.core1)
        self.links.append(link2)
        # if link1.get_link_id() == link2.get_link_id():
        #     self.link_id = link1.get_link_id()
        #     self.core1.add_link_id(self.link_id)
        #     self.core2.add_link_id(self.link_id)
        # else:
        #     self.core1.add_link_id(link1.get_link_id())
        #     self.core2.add_link_id(link2.get_link_id())
        self.link_id = link1.get_link_id()
        self.core1.add_link_id(link1.get_link_id())
        self.core1.add_link_id(link2.get_link_id())
        self.core2.add_link_id(link1.get_link_id())
        self.core2.add_link_id(link2.get_link_id())

        print(str(self.core1.core_id) + " " + str(self.core2.core_id) + " " + str(link1.link_id))
        print(str(self.core2.core_id) + " " + str(self.core1.core_id) + " " + str(link2.link_id))

    #Updates the duplex link based on flits on the link from parser
    #Routing dependent!
    #Currently implements shortest hop count direction since garnet does not give output direction
    def update_duplex_link(self, updated_link_flits):
        self.updated_link_flits = updated_link_flits
        link1_flit = []
        link2_flit = []
        for flit in self.updated_link_flits:
            dest_core = flit.dest
            hop_count_core1 = self.hop_count(self.core1.core_id, dest_core)
            hop_count_core2 = self.hop_count(self.core2.core_id, dest_core)
            if hop_count_core1 < hop_count_core2:
                link2_flit.append(flit)
            else:
                link1_flit.append(flit)
        self.links[0].update_link(link1_flit)
        self.links[1].update_link(link2_flit)

    #Draws the duplex link
    def draw_duplex_link(self, painter):
        for link in self.links:
            link.draw_link(painter)

    #Calculates the remaining hops to a destination core from source core
    #Used in deciding which direction flit is travelling on duplex link
    #Would like to replace this with information from garnet
    @staticmethod
    def hop_count(src_core, dest_core):
        src_col = src_core % networkAttr.CORE_COLS
        src_row = math.floor(src_core / networkAttr.CORE_COLS)
        dest_col = dest_core % networkAttr.CORE_COLS
        dest_row = math.floor(dest_core / networkAttr.CORE_COLS)
        return abs(src_col - dest_col) + abs(src_row - dest_row)

