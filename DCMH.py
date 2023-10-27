import random
from queue import PriorityQueue as PQ
import copy
from collections import Counter
import re
import time
import numpy as np


def random_pick(some_list, probabilities):
    item = 0
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            break
    return item

def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

class Vertex:
    def __init__(self, key, type, MEC_resource, CU_resource, DU_resource):
        self.id = key
        self.connectedTo = {}
        self.type = type
        self.resource = [MEC_resource, CU_resource, DU_resource]
        self.distance = 100000
        self.predecessor = None
        self.status = "F"

    # def __str__(self):
    #     return str(self.id) + ' has computing resource ' + str(self.resource[0]) + ' and DU resource ' + str(self.resource[1]) + ' and CU resource ' + str(self.resource[2]) +' , and connectedTo ' + \
    #            str([x.id for x in self.connectedTo]) +  ' with link info ' + str(self.connectedTo.values())

    def addNeighbour(self, nbr, dt):
        self.connectedTo[nbr] = dt

    def delNeighbor(self, nbr):
        if nbr in self.connectedTo:
            del self.connectedTo[nbr]

    def setStatus(self, newstate):
        self.state = newstate

    def getStatus(self):
        return self.state

    def settype(self, type):
        self.type = type

    def gettype(self):
        return self.type

    def getConnections(self):
        return list(self.connectedTo.keys())

    def getId(self):
        return self.id

    def getLinkInfor(self, nbr):
        if nbr in self.getConnections():
            return self.connectedTo[nbr]
        else:
            return None
    def getResource(self):
        return self.resource

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

    def setDistance(self, distance):
        self.distance = distance

    def getDistance(self):
        return self.distance

    def setPred(self, predecessor):
        self.predecessor = predecessor

    def getPred(self):
        return self.predecessor

class Network:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.traffic = {}
        self.bandwidth = {}

    def addVertex(self, key, type, Computing_resource, CU_resource, DU_resource):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key, type, Computing_resource, CU_resource, DU_resource) # Let newVertex be the data type of class Vertex
        self.vertList[key] = newVertex # VertList is a dictionary; newVertex has three data types pointing to (numeric id, dictionary connectedTo and list resource)
        return newVertex

    def delateVertex(self, key):
        if key in self.vertList:
            del self.vertList[key]
            self.numVertices = self.numVertices - 1
        for i in self.getVertics():
            self.vertList[i].delNeighbor(key)

    def changeResorce(self, key, ch_comp, ch_DU, ch_CU):
        self.vertList[key].resource[0] = self.vertList[key].resource[0] + ch_comp
        self.vertList[key].resource[1] = self.vertList[key].resource[1] + ch_DU
        self.vertList[key].resource[2] = self.vertList[key].resource[2] + ch_CU

    def getVertex(self, n):  # Find the node named n. The node is a data type with three points (numeric id, dictionary connectedTo and list resource).
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n): # It can be judged whether the data we input is in Class. The parameter n is the data we passed in, so we can use print(xx in XX), dict.has_key(key)
        return n in self.vertList

    def addEdge(self, f, t, dt):  # Undirected edge connecting from_Vertex to to_Vertex
        if f in self.vertList and t in self.vertList:
            self.vertList[f].addNeighbour(t, dt)
            self.vertList[t].addNeighbour(f, dt)

    def delEdge(self, f, t):
        if t in self.vertList[f].getConnections() or f in self.vertList[t].getConnections():
            if f in self.getVertics() and t not in self.getVertics():
                self.vertList[f].delNeighbor(t)
            elif f not in self.getVertics() and t in self.getVertics():
                self.vertList[t].delNeighbor(f)
            elif f in self.getVertics() and t in self.getVertics():
                self.vertList[f].delNeighbor(t)
                self.vertList[t].delNeighbor(f)

    def getVertics(self):
        Vertics = []
        for i in self.vertList.keys():
            Vertics.append(i)
        return Vertics

    def getNeighbors(self, vertex):
        Neighbors = self.vertList[vertex].getConnections()
        return Neighbors

    def __iter__(self):
        return iter(self.vertList.values())

    def find_the_paths(self, NodeA, NodeB, path, allpaths):
        self.vertList[NodeA].setStatus("T")
        path.append(NodeA)

        if NodeA == NodeB:
            mm = copy.deepcopy(path) # my god, so important
            allpaths.append(mm)

        else:
            for i in self.getNeighbors(NodeA):
                if self.vertList[i].getStatus() == 'F':
                    self.find_the_paths(i, NodeB, path, allpaths)
        path.pop()
        self.vertList[NodeA].setStatus('F')
        return allpaths

def find_the_shrest_path(req_position, NodeB):
    shortest_path_from_A_to_B = []
    Net.vertList[req_position].setDistance(0)
    value = Net.vertList[req_position].getDistance()
    pd = PQ()
    pd.put((value, req_position))
    while not pd.empty():
        currentVert = pd.get()[1]
        for NextVert in Net.getNeighbors(currentVert):
            newDist = Net.vertList[currentVert].getDistance() + Net.vertList[currentVert].getWeight(NextVert)
            if newDist <= Net.vertList[NextVert].getDistance():
                Net.vertList[NextVert].setDistance(newDist)
                Net.vertList[NextVert].setPred(currentVert)
                pd.put((newDist, NextVert))

    shortest_path_from_A_to_B.append(NodeB)
    while not req_position in shortest_path_from_A_to_B:
        shortest_path_from_A_to_B.append(Net.vertList[shortest_path_from_A_to_B[-1]].getPred())
    shortest_distance_from_A_to_B = Net.vertList[NodeB].getDistance()
    shortest_path_from_A_to_B.reverse()
    for iii in Net.vertList:
        Net.vertList[iii].distance = 100000
        Net.vertList[iii].predecessor = None
    return shortest_path_from_A_to_B, shortest_distance_from_A_to_B

def get_key(dict, value):
    return [k for k, v in dict.items() if v == value]

