/*
 * Copyright (c) 2008 Princeton University
 * Copyright (c) 2016 Georgia Institute of Technology
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met: redistributions of source code must retain the above copyright
 * notice, this list of conditions and the following disclaimer;
 * redistributions in binary form must reproduce the above copyright
 * notice, this list of conditions and the following disclaimer in the
 * documentation and/or other materials provided with the distribution;
 * neither the name of the copyright holders nor the names of its
 * contributors may be used to endorse or promote products derived from
 * this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 * A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * Authors: Niket Agarwal
 *          Tushar Krishna
 */


#include "mem/ruby/network/garnet2.0/RoutingUnit.hh"

#include "base/cast.hh"
#include "base/logging.hh"
#include "mem/ruby/network/garnet2.0/InputUnit.hh"
#include "mem/ruby/network/garnet2.0/Router.hh"
#include "mem/ruby/slicc_interface/Message.hh"

RoutingUnit::RoutingUnit(Router *router)
{
    m_router = router;
    m_routing_table.clear();
    m_weight_table.clear();
}

void
RoutingUnit::addRoute(const NetDest& routing_table_entry)
{
    m_routing_table.push_back(routing_table_entry);
}

void
RoutingUnit::addWeight(int link_weight)
{
    m_weight_table.push_back(link_weight);
}

/*
 * This is the default routing algorithm in garnet.
 * The routing table is populated during topology creation.
 * Routes can be biased via weight assignments in the topology file.
 * Correct weight assignments are critical to provide deadlock avoidance.
 */

int
RoutingUnit::lookupRoutingTable(int vnet, NetDest msg_destination)
{
    // First find all possible output link candidates
    // For ordered vnet, just choose the first
    // (to make sure different packets don't choose different routes)
    // For unordered vnet, randomly choose any of the links
    // To have a strict ordering between links, they should be given
    // different weights in the topology file

    int output_link = -1;
    int min_weight = INFINITE_;
    std::vector<int> output_link_candidates;
    int num_candidates = 0;

    // Identify the minimum weight among the candidate output links
    for (int link = 0; link < m_routing_table.size(); link++) {
        if (msg_destination.intersectionIsNotEmpty(m_routing_table[link])) {

        if (m_weight_table[link] <= min_weight)
            min_weight = m_weight_table[link];
        }
    }

    // Collect all candidate output links with this minimum weight
    for (int link = 0; link < m_routing_table.size(); link++) {
        if (msg_destination.intersectionIsNotEmpty(m_routing_table[link])) {

            if (m_weight_table[link] == min_weight) {

                num_candidates++;
                output_link_candidates.push_back(link);
            }
        }
    }

    if (output_link_candidates.size() == 0) {
        fatal("Fatal Error:: No Route exists from this Router.");
        exit(0);
    }

    // Randomly select any candidate output link
    int candidate = 0;
    if (!(m_router->get_net_ptr())->isVNetOrdered(vnet))
        candidate = rand() % num_candidates;

    output_link = output_link_candidates.at(candidate);
    return output_link;
}


void
RoutingUnit::addInDirection(PortDirection inport_dirn, int inport_idx)
{
    m_inports_dirn2idx[inport_dirn] = inport_idx;
    m_inports_idx2dirn[inport_idx]  = inport_dirn;
}

void
RoutingUnit::addOutDirection(PortDirection outport_dirn, int outport_idx)
{
    m_outports_dirn2idx[outport_dirn] = outport_idx;
    m_outports_idx2dirn[outport_idx]  = outport_dirn;
}

// outportCompute() is called by the InputUnit
// It calls the routing table by default.
// A template for adaptive topology-specific routing algorithm
// implementations using port directions rather than a static routing
// table is provided here.

