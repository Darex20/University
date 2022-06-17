import argparse
import heapq

parser = argparse.ArgumentParser()

parser.add_argument("--alg", default="")
parser.add_argument("--ss", default="")
parser.add_argument("--h", default="")
parser.add_argument("--check-optimistic", action='store_true')
parser.add_argument("--check-consistent", action='store_true')

args = parser.parse_args()

# Parsing input arguments
alg = args.alg
ss_path = args.ss 
h_path = args.h
check_optimistic = args.check_optimistic
check_consistent = args.check_consistent

# Node class used in bfs and ucs algorithms
class Node:
    def __init__(self, parentNode, state, price):
        self.parentNode = parentNode
        self.state = state
        self.price = price

    def __str__(self):
        return f'{self.state},{self.price}'
    
    def __repr__(self):
        return str(self)

    def __lt__ (self, other):
        return self.price < other.price

    def __gt__ (self, other):
        return other.__lt__(self)
    
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def getParentNode(self):
        return self.parentNode

# HeuristicNode class for nodes in astar algorithm, needed for heap sorting purposes
class HeuristicNode:

    def __init__(self, parentNode, state, price, heuristicValue):
        self.parentNode = parentNode
        self.state = state
        self.price = price
        self.heuristicValue = heuristicValue
        self.expectedCost = self.price + self.heuristicValue

    def __str__(self):
        return f'{self.state},{self.price}'

    def __repr__(self):
        return str(self)
    
    def __lt__ (self, other):
        return self.expectedCost < other.expectedCost

    def __gt__ (self, other):
        return other.__lt__(self)
    
    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

# Function for loading and parsing data
def loadData(h_flag):

    start_state = ""
    final_states = ""
    state_dict = {}
    heuristic_dict = {}
    ss = []

    with open(ss_path, encoding = 'utf-8') as f:
        for line in f:
            if not line.startswith('#'):
                ss.append(line)
    start_state = ss[0].strip()
    final_states = ss[1].split()
    for line in ss[2:]:
        curr_state = line.split(':')[0]
        next_states = line.split(':')[1].strip()
        state_dict[curr_state] = next_states
    
    # flag if we are using heuristic values
    if h_flag:
        with open(h_path, encoding = 'utf-8') as s:
            for line in s:
                if not line.startswith('#'):
                    curr_state = line.split(':')[0]
                    heuristic_value = line.split(':')[1].strip()
                    heuristic_dict[curr_state] = heuristic_value
        return start_state, final_states, state_dict, heuristic_dict

    return start_state, final_states, state_dict

def giveResult(node):
    
    nextNode = node
    totalCost = 0.0
    pathLength = 0
    reversedPath = []
    path = ""

    while nextNode != None:
        totalCost += float(nextNode.price)
        pathLength += 1
        reversedPath.append(nextNode.state)
        nextNode = nextNode.parentNode

    path_list = reversedPath[::-1]
    
    while path_list:
        state = path_list.pop(0)
        if path_list:
            path += f'{state} => '
        else:
            path += f'{state}'

    return pathLength, totalCost, path


def aStar(start_state, final_states, state_dict, heuristic_dict):

    open_list = []
    heapq.heapify(open_list)
    heapq.heappush(open_list, HeuristicNode(None, start_state, 0, 0))
    
    open_unwanted = {}

    closed_list = {}

    while open_list:
        node = heapq.heappop(open_list)
        
        # check if state should be ignored
        if node.state in open_unwanted.keys():
            if node.price > open_unwanted[node.state]:
                continue
            else:
                open_unwanted[node.state] = node.price

        if node.state in final_states:
            pathLength, totalCost, path = giveResult(node)
            totalCost = node.price
            return True, len(closed_list), pathLength, totalCost, path

        if node.state in closed_list:
            closed_list[node.state].append(node)
        else:
            closed_list[node.state] = [node]

        for el in state_dict[node.state].split():
            new_node = HeuristicNode(node, el.split(',')[0], int(el.split(',')[1]) + node.price, int(heuristic_dict[el.split(',')[0]]))

            if new_node.state in closed_list.keys():
                flag = False
                for st in closed_list[new_node.state]:
                    if st.price <= new_node.price:
                        flag = True
                        break
                    else:
                        # add state to unwanted states
                        if new_node.state not in open_unwanted:
                            open_unwanted[node.state] = new_node.price
                if flag:
                    continue
            
            heapq.heappush(open_list, new_node)

    return False, 0, 0, 0, ""
                        
    
def bfs(start_state, final_states, state_dict):
    
    open_list = []
    open_list.append(Node(None, start_state, 0))
    closed_list = set()

    while open_list:
        
        node = open_list.pop(0)
        n = node.state
        if n in final_states:
            pathLength, totalCost, path = giveResult(node)
            return True, len(closed_list), pathLength, totalCost, path
        
        closed_list.add(n)
        for state in state_dict[n].split():
            if state.split(',')[0] not in closed_list:
                open_list.append(Node(node, state.split(',')[0], state.split(',')[1]))

    return False, 0, 0, 0, ""