def chose_the_MEC(Unactivated, Activated_node): # 'activated': Options that may be activated
    activated = [k for k in Activated_node.keys()]
    # for i in activated:  # remove the activated node cause they select themself
    #     if i in Unactivated:
    #         Unactivated.remove(i)
    # print(Unactivated)
    paths_from_Unactivated_to_activated = {}
    for i in Unactivated:
        for target in activated:
            path = Net.find_the_paths(i, target, [], [])
            paths_from_Unactivated_to_activated[i+'-' +target] = path

    distance = {} # only the distance, paths_from_Unactivated include both path and distance
    for i in [k for k in paths_from_Unactivated_to_activated.keys()]:
        distance[i] = []
    for i in [k for k in paths_from_Unactivated_to_activated.keys()]:
        for ii in range(len(paths_from_Unactivated_to_activated[i])):
            length = 0
            q = 0
            while q < len(paths_from_Unactivated_to_activated[i][ii]) - 1:
                dis = Net.vertList[paths_from_Unactivated_to_activated[i][ii][q]].getWeight(paths_from_Unactivated_to_activated[i][ii][q + 1])
                length += dis
                q += 1
            distance[i].append(length)
            paths_from_Unactivated_to_activated[i][ii].append(length) # put the distance information into the links
    # print(distance)
    # print(paths_from_Unactivated_to_activated)

    # record the activated node
    goable_nodes = {} # which nodes can go the activated nodes
    Ungoable_nodes = []
    for i in Unactivated:
        for ii in activated:
            if Net.traffic[i][1] >= min(distance[i + '-' + ii]):
                if ii in goable_nodes:
                    goable_nodes[ii].append(i)
                else:
                    goable_nodes[ii] = [i]
            else:
                Ungoable_nodes.append(i + '-' + ii)
    # print(Ungoable_nodes)

    # sort the first fit order. e.g. 7:[2,3,4,5]  3[2,3,4]. If use 7 to solve 3,4,5, waste 3
    # so processing based on the emerging time, the less, the higher possibility to be solved
    overall_nodes_to_all_activated = []
    for i in [k for k in goable_nodes.values()]:
        for ii in i:
            overall_nodes_to_all_activated.append(ii)

    result = Counter(overall_nodes_to_all_activated)
    values = [k for k in result.values()]
    keys = [k for k in result.keys()]

    zip_two = zip(keys, values)
    sorted_keys_values = sorted(zip_two, key=lambda x:x[1])
    output = zip(*sorted_keys_values)
    sorted_keys, sorted_values = [list(x) for x in output]

    for i in [k for k in goable_nodes.keys()]:
        arr1 = sorted_keys
        goable_nodes[i].sort(key=arr1.index)

    sorted_goable_nodes = copy.deepcopy(goable_nodes)
    # for i in [k for k in goable_nodes.keys()]:
    #     sorted_goable_nodes[i].insert(0, i)
    for i in [k for k in sorted_goable_nodes.keys()]:
        for ii in sorted_goable_nodes[i]:
            if ii in [k for k in sorted_goable_nodes.keys()] and ii != i:
                sorted_goable_nodes[i].remove(ii)
                sorted_goable_nodes[i].append(ii) # The sorting is slightly different from the previous one. Put other PPs at the back first to save the PP and keep it locally without transmission energy consumption
                
    # here we decide PP3 or PP2
    sorted_goable_list = [k for k in sorted_goable_nodes.keys()]
    sorted_goable_nodes_1 = {}
    for i in [k for k in sorted_goable_nodes.keys()]:
        if Net.vertList[i].type == 3:
            task_size = 0
            for ii in sorted_goable_nodes[i]:
                task_size = task_size + Net.traffic[ii][2]
            if task_size > PP2_MEC_size: # As long as it is greater than the carrying capacity of PP2, it is better to use PP3; so according to the queuing method, even the last one is less than the carrying capacity
                sorted_goable_list.remove(i)
                sorted_goable_list.insert(0, i)
            else:
                sorted_goable_list.remove(i)
                sorted_goable_list.append(i)
    for i in sorted_goable_list:
        sorted_goable_nodes_1[i] = sorted_goable_nodes[i]

    Recording = {}        # Recording the node-node-node path, distance
    copy1 = {}
    rest_from_activated = copy.deepcopy(sorted_goable_nodes_1)
    # no_MEC_yet = copy.deepcopy(Net.getVertics()[:-1]) # MEC is not settled
    no_MEC_yet_in_the_end = copy.deepcopy(Unactivated)
    while copy1 != sorted_goable_nodes_1:
        copy1 = copy.deepcopy(sorted_goable_nodes_1)
        for ii in [k for k in sorted_goable_nodes_1.keys()]:
            for i in [k for k in sorted_goable_nodes_1.values()]:
                for iii in i:
                    if Net.traffic[iii][2] <= Activated_node[ii][0]: 
                    # if Net.traffic[iii][2] <= Activated_node[ii][0] and (Net.traffic[iii][3] * left_ratio) <= Activated_node[ii][1] \
                    #         and Net.traffic[iii][3] <= Activated_node[ii][2]: # need to satisfy the size of both MEC/DU/CU
                        Activated_node[ii][0] = Activated_node[ii][0] - Net.traffic[iii][2]
                        # Activated_node[ii][1] = Activated_node[ii][1] - (Net.traffic[iii][3] * left_ratio)
                        # Activated_node[ii][2] = Activated_node[ii][2] - Net.traffic[iii][3]
                        Net.traffic[iii][2] = 0
                        # Net.traffic[iii][3] = 0
                        if ii in Recording:
                            Recording[ii].append([iii, ii])
                        else:
                            Recording[ii] = [[iii, ii]]
                        # print(Recording)
                        for n in [k for k in Recording.values()]:
                            for nn in n:
                                for nnn in [k for k in sorted_goable_nodes_1.keys()]:
                                    if nn[0] in sorted_goable_nodes_1[nnn]:
                                        sorted_goable_nodes_1[nnn].remove(nn[0])
                                        if nn[0] in no_MEC_yet_in_the_end:# delete from Unacivated
                                            no_MEC_yet_in_the_end.remove(nn[0])
                    else:
                        rest_from_activated[ii] = sorted_goable_nodes_1[ii]
                        del sorted_goable_nodes_1[ii]
                    if ii in sorted_goable_nodes_1:
                        if sorted_goable_nodes_1[ii] == []:
                            del sorted_goable_nodes_1[ii]
                    break
                break
            break

    for i in Traffic_to_Core: # move the traffic that is going to the core
        if i in no_MEC_yet_in_the_end:
            no_MEC_yet_in_the_end.remove(i)

    for i in [k for k in Recording.values()]:
        for ii in i:
            for iii in [k for k in paths_from_Unactivated_to_activated.keys()]:
                if ii[0] + '-' + ii[1] == iii:
                    temp_copy = copy.deepcopy(paths_from_Unactivated_to_activated)
                    for iiii in temp_copy[iii]:
                        if iiii[-1] > Net.traffic[ii[0]][1]:
                            paths_from_Unactivated_to_activated[iii].remove(iiii)

    Recording_of_the_paths = {}
    for i in [k for k in Recording.values()]:
        for ii in i:
            for iii in [k for k in paths_from_Unactivated_to_activated.keys()]:
                if ii[0] + '-' + ii[1] == iii:
                    Recording_of_the_paths[ii[0] + '-' + ii[1]] = paths_from_Unactivated_to_activated[ii[0] + '-' + ii[1]]
    for i in [k for k in Recording.values()]: # put e.g.[node7, node7, 0] in to path_recording
        for ii in i:
            if ii[0] == ii[1]:
                Recording_of_the_paths[ii[0] + '-' + ii[1]] = [[ii[0], ii[1], 0]]
    # print(Recording_of_the_paths)
    return no_MEC_yet_in_the_end, Recording_of_the_paths


# future interface to change the size
Size_decrease_ratio = 0.2

PP1_DU_size = 50.1

PP2_CU_size = 50.1 #Gbps
PP2_DU_size = 50.1 #Gbps
PP2_MEC_size = 32.1

PP3_CU_size = 50.1
PP3_DU_size = 50.1
PP3_MEC_size = 50.1

DC_size = 10000

# Core = 'Node12'

Initial_Bandwidth = 50

Fronthaul_BW = 25
BackHaul_BW = Fronthaul_BW * Size_decrease_ratio

BW_divided = 50

