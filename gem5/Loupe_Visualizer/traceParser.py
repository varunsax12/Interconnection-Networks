import csv
import itertools
from collections import defaultdict
from flit import Flit
from networkAttr import networkAttr
from TraceDead import flit_trace_no_file


#Parser developed with garnet2.0 parser
#Reads in CSV file for each cycle
#Cycle counts larger than 5000 not recommended due to delay
class traceParser(object):
    def __init__(self):
        self.cycle_row_nums = dict()
        self.csv_file_name = None
        self.csv = None
        self.reader = None
        self.flit_tracker = dict()
        # Trace dictionary in default dictionary
        self.trace_dict = defaultdict(set)
        self.valid_cycles = list()

    #opens the trace
    def open_trace(self, csv_file_name):
        self.csv_file_name = csv_file_name
        self.csv = open(csv_file_name, 'r')
        self.reader = csv.reader(self.csv)
        self.preprocess()

    #opens the snapshot
    def open_snapshot(self, csv_file_name):
        self.csv_file_name = csv_file_name
        self.csv = open(csv_file_name, 'r')
        self.reader = csv.reader(self.csv)

    #creates a dictionary with key = cycle number and value = row the cycle begins at
    def preprocess(self):
        for row_num, row in enumerate(self.reader):
            if 'GarnetNetwork' not in row[0]:
                if int(row[0]) in self.cycle_row_nums:
                    pass
                if (int(row[0]) not in self.cycle_row_nums):
                    self.cycle_row_nums[int(row[0])] = row_num
        self.valid_cycles = list(self.cycle_row_nums.keys())

    #Returns cycle data based on cycle number using the dictionary lookup
    #Returns empty list if cycle does not exist
    def get_cycle(self, cycle_num, max_cycles):
        updated_router_flits = []
        updated_link_flits = []
        updated_exit_flits = []
        print("getting cycle: " + str(cycle_num))
        print("max_cycle: " + str(max_cycles))
        # Sanity Check, should not happen
        if (cycle_num > max_cycles):
            return []

        # Merge previous dict set with current dict set
        for i in range (cycle_num, 0, -1):
            if (i in self.trace_dict.keys()):
                self.trace_dict[cycle_num].update(set(self.trace_dict[i]))
                break 

        with open(self.csv_file_name, 'r') as f:
            if cycle_num in self.cycle_row_nums:
                # find next cycle
                next_cycle = cycle_num + 1
                while next_cycle not in self.cycle_row_nums:
                    if (next_cycle > max_cycles):
                        break
                    else:
                        next_cycle += 1
                # Calculate right bound for csv file slice
                if (next_cycle > max_cycles):
                    cycle_right_bound = None 
                else:
                    cycle_right_bound = self.cycle_row_nums[cycle_num + 1]

                print(str(self.cycle_row_nums[cycle_num]))
                print(str(cycle_right_bound))

                for row in itertools.islice(csv.reader(f), self.cycle_row_nums[cycle_num],
                                            cycle_right_bound):
                    # Generate new flit
                    insert_flit = Flit(row, True, False)
                    
                    # color assignment
                    if insert_flit.id in self.flit_tracker:
                        insert_flit.set_flit_color(self.flit_tracker[insert_flit.id])
                        # remove color entry if flit has entered the exit link
                        if insert_flit.location is "Link":
                            if networkAttr.CORE_CORES <= insert_flit.link_id < networkAttr.CORE_CORES * 2:
                                self.flit_tracker.pop(insert_flit.id)
                    else:
                        self.flit_tracker[insert_flit.id] = insert_flit.get_flit_color()

                    # insert_flit.set_flit_color_over_5000()

                    if insert_flit.location == "Link":
                        updated_link_flits.append(insert_flit)
                    elif insert_flit.location == "InUnit":
                        updated_router_flits.append(insert_flit)

                    # Create list of flits on core interface link
                    if insert_flit.location == "Link":
                        if networkAttr.CORE_CORES <= insert_flit.link_id < networkAttr.CORE_CORES * 2:
                            updated_exit_flits.append(insert_flit.id)

                    # Add row for deadlock calculation
                    self.trace_dict[int(row[0])].discard(insert_flit)
                    self.trace_dict[int(row[0])].add(insert_flit)
                    # print(set(self.trace_dict[int(row[0])]))
                    self.trace_dict[int(row[0])] = set(x for x in self.trace_dict[int(row[0])] if x.outport != "Local")

                return updated_router_flits, updated_link_flits, updated_exit_flits

            return [], [], []

    #Takes in first line from CSV and converts to network parameters
    def get_network_info(self):
        with open(self.csv_file_name, 'r') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            if 'GarnetNetwork' in row1[0]:
                net_info = []
                net_info.append(int(row1[1].split("=")[1]))
                net_info.append(int(row1[2].split("=")[1]))
                net_info.append(int(row1[3].split("=")[1]))
                net_info.append(int(row1[4].split("=")[1]))
                list_of_cycles = list(self.cycle_row_nums.keys())
                net_info.append(max(list_of_cycles))
                net_info.append(min(list_of_cycles))
                net_info.append(list(self.cycle_row_nums.keys()))
                return net_info
            else:
                print("Invalid Trace")
                return None

    # reads single snapshot
    def get_snapshot(self):
        # Get network info first
        updated_router_flits = []
        updated_link_flits = []
        updated_exit_flits = []
        snapshot_cycle = 0
        with open(self.csv_file_name, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if 'GarnetNetwork' not in row[0]:
                    # Set current network cycle
                    snapshot_cycle = int(row[0])
                    # Generate new flit
                    insert_flit = Flit(row, False, True)
                    if insert_flit.location == "Link":
                        updated_link_flits.append(insert_flit)
                    elif insert_flit.location == "InUnit":
                        updated_router_flits.append(insert_flit)

                    # Create list of flits on core interface link
                    if insert_flit.location == "Link":
                        if networkAttr.CORE_CORES <= insert_flit.link_id < networkAttr.CORE_CORES * 2:
                                updated_exit_flits.append(insert_flit.id)

                    # Set flit color
                    insert_flit.set_flit_color_over_5000()

                    # Add row for deadlock calculation
                    self.trace_dict[int(row[0])].add(insert_flit)

        return snapshot_cycle, updated_router_flits, updated_link_flits, updated_exit_flits


    # determine deadlock for single flit
    def find_deadlock(self, id_to, cycle_to, num_vc, num_rows, num_cols):
        loopedRouters = []
        loopFound = False
        if (cycle_to not in self.trace_dict.keys()):
            return [], False
        else:
            flit_set_no_link = set(x for x in self.trace_dict[cycle_to] if (x.location != "Link"))
            loopedRouters, loopFound = flit_trace_no_file(flit_set_no_link, num_rows, num_cols, id_to, num_vc)

        return loopedRouters, loopFound

    # Determine whether deadlock has occurred in one cycle
    def find_deadlock_cycle(self, cycle_to, num_vc, num_cols, num_rows):
        loopedRouters = []
        loopFound = []
        ret = False
        if (cycle_to not in self.trace_dict.keys()):
            return False
        else:
            # Exclude flits that are in link
            flit_set_no_link = set(x for x in self.trace_dict[cycle_to] if (x.location != "Link"))
            # For each flit that are in the set, check deadlock
            for each_flit in flit_set_no_link:
                loopedRouters, loopFound= flit_trace_no_file(flit_set_no_link, num_rows, num_cols, each_flit.id, num_vc)
                if loopFound:
                    # print("Deadlock found in flit: " + str(each_flit.id))
                    each_flit.deadlocked = True
                    ret = True

        return ret
            



