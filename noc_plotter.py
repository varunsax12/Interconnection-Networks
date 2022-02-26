
import matplotlib.pyplot as plt
import numpy as np

parent_loc = "graph_data"
#file_list = ["t_xy.csv", "t_turn_model_oblivious.csv", "t_turn_model_adaptive.csv", "t_random_oblivious.csv"]
file_list = ["ur_xy.csv", "ur_turn_model_oblivious.csv", "ur_turn_model_adaptive.csv", "ur_random_oblivious.csv"]
legends = ["XY", "Turn Model Oblivious", "Turn Model Adaptive", "Random Oblivious + Escape VC"]
x_ticks = []
for index in range(0, len(file_list)):
    file_path = parent_loc + "/" + file_list[index]
    with open(file_path) as FH:
        lines = FH.readlines()
        list_x = []
        list_y = []
        line_num = 0
        for line in lines[1:]:
            if "fail" not in line:
                items = line.split(";")
                list_x.append(items[0])
                #list_y.append(float(items[2])/(64*20000))
                list_y.append(items[-2])
                if ((line_num % 5) == 0):
                    x_ticks.append(items[0])
                #print(line)
            line_num += 1
    plt.plot(list_x, list_y, label = legends[index], linewidth = 2)

plt.tight_layout()
plt.xticks(x_ticks)
plt.legend()
plt.grid()
#plt.title("Part D. Traffic: Uniform Random")
plt.title("Part D. Traffic: Transpose")
plt.xlabel("Injection Rate")
plt.ylabel("Reception Rate")
plt.show()
#plt.savefig(parent_loc + '/transpose.png', bbox_inches='tight')