# Build the network
Net = Network()
Net.addVertex('Node1', 1, 0, 0, PP1_DU_size)
Net.addVertex('Node2', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
Net.addVertex('Node3', 1, 0, 0, PP1_DU_size)
Net.addVertex('Node4', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
Net.addVertex('Node5', 1, 0, 0, PP1_DU_size)
Net.addVertex('Node6', 1, 0, 0, PP1_DU_size)
Net.addVertex('Node7', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
Net.addVertex('Node8', 1, 0, 0, PP1_DU_size)
Net.addVertex('Node9', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
Net.addVertex('Node10', 1, 0, 0, PP1_DU_size)
Net.addVertex('Node11', 3, PP3_MEC_size, PP3_CU_size, PP3_DU_size)
Net.addVertex('Node12', 3, PP3_MEC_size, PP3_CU_size, PP3_DU_size)
Net.addVertex('Node13', 3, PP3_MEC_size, PP3_CU_size, PP3_DU_size)
Net.addVertex('Node14', 3, PP3_MEC_size, PP3_CU_size, PP3_DU_size)

Net.addEdge('Node1', 'Node2', 10)
Net.addEdge('Node1', 'Node11', 9)
Net.addEdge('Node1', 'Node10', 13)
Net.addEdge('Node2', 'Node3', 12)
Net.addEdge('Node2', 'Node12', 11)
Net.addEdge('Node2', 'Node11', 11)
Net.addEdge('Node3', 'Node4', 13)
Net.addEdge('Node3', 'Node12', 9)
Net.addEdge('Node4', 'Node5', 6)
Net.addEdge('Node4', 'Node5', 15)
Net.addEdge('Node4', 'Node13', 13)
Net.addEdge('Node4', 'Node12', 8)
Net.addEdge('Node5', 'Node6', 13)
Net.addEdge('Node5', 'Node13', 8)
Net.addEdge('Node6', 'Node7', 14)
Net.addEdge('Node6', 'Node13', 11)
Net.addEdge('Node7', 'Node8', 9)
Net.addEdge('Node7', 'Node14', 13)
Net.addEdge('Node7', 'Node13', 14)
Net.addEdge('Node8', 'Node9', 10)
Net.addEdge('Node8', 'Node14', 8)
Net.addEdge('Node9', 'Node10', 8)
Net.addEdge('Node9', 'Node11', 10)
Net.addEdge('Node9', 'Node14', 11)
Net.addEdge('Node10', 'Node11', 11)
Net.addEdge('Node11', 'Node12', 11)
Net.addEdge('Node11', 'Node14', 13)
Net.addEdge('Node12', 'Node13', 16)
Net.addEdge('Node12', 'Node14', 12)
Net.addEdge('Node13', 'Node14', 12)
# Net.addVertex('Node1', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node2', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node3', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node4', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node5', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
# Net.addVertex('Node6', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
# Net.addVertex('Node7', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node8', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node9', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node10', 3, PP3_MEC_size, PP3_CU_size, PP3_DU_size)
# Net.addVertex('Node11', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node12', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node13', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node14', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
# Net.addVertex('Node15', 2, PP2_MEC_size, PP2_CU_size, PP2_DU_size)
# Net.addVertex('Node16', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node17', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node18', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node19', 1, 0, 0, PP1_DU_size)
# Net.addVertex('Node20', 4, DC_size, 0, 0)
#
# Net.addEdge('Node1', 'Node2', 13)
# Net.addEdge('Node1', 'Node6', 11)
# Net.addEdge('Node1', 'Node7', 8)
# Net.addEdge('Node2', 'Node3', 15)
# Net.addEdge('Node2', 'Node5', 10)
# Net.addEdge('Node2', 'Node6', 9)
# Net.addEdge('Node3', 'Node4', 14)
# Net.addEdge('Node3', 'Node5', 16)
# Net.addEdge('Node4', 'Node5', 12)
# Net.addEdge('Node4', 'Node11', 9)
# Net.addEdge('Node4', 'Node12', 13)
# Net.addEdge('Node5', 'Node6', 10)
# Net.addEdge('Node5', 'Node10', 11)
# Net.addEdge('Node5', 'Node11', 10)
# Net.addEdge('Node6', 'Node7', 11)
# Net.addEdge('Node6', 'Node9', 8)
# Net.addEdge('Node6', 'Node10', 13)
# Net.addEdge('Node7', 'Node8', 12)
# Net.addEdge('Node7', 'Node9', 11)
# Net.addEdge('Node8', 'Node9', 9)
# Net.addEdge('Node8', 'Node16', 13)
# Net.addEdge('Node9', 'Node10', 12)
# Net.addEdge('Node9', 'Node15', 16)
# Net.addEdge('Node9', 'Node16', 8)
# Net.addEdge('Node10', 'Node11', 8)
# Net.addEdge('Node10', 'Node14', 13)
# Net.addEdge('Node10', 'Node15', 12)
# Net.addEdge('Node11', 'Node12', 15)
# Net.addEdge('Node11', 'Node13', 11)
# Net.addEdge('Node11', 'Node14', 9)
# Net.addEdge('Node12', 'Node13', 12)
# Net.addEdge('Node13', 'Node14', 15)
# Net.addEdge('Node13', 'Node19', 10)
# Net.addEdge('Node14', 'Node15', 14)
# Net.addEdge('Node14', 'Node18', 14)
# Net.addEdge('Node14', 'Node19', 16)
# Net.addEdge('Node15', 'Node16', 13)
# Net.addEdge('Node15', 'Node17', 8)
# Net.addEdge('Node15', 'Node18', 11)
# Net.addEdge('Node16', 'Node17', 15)
# Net.addEdge('Node17', 'Node18', 13)
# Net.addEdge('Node18', 'Node19', 9)

# Net.addEdge('Node12', 'Node20', 70)

for i in Net.getVertics():
    neigh = Net.vertList[i].getConnections()
    for ii in neigh:
        if str(i) + '-' + str(ii) not in Net.bandwidth and str(ii) + '-' + str(i) not in Net.bandwidth:
            Net.bandwidth[str(i) + '-' + str(ii)] = Initial_Bandwidth
# print(Net.bandwidth)


# Traffic, destination is unknown, we only the [fronthaul delay, e-e delay, cycles, data_size]
# These are background input, can be changed
left_ratio = 1 # how much MEC computing resource left
# Net.traffic = {'Node1': [16, 30, 4, 10], 'Node2': [10, 28, 4, 10], 'Node3': [15, 35, 4, 10],
#                'Node4': [13, 32, 4, 10], 'Node5': [15, 40, 4, 10], 'Node6': [12, 30, 4, 10], 'Node7': [11, 32, 4, 10],
#                'Node8': [16, 30, 4, 10], 'Node9': [20, 32, 4, 10], 'Node10': [11, 32, 4, 10], 'Node11': [11, 42, 4, 10],
#                'Node12': [11, 28, 4, 10], 'Node13': [11, 32, 4, 10], 'Node14': [20, 50, 4, 10]}
#                'Node15': [17, 36, 4, 10],
#                'Node16': [11, 28, 4, 10], 'Node17': [16, 30, 4, 10], 'Node18': [11, 40, 4, 10], 'Node19': [18, 45, 4, 10]}



Net.traffic = {'Node1': [14.0, 28.0, 3.0, 11.0], 'Node2': [20.0, 38.0, 4.0, 9.0], 'Node3': [17.0, 40.0, 5.0, 8.0], 'Node4': [19.0, 29.0, 5.0, 9.0], 'Node5': [19.0, 41.0, 3.0, 9.0], 'Node6': [17.0, 32.0, 3.0, 8.0], 'Node7': [17.0, 34.0, 5.0, 10.0], 'Node8': [17.0, 42.0, 3.0, 11.0], 'Node9': [13.0, 37.0, 3.0, 10.0], 'Node10': [15.0, 29.0, 3.0, 9.0], 'Node11': [20.0, 28.0, 3.0, 8.0], 'Node12': [18.0, 31.0, 3.0, 10.0], 'Node13': [16.0, 28.0, 5.0, 9.0], 'Node14': [11.0, 31.0, 3.0, 9.0]}



PP2_or_PP3 = []
for i in [k for k in Net.vertList.keys()]:
    if Net.vertList[i].resource[0] != 0:
        PP2_or_PP3.append(i)
PP2_or_PP3 = PP2_or_PP3[:-1]
# print('PP2 or PP3:')
# print(PP2_or_PP3)

Activated_node = {'Node2': [PP2_MEC_size * left_ratio, PP2_CU_size, PP2_DU_size], 'Node9': [PP2_MEC_size * left_ratio, PP2_CU_size, PP2_DU_size]} #'Node4': [PP2_MEC_size * left_ratio, PP2_CU_size, PP2_DU_size, Node7': [PP3_MEC_size * left_ratio, PP3_CU_size, PP3_DU_size]}# which one is activated, and how much traffic left
# NOTION!: only MEC resource / 2, because CU DU will immediately become free after use, but not MEC
for i in Activated_node: # 更新Net里resource的数值
    Net.vertList[i].resource = Activated_node[i]

Unactivated_PP2_PP3 = copy.deepcopy(PP2_or_PP3)
for i in [k for k in Activated_node.keys()]:
    Unactivated_PP2_PP3.remove(i)
Unactivated_PP2_PP3_dict = {}
for i in Unactivated_PP2_PP3:
    Unactivated_PP2_PP3_dict[i] = copy.deepcopy(Net.vertList[i].resource)

for i in Net.getVertics():
    Net.vertList[i].setStatus('F')

# STAGE 1 #
Traffic_to_Core = [] # Which traffic that will go to the core
for i in [k for k in Net.traffic.keys()]:
    if Net.traffic[i][1] >= 100: 
        Traffic_to_Core.append(i)
# print(Traffic_to_Core)

How_to_go_to_core = {}
for i in Traffic_to_Core:
    if i not in How_to_go_to_core:
        How_to_go_to_core[i] = Net.find_the_paths(i, Core, [], [])

# print(How_to_go_to_core)
distance_copied_from = {} # only the distance, paths_from_Unactivated include both path and distance
for i in [k for k in How_to_go_to_core.keys()]:
    distance_copied_from[i] = []
for i in [k for k in How_to_go_to_core.keys()]:
    for ii in range(len(How_to_go_to_core[i])):
        length = 0
        q = 0
        while q < len(How_to_go_to_core[i][ii]) - 1:
            dis = Net.vertList[How_to_go_to_core[i][ii][q]].getWeight(How_to_go_to_core[i][ii][q + 1])
            length += dis
            q += 1
        distance_copied_from[i].append(length)
        How_to_go_to_core[i][ii].append(length) # put the distance information into the links
# print(distance_copied_from)

How_to_go_to_core_1 = copy.deepcopy(How_to_go_to_core)
for i in [k for k in How_to_go_to_core.keys()]:
    for ii in How_to_go_to_core[i]:
        if ii[-1] > Net.traffic[i][1]:
            How_to_go_to_core_1[i].remove(ii)
# print(How_to_go_to_core_1)
# print(1)
def find_pairs(How_to_go_to_core_1):
    links = [k for k in How_to_go_to_core_1.values()]
    links_copy = copy.deepcopy(links)
    all_node_all_path_record = {}
    for path in links_copy:
        path_copy_1 = copy.deepcopy(path)
        target = path[0][-2]
        i = path[0][0]
        for ii in range(len(path)):
            path[ii] = path[ii][1:]
            path_copy_1[ii] = path_copy_1[ii][1:]
            path[ii] = path[ii][:-2]
            xx = path_copy_1[ii][-1]
            path_copy_1[ii] = path_copy_1[ii][:-2]
            path_copy_1[ii].append(xx)
        usable_paths_in_all_paths = []
        for n in range(len(path)):
            path_copy = copy.deepcopy(path)
            for m in range(len(path_copy)):
                set1 = set(path[n])
                set2 = set(path_copy[m])
                if path_copy[m] != path[n]:
                    if list(set1 & set2) == []:
                       if [path_copy_1[m], path_copy_1[n]] not in usable_paths_in_all_paths:
                           usable_paths_in_all_paths.append([path_copy_1[n], path_copy_1[m]])
        for j in usable_paths_in_all_paths:
            for jj in j:
                if jj[:-1] == []:
                    jj.insert(0, target)
                    jj.insert(0, i)
        for j in usable_paths_in_all_paths:
            for jj in j:
                if jj[0] != i:
                    jj.insert(0, i)
                    jj.insert(-1, target)
        all_node_all_path_record[i] = usable_paths_in_all_paths
    return all_node_all_path_record

path_pair_to_core = find_pairs(How_to_go_to_core_1)

# print(1.5)
# STAGE 2 #
# Stage 2.1, using the activated devices #
# Stage 2.1, whether they are enough, so we don't need to activate new one #
Unactivated = [k for k in Net.traffic.keys()]
for i in Traffic_to_Core: # remove the nodes  will go to core
    if i in Unactivated:
        Unactivated.remove(i)
activated = [k for k in Activated_node.keys()]
for i in activated:  # remove the activated node cause they select themself
    if i in Unactivated:
        Unactivated.remove(i)

paths_from_Unactivated_to_activated = {}
for i in Unactivated:
    for target in activated:
        path = Net.find_the_paths(i, target, [], [])
        paths_from_Unactivated_to_activated[i+'-' +target] = path

distance = {} # only the distance, paths_from_Unactivated include both path and distance
for i in [k for k in paths_from_Unactivated_to_activated.keys()]:
    distance[i] = []
for i in [k for k in paths_from_Unactivated_to_activated.keys()]:
    for ii in range(len(paths_from_Unactivated_to_activated[i])):
        length = 0
        q = 0
        while q < len(paths_from_Unactivated_to_activated[i][ii]) - 1:
            dis = Net.vertList[paths_from_Unactivated_to_activated[i][ii][q]].getWeight(paths_from_Unactivated_to_activated[i][ii][q + 1])
            length += dis
            q += 1
        distance[i].append(length)
        paths_from_Unactivated_to_activated[i][ii].append(length) # put the distance information into the links
# print(distance)
# print(paths_from_Unactivated_to_activated)

# record the activated node
goable_nodes = {} # which nodes can go the activated nodes
Ungoable_nodes = []
for i in Unactivated:
    for ii in activated:
        if Net.traffic[i][1] >= min(distance[i + '-' + ii]):
            if ii in goable_nodes:
                goable_nodes[ii].append(i)
            else:
                goable_nodes[ii] = [i]
        else:
            Ungoable_nodes.append(i + '-' + ii)
# print(goable_nodes)
# print(Ungoable_nodes)
# print(2)
# sort the first fit order. e.g. 7:[2,3,4,5]  3[2,3,4]. If use 7 to solve 3,4,5, waste 3
# so processing based on the emerging time, the less, the higher possibility to be solved
overall_nodes_to_all_activated = []
for i in [k for k in goable_nodes.values()]:
    for ii in i:
        overall_nodes_to_all_activated.append(ii)

result = Counter(overall_nodes_to_all_activated)
values = [k for k in result.values()]
keys = [k for k in result.keys()]
zip_two = zip(keys, values) 
sorted_keys_values = sorted(zip_two, key=lambda x:x[1])
output = zip(*sorted_keys_values)
sorted_keys, sorted_values = [list(x) for x in output]

for i in [k for k in goable_nodes.keys()]:
    arr1 = sorted_keys
    goable_nodes[i].sort(key=arr1.index) # 按照已有顺序排序

sorted_goable_nodes = copy.deepcopy(goable_nodes)
for i in [k for k in goable_nodes.keys()]:
    sorted_goable_nodes[i].insert(0, i)

# print('123')
# print(sorted_goable_nodes)
# print(Net.vertList['Node3'].resource)

# print(sorted_goable_nodes.values())
Recording = {}        # Recording the node-node-node path, distance
copy1 = {}
rest_from_activated = copy.deepcopy(sorted_goable_nodes)
no_MEC_yet = copy.deepcopy(Net.getVertics()[:-1]) # MEC is not settled
while copy1 != sorted_goable_nodes:
    copy1 = copy.deepcopy(sorted_goable_nodes)
    for ii in [k for k in sorted_goable_nodes.keys()]:
        for i in [k for k in sorted_goable_nodes.values()]:
            for iii in i:
                if Net.traffic[iii][2] <= Activated_node[ii][0]: 
                    Activated_node[ii][0] = Activated_node[ii][0] - Net.traffic[iii][2]
                    Net.traffic[iii][2] = 0
                    if ii in Recording:
                        Recording[ii].append([iii, ii])
                    else:
                        Recording[ii] = [[iii, ii]]
                    # print(Recording)
                    for n in [k for k in Recording.values()]:
                        for nn in n:
                            for nnn in [k for k in sorted_goable_nodes.keys()]:
                                if nn[0] in sorted_goable_nodes[nnn]:
                                    sorted_goable_nodes[nnn].remove(nn[0])
                                    if nn[0] in no_MEC_yet:# delete from Unacivated
                                        no_MEC_yet.remove(nn[0])
                else:
                    rest_from_activated[ii] = sorted_goable_nodes[ii]
                    del sorted_goable_nodes[ii]
                if ii in sorted_goable_nodes:
                    if sorted_goable_nodes[ii] == []:
                        del sorted_goable_nodes[ii]
                break
            break
        break
# print(no_MEC_yet)
# print(Net.vertList['Node3'].resource)
# print(Recording)


for i in Traffic_to_Core: # move the traffic that is going to the core
    if i in no_MEC_yet:
        no_MEC_yet.remove(i)


for i in [k for k in Recording.values()]:
    for ii in i:
        for iii in [k for k in paths_from_Unactivated_to_activated.keys()]:
            if ii[0] + '-' + ii[1] == iii:
                temp_copy = copy.deepcopy(paths_from_Unactivated_to_activated)
                for iiii in temp_copy[iii]:
                    if iiii[-1] > Net.traffic[ii[0]][1]:
                        paths_from_Unactivated_to_activated[iii].remove(iiii)

Recording_of_the_paths = {}
for i in [k for k in Recording.values()]:
    for ii in i:
        for iii in [k for k in paths_from_Unactivated_to_activated.keys()]:
            if ii[0] + '-' + ii[1] == iii:
                Recording_of_the_paths[ii[0] + '-' + ii[1]] = paths_from_Unactivated_to_activated[ii[0] + '-' + ii[1]]
for i in [k for k in Recording.values()]: # put e.g.[node7, node7, 0] in to path_recording
    for ii in i:
        if ii[0] == ii[1]:
            Recording_of_the_paths[ii[0] + '-' + ii[1]] = [[ii[0], ii[1], 0]]
# print(Recording_of_the_paths)

# print(3)
if 'Node20' in no_MEC_yet:
    no_MEC_yet.remove('Node20')

overlap_time_dictionary = {}
for i in Unactivated_PP2_PP3:
    for ii in no_MEC_yet:
        shorest_path_from, shorest_distance_from = find_the_shrest_path(ii, i)
        if shorest_distance_from < Net.traffic[ii][1]:
            if i in overlap_time_dictionary:
                overlap_time_dictionary[i] += 1
            else:
                overlap_time_dictionary[i] = 1
keys_1 = [k for k in overlap_time_dictionary.keys()]
values_1 = [k for k in overlap_time_dictionary.values()]
zip_two_1 = zip(keys_1, values_1) 
sorted_keys_values_1 = sorted(zip_two_1, key=lambda x:x[1])
output_1 = zip(*sorted_keys_values_1)
sorted_keys_1, sorted_values_1 = [list(x) for x in output_1]
sorted_keys_1.reverse()
sorted_values_1.reverse()

Might_activated = {}
for i in sorted_keys_1:
    Might_activated[i] = Net.vertList[i].resource

reference_activated = copy.deepcopy(Might_activated)
no_MEC_in_the_end, Recording_of_the_paths_2 = chose_the_MEC(no_MEC_yet, Might_activated) 
print('no MEC in the end')
print(no_MEC_in_the_end) 
# print(Recording_of_the_paths_2)

for i in [k for k in Net.traffic.keys()]:
    for ii in no_MEC_in_the_end:
        if ii == i:
            del Net.traffic[i]

for i in [k for k in Might_activated.keys()]:
    if Might_activated[i] != reference_activated[i]:
        Activated_node[i] = Might_activated[i]

Recording_of_the_paths_end = copy.deepcopy(Recording_of_the_paths)
for i in [k for k in Recording_of_the_paths_2.keys()]:
    Recording_of_the_paths_end[i] = Recording_of_the_paths_2[i]

# print(Recording_of_the_paths_end)

links = [k for k in Recording_of_the_paths_end.values()]
links_copy = copy.deepcopy(links)
only_one_way_to_go_MEC = {}
for i in links:
    if len(i) == 1:
        links_copy.remove(i)
        only_one_way_to_go_MEC[i[0][0]] = i
print('only_one_way_to_go_MEC')
print('mention here')
print(only_one_way_to_go_MEC) 

for i in only_one_way_to_go_MEC.keys():
    if i == only_one_way_to_go_MEC[i][0][-2]:
        Net.vertList[i].resource[2] -= Net.traffic[i][-1]
        Net.vertList[i].resource[1] -= Net.traffic[i][-1] * Size_decrease_ratio
    else: 
        Net.vertList[i].resource[1] -= Net.traffic[i][-1] * Size_decrease_ratio


no_backup_to_use = {}
rest_unused_path = {}
all_node_all_path_record = {}
for path in links_copy:
    path_copy_1 = copy.deepcopy(path)
    target = path[0][-2]
    i = path[0][0]
    for ii in range(len(path)):
        path[ii] = path[ii][1:]
        path_copy_1[ii] = path_copy_1[ii][1:]
        path[ii] = path[ii][:-2]
        xx = path_copy_1[ii][-1]
        path_copy_1[ii] = path_copy_1[ii][:-2]
        path_copy_1[ii].append(xx)
    usable_paths_in_all_paths = []
    for n in range(len(path)):
        path_copy = copy.deepcopy(path)
        for m in range(len(path_copy)):
            set1 = set(path[n])
            set2 = set(path_copy[m])
            if path_copy[m] != path[n]:
                if list(set1 & set2) == []:
                   if [path_copy_1[m], path_copy_1[n]] not in usable_paths_in_all_paths:
                       usable_paths_in_all_paths.append([path_copy_1[n], path_copy_1[m]])
    for j in usable_paths_in_all_paths:
        for jj in j:
            if jj[:-1] == []:
                jj.insert(0, target)
                jj.insert(0, i)
    for j in usable_paths_in_all_paths:
        for jj in j:
            if jj[0] != i:
                jj.insert(0, i)
                jj.insert(-1, target)
    all_node_all_path_record[i] = usable_paths_in_all_paths

###### no_backup_to_use, except only one way ######
print(all_node_all_path_record)
print(Recording_of_the_paths_end)

for i in [k for k in all_node_all_path_record.keys()]:
    if all_node_all_path_record[i] == []:
        for ii in [k for k in Recording_of_the_paths_end.keys()]:
            if i in ii:
                no_backup_to_use[i] = Recording_of_the_paths_end[ii]
                del all_node_all_path_record[i]
                break

################################################# end point ########################################
print(' no backup to use ')
print(no_backup_to_use)
print(all_node_all_path_record)

MEC = []
for i in all_node_all_path_record.keys():
    MEC.append(all_node_all_path_record[i][0][0][-2])
for i in only_one_way_to_go_MEC.keys():
    if only_one_way_to_go_MEC[i][0][-2] not in MEC:
        MEC.append(only_one_way_to_go_MEC[i][0][-2])

for i in [k for k in path_pair_to_core.keys()]:
    if i not in all_node_all_path_record:
        all_node_all_path_record[i] = path_pair_to_core[i]

record_list = []
for i in [k for k in all_node_all_path_record.keys()]:
    for ii in all_node_all_path_record[i]:
        for iii in ii:
            if iii not in record_list:
                record_list.append(iii)
record_list_1 = []
for i in links:
    for ii in i:
        if ii not in record_list_1:
            record_list_1.append(ii)
for i in record_list_1:
    if i not in record_list:
        if i[0] not in rest_unused_path:
            rest_unused_path[i[0]] = i
        else:
            rest_unused_path[i[0]].append(i)
for i in [k for k in only_one_way_to_go_MEC.keys()]:
    if i in [k for k in rest_unused_path.keys()]:
        del rest_unused_path[i]

all_DU = copy.deepcopy(all_node_all_path_record)
for i in [k for k in all_DU.keys()]:
    for ii in range(len(all_DU[i])):
        for iii in range(len(all_DU[i][ii])):
            all_DU[i][ii][iii] = []

for i in [k for k in all_node_all_path_record.keys()]:
    for ii in range(len(all_node_all_path_record[i])):
        for iii in range(len(all_node_all_path_record[i][ii])):
            iiii = 0
            d = 0
            if iiii == 0:
                all_DU[i][ii][iii].append(all_node_all_path_record[i][ii][iii][iiii])
            while iiii < len(all_node_all_path_record[i][ii][iii]) - 2:
                d += Net.vertList[all_node_all_path_record[i][ii][iii][iiii]].getWeight(all_node_all_path_record[i][ii][iii][iiii + 1])
                if d <= Net.traffic[i][0]:
                    all_DU[i][ii][iii].append(all_node_all_path_record[i][ii][iii][iiii + 1])
                iiii += 1


Activated_PP1 = {} # 'Node2':[0, 0, PP1_DU_size]
DU = {}
for i in [k for k in Activated_node.keys()]:
    Net.vertList[i].resource[2] -= Net.traffic[i][-1]
    DU[i] = Net.vertList[i].resource

predeleted = {}
for i in [k for k in Activated_PP1.keys()]: 
    # Net.vertList[i].resource[2] -= Net.traffic[i][-1]
    DU[i] = Net.vertList[i].resource
    if i in all_DU: 
        predeleted[i] = all_DU[i]
        del all_DU[i]

for i in [k for k in all_DU.keys()]:
    ii = 0
    xx = 0
    while ii < len(all_DU[i]):
        if len(all_DU[i][ii][0]) == 1 and len(all_DU[i][ii][1]) == 1:
            xx += 1
        ii += 1
    if ii == xx:
        DU[i] = Net.vertList[i].resource
        predeleted[i] = all_DU[i]
        del all_DU[i]
# print('DU')
# print(DU)
# print(all_DU)
# print(all_node_all_path_record)


for i in [k for k in all_DU.keys()]:
    for ii in range(len(all_DU[i])):
        for iii in range(len(all_DU[i][ii])):
            all_DU[i][ii][iii].append(len(all_node_all_path_record[i][ii][iii]) - 1)
# print('all_DU')
# print(all_DU)

which_DU_selected = {} 
which_include_existed_PP1 = {}
for i in [k for k in all_DU.keys()]:
    for ii in all_DU[i]:
        for iii in ii:
            for n in [k for k in DU.keys()]:
                if n in iii:
                    if i not in which_include_existed_PP1:
                        which_include_existed_PP1[i] = [ii]
                    elif i in which_include_existed_PP1 and ii not in which_include_existed_PP1[i]:
                        which_include_existed_PP1[i].append(ii)
rest_need_new_PP1 = {}
for i in [k for k in all_DU.keys()]:
    if i not in which_include_existed_PP1:
        rest_need_new_PP1[i] = all_DU[i]
# print('rest_need_new_PP1')
# print(rest_need_new_PP1)
# print(rest_need_new_PP1)
# print('')
# print('which_include_existed_PP1:')
# print(which_include_existed_PP1)
copy_for_rest = copy.deepcopy(which_include_existed_PP1)

left_not_included_existed_PP1 = {}
for i in [k for k in all_node_all_path_record.keys()]:
    if i not in [k for k in which_include_existed_PP1.keys()]:
        left_not_included_existed_PP1[i] = copy.deepcopy(all_node_all_path_record[i])

record_the_hops = {}
for i in [k for k in which_include_existed_PP1.keys()]:
    if i not in record_the_hops:
        record_the_hops[i] = []

for i in [k for k in which_include_existed_PP1.keys()]:
    for ii in which_include_existed_PP1[i]:
        ii.append(ii[0][-1] + ii[1][-1])
        record_the_hops[i].append(ii[0][-1] + ii[1][-1])


for i in [k for k in record_the_hops.keys()]:
    second = which_include_existed_PP1[i]
    first = record_the_hops[i]
    zip_FS = zip(second, first)
    sorted_fs = sorted(zip_FS, key=lambda x:x[1])
    output_fs = zip(*sorted_fs)
    sorted_second, sorted_first = [list(x) for x in output_fs]
    which_include_existed_PP1[i] = sorted_second
# print('which_include_existed_PP1')
# print(which_include_existed_PP1)

for i in [k for k in record_the_hops.keys()]:
    second = all_node_all_path_record[i]
    first = record_the_hops[i]
    zip_FS = zip(second, first)
    sorted_fs = sorted(zip_FS, key=lambda x:x[1])
    output_fs = zip(*sorted_fs)
    sorted_second, sorted_first = [list(x) for x in output_fs]
    all_node_all_path_record[i] = sorted_second

# print('all_node_all_path_record')
# print(all_node_all_path_record)

# print(Net.bandwidth)
# print(which_include_existed_PP1['Node1'][0])
daikuan = copy.deepcopy(Net.bandwidth)
allpath = {}
working = {}
which_PP1_used = {}
print(7)
flage = False
for i in [k for k in which_include_existed_PP1.keys()]:
    for ii in range(len(which_include_existed_PP1[i])):
        flage = False
        # print(which_include_existed_PP1[i][ii])
        for iii in [k for k in DU.keys()]:
            # 这里是在这一个pair中，选择hop数目少的作为working path
            if iii in which_include_existed_PP1[i][ii][0] or iii in which_include_existed_PP1[i][ii][1]:
                wp = 0 # working_path
                if iii in which_include_existed_PP1[i][ii][0] and iii not in which_include_existed_PP1[i][ii][1]:
                    wp = 0
                elif iii in which_include_existed_PP1[i][ii][1] and iii not in which_include_existed_PP1[i][ii][0]:
                    wp = 1
                elif which_include_existed_PP1[i][ii][0][-1] >= which_include_existed_PP1[i][ii][1][-1]:
                    wp = 1
                elif which_include_existed_PP1[i][ii][0][-1] < which_include_existed_PP1[i][ii][1][-1]:
                    wp = 0
                if Net.vertList[iii].resource[2] > Net.traffic[i][3]: 
                    n = 0
                    while n < len(which_include_existed_PP1[i][ii][wp]) - 2:
                        if str(which_include_existed_PP1[i][ii][wp][n]) + '-' + \
                                str(which_include_existed_PP1[i][ii][wp][n + 1]) in daikuan:
                            daikuan[str(which_include_existed_PP1[i][ii][wp][n]) + '-' +
                                    str(which_include_existed_PP1[i][ii][wp][n + 1])] -= Net.traffic[i][3]
                        else: 
                            daikuan[str(which_include_existed_PP1[i][ii][wp][n + 1]) + '-' +
                                    str(which_include_existed_PP1[i][ii][wp][n])] -= Net.traffic[i][3]
                        n += 1
                    m = 0
                    while m < len(all_node_all_path_record[i][ii][wp]) - n - 2:
                        if str(all_node_all_path_record[i][ii][wp][n + m]) + '-' \
                                + str(all_node_all_path_record[i][ii][wp][n + m + 1]) in daikuan:
                            daikuan[str(all_node_all_path_record[i][ii][wp][n + m]) + '-'
                                    + str(all_node_all_path_record[i][ii][wp][n + m + 1])] \
                                -= Net.traffic[i][3] / 100 * Size_decrease_ratio
                        else:
                            daikuan[str(all_node_all_path_record[i][ii][wp][n + m + 1]) + '-'
                                    + str(all_node_all_path_record[i][ii][wp][n + m])] \
                                -= Net.traffic[i][3] / 100 * Size_decrease_ratio
                        m += 1
                    if (np.array([k for k in daikuan.values()]) >= 0).all() == False:
                        daikuan = copy.deepcopy(Net.bandwidth)
                    elif (np.array([k for k in daikuan.values()]) >= 0).all() == True:
                        nn = 0
                        while nn < len(which_include_existed_PP1[i][ii][wp]) - 2:
                            if str(which_include_existed_PP1[i][ii][wp][nn]) + '-' + \
                                    str(which_include_existed_PP1[i][ii][wp][nn + 1]) in Net.bandwidth:
                                Net.bandwidth[str(which_include_existed_PP1[i][ii][wp][nn]) + '-' +
                                        str(which_include_existed_PP1[i][ii][wp][nn + 1])] -= Net.traffic[i][3]
                            else:
                                Net.bandwidth[str(which_include_existed_PP1[i][ii][wp][nn + 1]) + '-' +
                                        str(which_include_existed_PP1[i][ii][wp][nn])] -= Net.traffic[i][3]
                            nn += 1
                        mm = 0
                        while mm < len(all_node_all_path_record[i][ii][wp]) - nn - 2:
                            if str(all_node_all_path_record[i][ii][wp][nn + mm]) + '-' \
                                + str(all_node_all_path_record[i][ii][wp][nn + mm + 1]) in Net.bandwidth:
                                Net.bandwidth[str(all_node_all_path_record[i][ii][wp][nn + mm]) + '-'
                                        + str(all_node_all_path_record[i][ii][wp][nn + mm + 1])] \
                                    -= Net.traffic[i][3]  * Size_decrease_ratio
                            else:
                                Net.bandwidth[str(all_node_all_path_record[i][ii][wp][nn + mm + 1]) + '-'
                                              + str(all_node_all_path_record[i][ii][wp][nn + mm])] \
                                    -= Net.traffic[i][3]  * Size_decrease_ratio
                            mm += 1
                        Net.vertList[iii].resource[2] -= Net.traffic[i][3]
                        allpath[i] = all_node_all_path_record[i][ii]
                        working[i] = all_node_all_path_record[i][ii][wp]
                        which_PP1_used[i] = iii
                        daikuan = copy.deepcopy(Net.bandwidth)
                        flage = True
                        break
                    if flage:
                        break
                if flage:
                    break
            if flage:
                break
        if flage:
            break


for i in [k for k in predeleted.keys()]:
    for ii in range(len(predeleted[i])):
        for iii in range(len(predeleted[i][ii])):
            predeleted[i][ii][iii].append(len(all_node_all_path_record[i][ii][iii]) - 1)

for i in [k for k in which_include_existed_PP1.keys()]:  
    if i not in [k for k in which_PP1_used]:
        rest_need_new_PP1[i] = copy.deepcopy(copy_for_rest[i])
for i in [k for k in predeleted.keys()]:  
    if i not in [k for k in which_PP1_used]:
        rest_need_new_PP1[i] = copy.deepcopy(predeleted[i])
# print('rest_need_new_PP1:')
# print(rest_need_new_PP1)
#
record_the_hops_1 = {}
for i in [k for k in rest_need_new_PP1.keys()]:
    if i not in record_the_hops_1:
        record_the_hops_1[i] = []

for i in [k for k in rest_need_new_PP1.keys()]:
    for ii in rest_need_new_PP1[i]:
        ii.append(ii[0][-1] + ii[1][-1])
        record_the_hops_1[i].append(ii[0][-1] + ii[1][-1])

for i in [k for k in record_the_hops_1.keys()]:
    second = rest_need_new_PP1[i]
    first = record_the_hops_1[i]
    zip_FS = zip(second, first)
    sorted_fs = sorted(zip_FS, key=lambda x:x[1])
    output_fs = zip(*sorted_fs)
    sorted_second, sorted_first = [list(x) for x in output_fs]
    rest_need_new_PP1[i] = sorted_second
print('rest_need_new_PP1')
print(rest_need_new_PP1)

for i in [k for k in record_the_hops_1.keys()]:
    second = all_node_all_path_record[i]
    first = record_the_hops_1[i]
    zip_FS = zip(second, first)
    sorted_fs = sorted(zip_FS, key=lambda x:x[1])
    output_fs = zip(*sorted_fs)
    sorted_second, sorted_first = [list(x) for x in output_fs]
    all_node_all_path_record[i] = sorted_second


# In the end, the original activated points may not be enough. At this time, the remaining points should be combined with the originally removed points to find the maximum overlap point. If the maximum overlap point is an existing point, delete it directly. Reselect
# Finding the maximum point actually means drawing circles to find the maximum overlap point, and also needs to do some bandwidth management.
# You have to find a place to add Node1, because it is not a hop connection
all_the_PP1s_without_times = []
for u in [k for k in rest_need_new_PP1]:
    for i in rest_need_new_PP1[u]:
        for ii in i[:-1]:
            for iii in ii[1:-1]:
                if i != iii:
                    all_the_PP1s_without_times.append(iii)
for i in [k for k in rest_need_new_PP1.keys()]:
    all_the_PP1s_without_times.append(i)
# print('all_the_PP1s_without_times:')
# print(all_the_PP1s_without_times)

count_for = Counter(all_the_PP1s_without_times)
values_of_count_for = [k for k in count_for.values()]
keys_of_count_for = [k for k in count_for.keys()]

zip_two_2 = zip(keys_of_count_for, values_of_count_for) 
sorted_keys_values_2 = sorted(zip_two_2, key=lambda x:x[1])
output_2 = zip(*sorted_keys_values_2)
sorted_keys_of_count_for, sorted_values_of_count_for = [list(x) for x in output_2]
sorted_keys_of_count_for.reverse()
sorted_values_of_count_for.reverse()


for i in [k for k in DU.keys()]:
    if i in sorted_keys_of_count_for:
        sorted_keys_of_count_for.remove(i)
        sorted_keys_of_count_for.insert(0, i)

print('Activated_PP1')
print(Activated_PP1)
for i in [k for k in Activated_PP1.keys()]:
    if i not in sorted_keys_of_count_for:
        sorted_keys_of_count_for.insert(0, i)
# print('sorted_keys_of_count_for')

for i in PP2_or_PP3: 
    if i not in [k for k in DU.keys()] and i in sorted_keys_of_count_for:
        sorted_keys_of_count_for.remove(i)
        sorted_keys_of_count_for.append(i)


flage = False
for i in [k for k in rest_need_new_PP1.keys()]:
    for ii in range(len(rest_need_new_PP1[i])):
        flage = False
        for iii in sorted_keys_of_count_for:
            if iii in rest_need_new_PP1[i][ii][0] or iii in rest_need_new_PP1[i][ii][1]:
                wp = 0 # working_path
                if iii in rest_need_new_PP1[i][ii][0] and iii not in rest_need_new_PP1[i][ii][1]:
                    wp = 0
                elif iii in rest_need_new_PP1[i][ii][1] and iii not in rest_need_new_PP1[i][ii][0]:
                    wp = 1
                elif rest_need_new_PP1[i][ii][0][-1] >= rest_need_new_PP1[i][ii][1][-1]:
                    wp = 1
                elif rest_need_new_PP1[i][ii][0][-1] < rest_need_new_PP1[i][ii][1][-1]:
                    wp = 0
                if Net.vertList[iii].resource[2] > Net.traffic[i][3]: 
                    n = 0
                    while n < len(rest_need_new_PP1[i][ii][wp]) - 2:
                        if str(rest_need_new_PP1[i][ii][wp][n]) + '-' + \
                                str(rest_need_new_PP1[i][ii][wp][n + 1]) in daikuan:
                            daikuan[str(rest_need_new_PP1[i][ii][wp][n]) + '-' +
                                    str(rest_need_new_PP1[i][ii][wp][n + 1])] -= Net.traffic[i][3]
                        else: 
                            daikuan[str(rest_need_new_PP1[i][ii][wp][n + 1]) + '-' +
                                    str(rest_need_new_PP1[i][ii][wp][n])] -= Net.traffic[i][3]
                        n += 1
                    m = 0
                    while m < len(all_node_all_path_record[i][ii][wp]) - n - 2:
                        if str(all_node_all_path_record[i][ii][wp][n + m]) + '-' \
                                + str(all_node_all_path_record[i][ii][wp][n + m + 1]) in daikuan:
                            daikuan[str(all_node_all_path_record[i][ii][wp][n + m]) + '-'
                                    + str(all_node_all_path_record[i][ii][wp][n + m + 1])] \
                                -= Net.traffic[i][3]  * Size_decrease_ratio
                        else:
                            daikuan[str(all_node_all_path_record[i][ii][wp][n + m + 1]) + '-'
                                    + str(all_node_all_path_record[i][ii][wp][n + m])] \
                                -= Net.traffic[i][3]  * Size_decrease_ratio
                        m += 1
                    if (np.array([k for k in daikuan.values()]) >= 0).all() == False:
                        daikuan = copy.deepcopy(Net.bandwidth)
                    elif (np.array([k for k in daikuan.values()]) >= 0).all() == True:
                        nn = 0
                        while nn < len(rest_need_new_PP1[i][ii][wp]) - 2:
                            if str(rest_need_new_PP1[i][ii][wp][nn]) + '-' + \
                                    str(rest_need_new_PP1[i][ii][wp][nn + 1]) in Net.bandwidth:
                                Net.bandwidth[str(rest_need_new_PP1[i][ii][wp][nn]) + '-' +
                                        str(rest_need_new_PP1[i][ii][wp][nn + 1])] -= Net.traffic[i][3]
                            else:
                                Net.bandwidth[str(rest_need_new_PP1[i][ii][wp][nn + 1]) + '-' +
                                        str(rest_need_new_PP1[i][ii][wp][nn])] -= Net.traffic[i][3]
                            nn += 1
                        mm = 0
                        while mm < len(all_node_all_path_record[i][ii][wp]) - nn - 2:
                            if str(all_node_all_path_record[i][ii][wp][nn + mm]) + '-' \
                                + str(all_node_all_path_record[i][ii][wp][nn + mm + 1]) in Net.bandwidth:
                                Net.bandwidth[str(all_node_all_path_record[i][ii][wp][nn + mm]) + '-'
                                        + str(all_node_all_path_record[i][ii][wp][nn + mm + 1])] \
                                    -= Net.traffic[i][3] * Size_decrease_ratio
                            else:
                                Net.bandwidth[str(all_node_all_path_record[i][ii][wp][nn + mm + 1]) + '-'
                                              + str(all_node_all_path_record[i][ii][wp][nn + mm])] \
                                    -= Net.traffic[i][3] * Size_decrease_ratio
                            mm += 1
                        Net.vertList[iii].resource[2] -= Net.traffic[i][3]
                        allpath[i] = all_node_all_path_record[i][ii]
                        working[i] = all_node_all_path_record[i][ii][wp]
                        which_PP1_used[i] = iii
                        daikuan = copy.deepcopy(Net.bandwidth)
                        flage = True
                        break
                    if flage:
                        break
                if flage:
                    break
            if flage:
                break
        if flage:
            break


start = time.time()

looking_for_CU = {}
for i in [k for k in which_PP1_used.keys()]:
    looking_for_CU[i] = copy.deepcopy(working[i][working[i].index(which_PP1_used[i]):])

copy_lok = copy.deepcopy(looking_for_CU)
for i in [k for k in copy_lok.keys()]:
    for ii in copy_lok[i]:
        if ii not in PP2_or_PP3:
            looking_for_CU[i].remove(ii)
# print(looking_for_CU)

which_CU = {}
for i in [k for k in looking_for_CU.keys()]:
    if len(looking_for_CU[i]) == 1:
        if Net.vertList[looking_for_CU[i][0]].resource[1] >= Net.traffic[i][-1] * Size_decrease_ratio:
            which_CU[i] = looking_for_CU[i][0]
            Net.vertList[looking_for_CU[i][0]].resource[1] -= Net.traffic[i][-1] * Size_decrease_ratio
            del copy_lok[i]
# print(copy_lok)

flage_2 = False
for i in [k for k in copy_lok.keys()]:
    for iii in copy_lok[i]:
        for ii in [k for k in which_CU.values()]:
            if ii == iii and Net.vertList[iii].resource[1] >= Net.traffic[i][-1] * Size_decrease_ratio:
                which_CU[i] = iii
                Net.vertList[iii].resource[1] -= Net.traffic[i][-1] * Size_decrease_ratio
                flage_2 = True
                break
            if flage_2:
                break
print('CU')
print(which_CU)
################################## CU #######################################



CU = [k for k in which_CU.values()]
DU = [k for k in which_PP1_used.values()]
all_of_them = []
for i in DU:
    if i not in all_of_them:
        all_of_them.append(i)
for i in CU:
    if i not in all_of_them:
        all_of_them.append(i)
for i in MEC:
    if i not in all_of_them:
        all_of_them.append(i)

for i in [k for k in only_one_way_to_go_MEC.keys()]:
    if i != only_one_way_to_go_MEC[i][0][-2]:
        for ii in only_one_way_to_go_MEC[i][0][1:-1]:
            a, b = find_the_shrest_path(i, ii)
            if ii in all_of_them and b <= Net.traffic[i][0]:
                band_marker = copy.deepcopy(Net.bandwidth)
                n = 0
                while n < only_one_way_to_go_MEC[i][0].index(ii):
                    if str(only_one_way_to_go_MEC[i][0][n]) + '-' + \
                            str(only_one_way_to_go_MEC[i][0][n + 1]) in Net.bandwidth:
                        Net.bandwidth[str(only_one_way_to_go_MEC[i][0][n]) + '-' +
                                        str(only_one_way_to_go_MEC[i][0][n + 1])] -= Net.traffic[i][3]
                        n += 1
                    else:
                        Net.bandwidth[str(only_one_way_to_go_MEC[i][0][n + 1]) + '-' +
                                      str(only_one_way_to_go_MEC[i][0][n])] -= Net.traffic[i][3]
                        n += 1
                while n < len(only_one_way_to_go_MEC[i][0]) - 2:
                    if str(only_one_way_to_go_MEC[i][0][n]) + '-' + \
                            str(only_one_way_to_go_MEC[i][0][n + 1]) in Net.bandwidth:
                        Net.bandwidth[str(only_one_way_to_go_MEC[i][0][n]) + '-' +
                                    str(only_one_way_to_go_MEC[i][0][n + 1])] -= Net.traffic[i][3] * Size_decrease_ratio
                        n += 1
                    else:
                        Net.bandwidth[str(only_one_way_to_go_MEC[i][0][n + 1]) + '-' +
                                      str(only_one_way_to_go_MEC[i][0][n])] -= Net.traffic[i][
                                                                                       3] * Size_decrease_ratio
                        n += 1
                if (np.array([k for k in Net.bandwidth.values()]) >= 0).all() == True:
                    which_PP1_used[i] = ii
                else:
                    Net.bandwidth = band_marker
print('DU')
print(which_PP1_used)



# In the end, you only need to calculate the energy consumption according to the selected DU, CU, and MEC.