int
RoutingUnit::outportCompute(RouteInfo route, int inport,
                            PortDirection inport_dirn,
                            int vc)
{
    int outport = -1;

    int vnet = route.vnet;
    int vc_base = vnet * m_router->get_vc_per_vnet();
    int vc_escape1 = vc_base + m_router->get_vc_per_vnet() - 1;

    if (route.dest_router == m_router->get_id()) {

        // Multiple NIs may be connected to this router,
        // all with output port direction = "Local"
        // Get exact outport id from table
        outport = lookupRoutingTable(route.vnet, route.net_dest);
        return outport;
    }

    // Routing Algorithm set in GarnetNetwork.py
    // Can be over-ridden from command line using --routing-algorithm = 1
    RoutingAlgorithm routing_algorithm =
        (RoutingAlgorithm) m_router->get_net_ptr()->getRoutingAlgorithm();

    switch (routing_algorithm) {
        case TABLE_:  outport =
            lookupRoutingTable(route.vnet, route.net_dest); break;
        case XY_:     outport =
            outportComputeXY(route, inport, inport_dirn); break;
        case TURN_MODEL_OBLIVIOUS_: outport =
            outportComputeTurnModelOblivious(route, inport, inport_dirn); break;
        case TURN_MODEL_ADAPTIVE_: outport =
            outportComputeTurnModelAdaptive(route, inport, inport_dirn); break;
        case RANDOM_OBLIVIOUS_:
        {
            if (vc != vc_escape1)
            {
                outport =
                outportComputeRandomOblivious(route, inport, inport_dirn);
            }
            else
            {
                outport =
                outportComputeTurnModelWestFirst(route, inport, inport_dirn);
            }
            break;
        }
        case RANDOM_ADAPTIVE_: outport =
            outportComputeRandomAdaptive(route, inport, inport_dirn); break;
        // any custom algorithm
        case CUSTOM_: outport =
            outportComputeCustom(route, inport, inport_dirn); break;
        default: outport =
            lookupRoutingTable(route.vnet, route.net_dest); break;
    }

    assert(outport != -1);
    return outport;
}

int
RoutingUnit::outportComputeTurnModelWestFirst(RouteInfo route,
                                    int inport,
                                    PortDirection inport_dirn)
{

    PortDirection outport_dirn = "Unknown";

    int M5_VAR_USED num_rows = m_router->get_net_ptr()->getNumRows();
    int num_cols = m_router->get_net_ptr()->getNumCols();
    assert(num_rows > 0 && num_cols > 0);

    int my_id = m_router->get_id();
    int my_x = my_id % num_cols;
    int my_y = my_id / num_cols;

    int dest_id = route.dest_router;
    int dest_x = dest_id % num_cols;
    int dest_y = dest_id / num_cols;

    int x_hops = abs(dest_x - my_x);
    int y_hops = abs(dest_y - my_y);

    bool x_dirn = (dest_x >= my_x);
    bool y_dirn = (dest_y >= my_y);

    // already checked that in outportCompute() function
    assert(!(x_hops == 0 && y_hops == 0));

    if (x_hops == 0)
    {
        if (y_dirn > 0)
            outport_dirn = "North";
        else
            outport_dirn = "South";
    }
    else if (y_hops == 0)
    {
        if (x_dirn > 0)
            outport_dirn = "East";
        else
            outport_dirn = "West";
    }
    else
    {
        // Get the number of free ports in each directions (apart from North)
        int EastPort = m_outports_dirn2idx["East"];
        int NorthPort = m_outports_dirn2idx["North"];
        int SouthPort = m_outports_dirn2idx["South"];

        int EastVcCount = this->m_router->get_free_vc_count(EastPort, route.vnet);
        int NorthVcCount = this->m_router->get_free_vc_count(NorthPort, route.vnet);
        int SouthVcCount = this->m_router->get_free_vc_count(SouthPort, route.vnet);
        int rand = random() % 2;

        if (x_dirn && y_dirn) // Quadrant I
        {
            if (EastVcCount < NorthVcCount)
            {
                outport_dirn = "North";
            }
            else if (EastVcCount > NorthVcCount)
            {
                outport_dirn = "East";
            }
            else
            {
                outport_dirn = rand ? "North" : "East";
            }
        }
        else if (!x_dirn && y_dirn) // Quadrant II
            outport_dirn = "West";
        else if (!x_dirn && !y_dirn) // Quadrant III
            outport_dirn = "West";
        else // Quadrant IV
        {
            if (EastVcCount < SouthVcCount)
            {
                outport_dirn = "South";
            }
            else if (EastVcCount > SouthVcCount)
            {
                outport_dirn = "East";
            }
            else
            {
                outport_dirn = rand ? "South" : "East";
            }
        }
    }

    return m_outports_dirn2idx[outport_dirn];
}

