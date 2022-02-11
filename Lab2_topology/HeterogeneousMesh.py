# Description:
#   Heterogeneous Mesh implementation for lab2 part1 

from m5.params import *
from m5.objects import *

from BaseTopology import SimpleTopology

# Creates a generic Mesh assuming an equal number of cache
# and directory controllers.
# XY routing is enforced (using link weights)
# to guarantee deadlock freedom.

class HeterogeneousMesh(SimpleTopology):
    description='HeterogeneousMesh'

    print "Creating Topology: " + description

    def __init__(self, controllers):
        self.nodes = controllers

    # Makes a generic mesh
    # assuming an equal number of cache and directory cntrls

    def makeTopology(self, options, network, IntLink, ExtLink, Router):
        nodes = self.nodes

        num_routers = options.num_cpus
        num_rows = options.mesh_rows

        # default values for link latency and router latency.
        # Can be over-ridden on a per link/router basis
        link_latency = options.link_latency # used by simple and garnet
        router_latency = options.router_latency # only used by garnet


        # There must be an evenly divisible number of cntrls to routers
        # Also, obviously the number or rows must be <= the number of routers
        cntrls_per_router, remainder = divmod(len(nodes), num_routers)
        assert(num_rows > 0 and num_rows <= num_routers)
        num_columns = int(num_routers / num_rows)
        assert(num_columns * num_rows == num_routers)

        # Create the routers in the mesh
        routers = [Router(router_id=i, latency = router_latency) \
            for i in range(num_routers)]
        network.routers = routers

        # link counter to set unique link ids
        link_count = 0

        # Add all but the remainder nodes to the list of nodes to be uniformly
        # distributed across the network.
        network_nodes = []
        remainder_nodes = []
        for node_index in xrange(len(nodes)):
            if node_index < (len(nodes) - remainder):
                network_nodes.append(nodes[node_index])
            else:
                remainder_nodes.append(nodes[node_index])

        # Connect each node to the appropriate router
        ext_links = []
        for (i, n) in enumerate(network_nodes):
            cntrl_level, router_id = divmod(i, num_routers)
            assert(cntrl_level < cntrls_per_router)
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                    int_node=routers[router_id],
                                    latency = link_latency))
            link_count += 1

        # Connect the remainding nodes to router 0.  These should only be
        # DMA nodes.
        for (i, node) in enumerate(remainder_nodes):
            assert(node.type == 'DMA_Controller')
            assert(i < remainder)
            ext_links.append(ExtLink(link_id=link_count, ext_node=node,
                                    int_node=routers[0],
                                    latency = link_latency))
            link_count += 1

        network.ext_links = ext_links

        # Create the mesh links.
        int_links = []
        print "East output to west input............................"
        # East output to West input links (weight = 1)
        for row in xrange(num_rows):
            for col in xrange(num_columns):
                num_links = 0
                east_out = col + (row * num_columns)
                west_in = (col + 1) + (row * num_columns)
                if col == 0 or col == (num_columns - 2):
                    num_links = 1
                elif row != 0 and row != (num_rows - 1) and col != 0 and col != (num_columns - 1):
                    num_links = 2
                for link_num in range(0, num_links):
                    print "Router " + get_id(routers[east_out]) + " created a link to Router " +  get_id(routers[west_in])
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[east_out],
                                             dst_node=routers[west_in],
                                             src_outport="East",
                                             dst_inport="West",
                                             latency = link_latency,
                                             weight=1))
                    link_count += 1

        print "West output to East input............................"
        # West output to East input links (weight = 1)
        for row in xrange(num_rows):
            for col in xrange(num_columns):
                num_links = 0
                east_in = col + (row * num_columns)
                west_out = (col + 1) + (row * num_columns)
                if col == 0 or col == (num_columns - 2):
                    num_links = 1
                elif row != 0 and row != (num_rows - 1) and col != 0 and col != (num_columns - 1):
                    num_links = 2
                for link_num in range(0, num_links):
                    print "Router " + get_id(routers[west_out]) + " created a link to Router " +  get_id(routers[east_in])
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[west_out],
                                             dst_node=routers[east_in],
                                             src_outport="West",
                                             dst_inport="East",
                                             latency = link_latency,
                                             weight=1))
                    link_count += 1

        print "North output to South input............................"
        # North output to South input links (weight = 2)
        for col in xrange(num_columns):
            for row in xrange(num_rows):
                num_links = 0
                north_out = col + (row * num_columns)
                south_in = col + ((row + 1) * num_columns)
                if row == 0 or row == (num_rows - 2):
                    num_links = 1
                elif row != 0 and row != (num_rows - 1) and col != 0 and col != (num_columns - 1):
                    num_links = 2
                for link_num in range(0, num_links):
                    print "Router " + get_id(routers[north_out]) + " created a link to Router " +  get_id(routers[south_in])
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[north_out],
                                             dst_node=routers[south_in],
                                             src_outport="North",
                                             dst_inport="South",
                                             latency = link_latency,
                                             weight=2))
                    link_count += 1

        print "South output to North input............................"
        # South output to North input links (weight = 2)
        for col in xrange(num_columns):
            for row in xrange(num_rows):
                num_links = 0
                north_in = col + (row * num_columns)
                south_out = col + ((row + 1) * num_columns)
                if row == 0 or row == (num_rows - 2):
                    num_links = 1
                elif row != 0 and row != (num_rows - 1) and col != 0 and col != (num_columns - 1):
                    num_links = 2
                for link_num in range(0, num_links):
                    print "Router " + get_id(routers[south_out]) + " created a link to Router " +  get_id(routers[north_in])
                    int_links.append(IntLink(link_id=link_count,
                                             src_node=routers[south_out],
                                             dst_node=routers[north_in],
                                             src_outport="South",
                                             dst_inport="North",
                                             latency = link_latency,
                                             weight=2))
                    link_count += 1


        network.int_links = int_links

def get_id(node) :
    return str(node).split('.')[3].split('routers')[1]