def ucs(start_state, final_states, state_dict):

    open_list = []
    open_list.append(Node(None, start_state, 0))
    heapq.heapify(open_list)
    
    closed_list = set()

    while open_list:

        node = heapq.heappop(open_list)
        n, price = node.state, node.price
        if n in final_states:
            pathLength, _, path = giveResult(node)
            return True, len(closed_list), pathLength, price, path
        
        closed_list.add(n)
        for state in state_dict[n].split():
            if state.split(',')[0] not in closed_list:
                heapq.heappush(open_list, (Node(node, state.split(',')[0], int(state.split(',')[1]) + int(node.price))))

    return False, 0, 0, 0, ""

def checkConsistent(state_dict, heuristic_dict):
    
    output_list = []
    consistent = True
    for s in state_dict:
        nodes = state_dict[s].split()
        for node in nodes:
            state, price = node.split(',')[0], node.split(',')[1]
            if int(heuristic_dict[s]) <= int(heuristic_dict[state]) + int(price):
                output = f'[CONDITION]: [OK] h({s}) <= h({state}) + c: {float(heuristic_dict[s]):.1f} <= {float(heuristic_dict[state]):.1f} + {float(price):.1f}'
            else:
                output = f'[CONDITION]: [ERR] h({s}) <= h({state}) + c: {float(heuristic_dict[s]):.1f} <= {float(heuristic_dict[state]):.1f} + {float(price):.1f}'
                consistent = False
        
            output_list.append(output)

    return output_list, consistent


def checkOptimistic(final_states, state_dict, heuristic_dict):
    
    output_list = []
    optimistic = True
    for state in state_dict:
        _, _, _, total_cost, _ = ucs(state, final_states, state_dict)
        if int(heuristic_dict[state]) <= total_cost:
            output = f'[CONDITION]: [OK] h({state}) <= h*: {float(heuristic_dict[state]):.1f} <= {float(total_cost):.1f}'
        else:
            output = f'[CONDITION]: [ERR] h({state}) <= h*: {float(heuristic_dict[state]):.1f} <= {float(total_cost):.1f}'
            optimistic = False

        output_list.append(output)

    return output_list, optimistic


def output(method):
    if method == "astar":
        start_state, final_states, state_dict, heuristic_dict = loadData(h_flag = True)
        found_solution, states_visited, path_length, total_cost, path = aStar(start_state, final_states, state_dict, heuristic_dict)
        print(f'# A-STAR {h_path}')
        if found_solution:
            print(f'[FOUND_SOLUTION]: yes')
            print(f'[STATES_VISITED]: {states_visited}')
            print(f'[PATH_LENGTH]: {path_length}')
            print(f'[TOTAL_COST]: {total_cost:.1f}')
            print(f'[PATH]: {path}')
        else:
            print(f'[FOUND_SOLUTION]: no')

    elif method == "bfs":
        start_state, final_states, state_dict = loadData(h_flag = False)
        found_solution, states_visited, path_length, total_cost, path = bfs(start_state, final_states, state_dict)
        print(f'# BFS')
        if found_solution:
            print(f'[FOUND_SOLUTION]: yes')
            print(f'[STATES_VISITED]: {states_visited}')
            print(f'[PATH_LENGTH]: {path_length}')
            print(f'[TOTAL_COST]: {total_cost:.1f}')
            print(f'[PATH]: {path}')
        else:
            print(f'[FOUND_SOLUTION]: no')

    elif method == "ucs":
        start_state, final_states, state_dict = loadData(h_flag = False)
        found_solution, states_visited, path_length, total_cost, path = ucs(start_state, final_states, state_dict)
        print(f'# UCS')
        if found_solution:
            print(f'[FOUND_SOLUTION]: yes')
            print(f'[STATES_VISITED]: {states_visited}')
            print(f'[PATH_LENGTH]: {path_length}')
            print(f'[TOTAL_COST]: {total_cost:.1f}')
            print(f'[PATH]: {path}')
        else:
            print(f'[FOUND_SOLUTION]: no')
    
    elif method == "check_optimistic":
        _, final_states, state_dict, heuristic_dict = loadData(h_flag = True)
        output_list, optimistic = checkOptimistic(final_states, state_dict, heuristic_dict)
        print(f'# HEURISTIC-OPTIMISTIC {h_path}')
        for line in output_list:
            print(line)
        if optimistic:
            print(f'[CONCLUSION]: Heuristic is optimistic.')
        else:
            print(f'[CONCLUSION]: Heuristic is not optimistic.')

    elif method == "check_consistent":
        _, _, state_dict, heuristic_dict = loadData(h_flag = True)
        output_list, consistent = checkConsistent(state_dict, heuristic_dict)
        print(f'# HEURISTIC-CONSISTENT {h_path}')
        for line in output_list:
            print(line)
        if consistent:
            print(f'[CONCLUSION]: Heuristic is consistent.')
        else:
            print(f'[CONCLUSION]: Heuristic is not consistent.')

# Decide which algorithm we are going to use
if alg == "astar":
    output("astar")
elif alg == "bfs":
    output("bfs")
elif alg == "ucs":
    output("ucs")
elif alg == "":
    if check_consistent:
        output("check_consistent")
    elif check_optimistic:
        output("check_optimistic")
    else:
        print("Wrong argument input")
