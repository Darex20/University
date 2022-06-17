from calendar import c
from dis import dis
from os import access
import sys
import math
from tkinter import Y

class Node:
    def __init__(self, parent, name, types, curr_dataset, predecessor, depth, children):
        self.parent = parent
        self.name = name
        self.types = types
        self.curr_dataset = curr_dataset
        self.predecessor = predecessor
        self.depth = depth
        self.children = children

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    def __contains__(self, item):
        return item.name == self.name

class Leaf:
    def __init__(self, parent, value, predecessor):
        self.parent = parent
        self.value = value
        self.predecessor = predecessor

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)

class ID3:
    def __init__(self, depth):
        self.root_node = None
        self.leafs = None
        self.depth = depth
        pass

    def entropy(self, dataset):
        y_values = self.findTargetDisparity(dataset)
        domain_size = len(dataset)
        entropy = 0.
        for _, value in y_values.items():
            if value/domain_size == 0:
                continue
            else:
                entropy += float(value/domain_size) * math.log2(float(value/domain_size))
        if entropy == 0:
            return 0
        else:
            entropy = -entropy
            return entropy
        
    def findTargetDisparity(self, dataset):
        y_values = {}
        for line in dataset:
            if line[-1] not in y_values:
                y_values[line[-1]] = 1.
            else:
                y_values[line[-1]] += 1.
        return y_values

    def findBestVal(self, gains):
        curr_key, curr_value = None, None
        for key, value in gains.items():
            if not curr_key and not curr_value:
                curr_key, curr_value = key, value
            else:
                if curr_value < value:
                    curr_value = value
                    curr_key = key
                elif curr_value == value and curr_key > key:
                    curr_key = key
        return curr_key

    def findGain(self, header, dataset, domain_entropy, domain_size, untouched_header):
        
        gain_values = dict()
        all_values = dict()
        all_values = self.findTypes(dataset, untouched_header)
        new_values = dict()
        for el in header:
            if el in all_values:
                new_values[el] = all_values[el]

        for el in new_values:
            ig_value = domain_entropy
            for val in new_values[el]:
                val_lines = []
                for line in dataset:
                    if val == line[untouched_header.index(el)]:
                        val_lines.append(line)
                ig_value -= (float(len(val_lines)) / float(domain_size)) * self.entropy(val_lines)
            gain_values[el] = ig_value
        
        for key in list(gain_values.keys()):
            if key not in header:
                del gain_values[key]

        return gain_values

    def findTypes(self, dataset, untouched_header):
        types = dict()
        for el in untouched_header:
            for line in dataset:
                if el in types:
                    if line[untouched_header.index(el)] not in types[el]:
                        types[el].append(line[untouched_header.index(el)])
                else:
                    types[el] = [line[untouched_header.index(el)]]
        return types

    def findBestNode(self, parent, header, types, curr_dataset, untouched_header, predecessor, depth, children):
        domain_size = len(curr_dataset)
        domain_entropy = self.entropy(curr_dataset)
        gain_values = self.findGain(header, curr_dataset, domain_entropy, domain_size, untouched_header)

        gains = ""
        for key, value in gain_values.items():
            gains = gains + f'IG({key})={value:.4f} '
        print(gains)

        found_key = self.findBestVal(gain_values)
        best_node = Node(parent, found_key, types[found_key], curr_dataset, predecessor, depth, children)
        return best_node
        

    def fit(self, train_dataset):
        header = train_dataset[:1].pop()[:-1]
        untouched_header = train_dataset[:1].pop()[:-1]
        types = self.findTypes( train_dataset[1:], untouched_header)
        root_node = self.findBestNode(None, header, types, train_dataset[1:], untouched_header, None, 0, [])
        self.root_node = root_node
        visited = [root_node]
        leafs = []
        while visited:
            curr_node = visited.pop(0)
            if self.depth:
                if curr_node.depth == self.depth:
                    break
            for value in curr_node.types:
                curr_domain = []
                for line in curr_node.curr_dataset:
                    if value == line[untouched_header.index(curr_node.name)]:
                        curr_domain.append(line)
                if self.entropy(curr_domain) != 0:
                    if curr_node.name in header:
                        header.remove(curr_node.name)
                    next_node = self.findBestNode(curr_node, header, types, curr_domain, untouched_header, value, curr_node.depth+1, [])
                    curr_node.children.append(next_node)
                    visited.append(next_node)
                else:
                    if curr_domain:
                        curr_node.children.append(Leaf(curr_node, curr_domain[0][-1], value))
                        leafs.append(Leaf(curr_node, curr_domain[0][-1], value))
        
        self.leafs = leafs
        print("[BRANCHES]:")
        if not self.depth:
            for leaf in leafs:
                parent = leaf.parent
                output = f'{parent.depth+1}:{parent.name}={leaf.predecessor} {leaf.value}'
                while parent:
                    curr = parent
                    parent = parent.parent
                    if not parent:
                        break
                    output = f'{parent.depth+1}:{parent.name}={curr.predecessor} {output}'
                print(output)
        else:
            visit = [self.root_node]
            front_nodes = []
            while visit:
                curr_node = visit.pop()
                if type(curr_node) is Leaf:
                    front_nodes.append(curr_node)
                elif not curr_node.children:
                    front_nodes.append(curr_node)
                else:
                    for children in curr_node.children:
                        visit.insert(0,children)

            output = ""
            for node in front_nodes:
                if type(node) is Leaf:
                    output = f'{node.parent.depth+1}:{node.parent.name}={node.predecessor} {node.value}'
                else:
                    if node.parent:
                        disparity = self.findTargetDisparity(node.curr_dataset)
                        best_key = self.findBestVal(disparity)
                        output = f'{node.parent.depth+1}:{node.parent.name}={node.predecessor} {best_key}'
                parent = node.parent
                curr_node = node
                while parent:
                    curr_node = parent
                    parent = parent.parent
                    if not parent:
                        break
                    output = f'{parent.depth+1}:{parent.name}={curr_node.predecessor} {output}'
                if not output:
                    disparity = self.findTargetDisparity(node.curr_dataset)
                    best_key = self.findBestVal(disparity)
                    output = f'{best_key}'
                print(output)

    def predict(self, test_dataset):
        header = test_dataset[:1].pop()
        dataset = test_dataset[1:]

        predictions = []
        real_values = []
        
        not_found = False
        if not self.depth:
            for line in dataset:
                curr_node = self.root_node
                flag = False
                not_found = False
                while True:
                    if not_found:
                        break
                    for child in curr_node.children:
                        if line[header.index(curr_node.name)] == child.predecessor:
                            curr_node = child
                            if type(curr_node) is Leaf:
                                predictions.append(curr_node.value)
                                real_values.append(line[-1])
                                flag = True
                            not_found = False
                            break
                        else:
                            not_found = True
                    if flag:
                        break
        else:
            for line in dataset:
                visit = [self.root_node]
                while visit:
                    curr_node = visit.pop()
                    for child in curr_node.children:
                        if line[header.index(curr_node.name)] == child.predecessor:
                            if type(child) is Leaf:
                                real_values.append(line[-1])
                                predictions.append(child.value)
                            elif not child.children:
                                real_values.append(line[-1])
                                disparity = self.findTargetDisparity(child.curr_dataset)
                                best_key = self.findBestVal(disparity)
                                predictions.append(best_key)
                            else:
                                visit.append(child)
                            break
                    
        if not_found:
            disparity = self.findTargetDisparity(test_dataset[1:])
            value = disparity.popitem()
            for line in test_dataset[1:]:
                real_values.append(line[-1])
            for i in range(len(real_values)):
                predictions.append(value[0])

        output_predictions = "[PREDICTIONS]: "
        for prediction in predictions:
            output_predictions += f'{prediction} '
        print(output_predictions)
        
        
        good_predictions = 0
        for i in range(len(predictions)):
            if predictions[i] == real_values[i]:
                good_predictions += 1
            
        accuracy = float(good_predictions / len(real_values))
        print(f"[ACCURACY]: {accuracy:.5f}")

        y_values = self.findTypes(test_dataset, header).popitem()[1][1:]
        y_values = sorted(y_values)
        n = len(y_values)
        confusion_matrix = [[0] *n for _ in range(n)]

        print("[CONFUSION_MATRIX]:")
        for i in range(len(y_values)):
            for j in range(len(y_values)):
                num = 0
                for k in range(len(predictions)):
                    if real_values[k] == y_values[i] and predictions[k] == y_values[j]:
                        num += 1
                confusion_matrix[i][j] = num
                print(f'{num}', end =" ")
            print()
        


path_train = sys.argv[1]
path_test = sys.argv[2]
depth = None

if len(sys.argv) > 3:
    depth = int(sys.argv[3])
    
with open(path_train) as file:
    content_train = file.readlines()
train_dataset = [s.strip().split(',') for s in content_train]

with open(path_test) as file:
    content_test = file.readlines()
test_dataset = [s.strip().split(',') for s in content_test]

model = ID3(depth)
model.fit(train_dataset)
model.predict(test_dataset)