// XY routing implemented using port directions
// Only for reference purpose in a Mesh
// By default Garnet uses the routing table
int
RoutingUnit::outportComputeXY(RouteInfo route,
                              int inport,
                              PortDirection inport_dirn)
{
    PortDirection outport_dirn = "Unknown";

    int M5_VAR_USED num_rows = m_router->get_net_ptr()->getNumRows();
    int num_cols = m_router->get_net_ptr()->getNumCols();
    assert(num_rows > 0 && num_cols > 0);

    int my_id = m_router->get_id();
    int my_x = my_id % num_cols;
    int my_y = my_id / num_cols;

    int dest_id = route.dest_router;
    int dest_x = dest_id % num_cols;
    int dest_y = dest_id / num_cols;

    int x_hops = abs(dest_x - my_x);
    int y_hops = abs(dest_y - my_y);

    bool x_dirn = (dest_x >= my_x);
    bool y_dirn = (dest_y >= my_y);

    // already checked that in outportCompute() function
    assert(!(x_hops == 0 && y_hops == 0));

    if (x_hops > 0) {
        if (x_dirn) {
            assert(inport_dirn == "Local" || inport_dirn == "West");
            outport_dirn = "East";
        } else {
            assert(inport_dirn == "Local" || inport_dirn == "East");
            outport_dirn = "West";
        }
    } else if (y_hops > 0) {
        if (y_dirn) {
            // "Local" or "South" or "West" or "East"
            assert(inport_dirn != "North");
            outport_dirn = "North";
        } else {
            // "Local" or "North" or "West" or "East"
            assert(inport_dirn != "South");
            outport_dirn = "South";
        }
    } else {
        // x_hops == 0 and y_hops == 0
        // this is not possible
        // already checked that in outportCompute() function
        panic("x_hops == y_hops == 0");
    }

    return m_outports_dirn2idx[outport_dirn];
}


int
RoutingUnit::outportComputeTurnModelOblivious(RouteInfo route,
                                    int inport,
                                    PortDirection inport_dirn)
{

    PortDirection outport_dirn = "Unknown";

    int M5_VAR_USED num_rows = m_router->get_net_ptr()->getNumRows();
    int num_cols = m_router->get_net_ptr()->getNumCols();
    assert(num_rows > 0 && num_cols > 0);

    int my_id = m_router->get_id();
    int my_x = my_id % num_cols;
    int my_y = my_id / num_cols;

    int dest_id = route.dest_router;
    int dest_x = dest_id % num_cols;
    int dest_y = dest_id / num_cols;

    int x_hops = abs(dest_x - my_x);
    int y_hops = abs(dest_y - my_y);

    bool x_dirn = (dest_x >= my_x);
    bool y_dirn = (dest_y >= my_y);

    // already checked that in outportCompute() function
    assert(!(x_hops == 0 && y_hops == 0));

    if (x_hops == 0)
    {
        if (y_dirn > 0)
            outport_dirn = "North";
        else
            outport_dirn = "South";
    }
    else if (y_hops == 0)
    {
        if (x_dirn > 0)
            outport_dirn = "East";
        else
            outport_dirn = "West";
    }
    else
    {
        int rand = random() % 2;

        if (x_dirn && y_dirn) // Quadrant I
            outport_dirn = "East";
        else if (!x_dirn && y_dirn) // Quadrant II
            outport_dirn = "West";
        else if (!x_dirn && !y_dirn) // Quadrant III
            outport_dirn = rand ? "West" : "South";
        else // Quadrant IV
            outport_dirn = rand ? "East" : "South";
    }

    return m_outports_dirn2idx[outport_dirn];
}

