
import os

traffic_list = ["uniform_random", "bit_complement", "shuffle"]
possible_strings = [
    "packets_injected",
    "packets_received",
    "average_packet_queueing_latency",
    "average_packet_network_latency",
    "average_packet_latency",
    "flits_injected",
    "flits_received",
    "average_flit_queueing_latency",
    "average_flit_network_latency",
    "average_flit_latency",
    "average_hops"]
for traffic_type in traffic_list:
    outfile = "result_stats_torus_" + traffic_type + ".csv"
    with open(outfile, "w") as OUTFH:
        OUTFH.write("injection_rate;")
        for curr_string in possible_strings:
            OUTFH.write(curr_string + ";")
        OUTFH.write("\n")
        stop_threshold = 100
        b_stop_condition_reached = False
        for i in range(1, 26):
            if b_stop_condition_reached:
                break
            os.system("./build/Garnet_standalone/gem5.opt configs/example/garnet_synth_traffic.py --network=garnet2.0 --num-cpus=16 --num-dirs=16 --topology=Torus --mesh-rows=4 --sim-cycles=50000 --inj-vnet=0 --router-latency=2 --injectionrate=" + str(i*0.02) + " --synthetic=" + traffic_type + " --link-width-bits=32")
            os.system("./my_scripts/extract_network_stats.sh")
            fileLoc = "network_stats.txt"
            OUTFH.write(str(0.02*i) + ";")
            with open(fileLoc) as FH:
                lines = FH.readlines()
                for line in lines:
                    line = line.strip()
                    for curr_string in possible_strings:
                        out_string = ";"
                        if "average_hops" in line:
                            out_string = "\n"
                        if curr_string in line:
                            line = line.replace(curr_string + " = ", "")
                            OUTFH.write(line + out_string)
                            if "average_packet_latency" in curr_string and float(line) > stop_threshold:
                                b_stop_condition_reached = True