int
RoutingUnit::outportComputeTurnModelAdaptive(RouteInfo route,
                                    int inport,
                                    PortDirection inport_dirn)
{

    PortDirection outport_dirn = "Unknown";

    int M5_VAR_USED num_rows = m_router->get_net_ptr()->getNumRows();
    int num_cols = m_router->get_net_ptr()->getNumCols();
    assert(num_rows > 0 && num_cols > 0);

    int my_id = m_router->get_id();
    int my_x = my_id % num_cols;
    int my_y = my_id / num_cols;

    int dest_id = route.dest_router;
    int dest_x = dest_id % num_cols;
    int dest_y = dest_id / num_cols;

    int x_hops = abs(dest_x - my_x);
    int y_hops = abs(dest_y - my_y);

    bool x_dirn = (dest_x >= my_x);
    bool y_dirn = (dest_y >= my_y);

    // already checked that in outportCompute() function
    assert(!(x_hops == 0 && y_hops == 0));

    if (x_hops == 0)
    {
        if (y_dirn > 0)
            outport_dirn = "North";
        else
            outport_dirn = "South";
    }
    else if (y_hops == 0)
    {
        if (x_dirn > 0)
            outport_dirn = "East";
        else
            outport_dirn = "West";
    }
    else
    {
        // Get the number of free ports in each directions (apart from North)
        int EastPort = m_outports_dirn2idx["East"];
        int WestPort = m_outports_dirn2idx["West"];
        int SouthPort = m_outports_dirn2idx["South"];
        //std::vector<OutputUnit *> output_unit_list = this->m_router->get_outputUnit_ref();
        //assert(output_unit_list[EastPort]->get_id() != EastPort);
        //output_unit_list[EastPort];
        int EastVcCount = this->m_router->get_free_vc_count(EastPort, route.vnet);
        int WestVcCount = this->m_router->get_free_vc_count(WestPort, route.vnet);
        int SouthVcCount = this->m_router->get_free_vc_count(SouthPort, route.vnet);

        int rand = random() % 2;

        if (x_dirn && y_dirn) // Quadrant I
            outport_dirn = "East";
        else if (!x_dirn && y_dirn) // Quadrant II
            outport_dirn = "West";
        else if (!x_dirn && !y_dirn) // Quadrant III
        {
            if (WestVcCount > SouthVcCount)
            {
                outport_dirn = "West";
            }
            else if (WestVcCount < SouthVcCount)
            {
                outport_dirn = "South";
            }
            else
            {
                outport_dirn = rand ? "West" : "South";
            }
        }
        else // Quadrant IV
        {
            if (EastVcCount > SouthVcCount)
            {
                outport_dirn = "East";
            }
            else if (EastVcCount < SouthVcCount)
            {
                outport_dirn = "South";
            }
            else
            {
                outport_dirn = rand ? "East" : "South";
            }
        }
    }

    return m_outports_dirn2idx[outport_dirn];
}


int
RoutingUnit::outportComputeRandomOblivious(RouteInfo route,
                              int inport,
                              PortDirection inport_dirn)
{
    PortDirection outport_dirn = "Unknown";

    int M5_VAR_USED num_rows = m_router->get_net_ptr()->getNumRows();
    int num_cols = m_router->get_net_ptr()->getNumCols();
    assert(num_rows > 0 && num_cols > 0);

    int my_id = m_router->get_id();
    int my_x = my_id % num_cols;
    int my_y = my_id / num_cols;

    int dest_id = route.dest_router;
    int dest_x = dest_id % num_cols;
    int dest_y = dest_id / num_cols;

    int x_hops = abs(dest_x - my_x);
    int y_hops = abs(dest_y - my_y);

    bool x_dirn = (dest_x >= my_x);
    bool y_dirn = (dest_y >= my_y);

    // already checked that in outportCompute() function
    assert(!(x_hops == 0 && y_hops == 0));

    if (x_hops == 0)
    {
        if (y_dirn > 0)
            outport_dirn = "North";
        else
            outport_dirn = "South";
    }
    else if (y_hops == 0)
    {
        if (x_dirn > 0)
            outport_dirn = "East";
        else
            outport_dirn = "West";
    } else {
        int rand = random() % 2;

        if (x_dirn && y_dirn) // Quadrant I
            outport_dirn = rand ? "East" : "North";
        else if (!x_dirn && y_dirn) // Quadrant II
            outport_dirn = rand ? "West" : "North";
        else if (!x_dirn && !y_dirn) // Quadrant III
            outport_dirn = rand ? "West" : "South";
        else // Quadrant IV
            outport_dirn = rand ? "East" : "South";
    }

    return m_outports_dirn2idx[outport_dirn];
}

int
RoutingUnit::outportComputeRandomAdaptive(RouteInfo route,
                              int inport,
                              PortDirection inport_dirn)
{
    panic("%s placeholder executed", __FUNCTION__);
}

// Template for implementing custom routing algorithm
// using port directions. (Example adaptive)
int
RoutingUnit::outportComputeCustom(RouteInfo route,
                                 int inport,
                                 PortDirection inport_dirn)
{
    panic("%s placeholder executed", __FUNCTION__);
}
