import sys

class Clause:
    def __init__(self, clause, parent1, parent2):
        self.clause = clause
        self.parent1 = parent1
        self.parent2 = parent2
    
    def __hash__(self):
        hash_value = 0
        for el in self.clause.split(" v "):
            hash_value += hash(el)
        return hash_value

    def __str__(self):
        return self.clause
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        premises1 = self.clause.split(" v ")
        premises2 = other.clause.split(" v ")
        return premises1 == premises2
        
    # Get complement of a clause
    def complement(self):
        help_list = []
        for premise in self.clause.split(" v "):
            if premise.startswith("~"):
                premise = premise.replace("~", "")
            else:
                premise = "~" + premise
            help_list.append(Clause(premise, None, None))
        return help_list
    
    # Returns if a clause is subset of another
    def isSubset(self, other):
        premises1 = self.clause.split(" v ")
        premises2 = other.clause.split(" v ")
        return set(premises1).issubset(set(premises2))
    
    # Check if clause is tautology
    def checkTautology(self):
        premises = self.clause.split(" v ")
        for premise in premises:
            if premise.startswith("~"):
                complement = premise.replace("~", "")
            else:
                complement = "~" + premise
            if complement in premises:
                return True
        return False

    # Returns resolvants of parent clauses
    def plResolve(self, other):
        premises1 = self.clause.split(" v ")
        premises2 = other.clause.split(" v ")
        for premise1 in premises1:
            if premise1.startswith("~"):
                complement = premise1.replace("~", "")
            else:
                complement = "~" + premise1
            if complement in premises2:
                premises1.remove(premise1)
                premises2.remove(complement)
                premises = premises1 + premises2
                premises = list(set(premises))
                clause = ""
                if not premises:
                    return True, Clause("NIL", self, other)
                while premises:
                    el = premises.pop(0)
                    if premises:
                        clause += f'{el} v '
                    else:
                        clause += f'{el}'
                return True, Clause(clause, self, other)
        return False, None

# Function for loading input data
def loadData(resolution_path, input_path=""):

    clauses = []
    with open(resolution_path, encoding = 'utf-8') as s:
        for line in s:
            if not line.startswith('#'):
                clauses.append(line.strip().lower())

    if input_path:
        output_list = []
        with open(input_path, encoding = 'utf-8') as s:
            for line in s:
                if not line.startswith('#'):
                    index = line.rfind(' ')
                    clause = line.strip()[:index].lower()
                    command = line.strip()[index+1:]
                    tup = (clause, command)
                    output_list.append(tup)
        return clauses, output_list

    return clauses

# Delete Strategy
def delStratetgy(clauses):

    # Remove redundant clauses
    for clause in list(clauses):
        for c in list(clauses):
            if clause != c and clause.isSubset(c) and c in clauses:
                clauses.remove(c)

    # Remove tautology clauses
    for clause in list(clauses):
        if clause.checkTautology():
            clauses.remove(clause)
    
    return clauses
    
# Turn string clauses to objects
def clausify(clauses):
    return_list = []
    for clause in clauses:
        clause = Clause(clause, None, None)
        return_list.append(clause)
    return return_list

# Resolution Algorithm
def plResolution(clauses, cooking=False, targetClause=None):
    
    if not cooking:
        clauses = clausify(clauses)
        targetClause = clauses.pop()

    sos_list = targetClause.complement()
    clauses = delStratetgy(clauses)

    while True:
        new_clauses = []
        flag = False
        for c1 in clauses + sos_list:
            for c2 in sos_list:
                found, resolvents = c1.plResolve(c2)
                if found:
                    if resolvents.clause == "NIL":
                        flag = True
                    if resolvents not in new_clauses:
                        check = True
                        for clause in clauses:
                            if clause.isSubset(resolvents):
                                check = False
                        if check:
                            new_clauses.append(resolvents)
        
        if set(new_clauses).issubset(set(clauses)):
            return False, targetClause, clauses
        
        new_clauses = delStratetgy(new_clauses)
        for clause in new_clauses:
            if clause not in clauses:
                clauses.append(clause)
        
        sos_list = new_clauses
        if flag:
            return True, targetClause, clauses
        
# Cooking Algorithm
def cooking(clauses, command_list):
    clauses = clausify(clauses)
    for command in command_list:
        if command[1] == "-":
            clauses.remove(Clause(command[0], None, None))
        elif command[1] == "+":
            clauses.append(Clause(command[0], None, None))
        elif command[1] == "?":
            found, targetClause, cla = plResolution(clauses[:], True, Clause(command[0], None, None))
            outputData(found, targetClause, cla)
    return

# Function for parsing output
def outputData(found, targetClause, clauses):
    if found:
        counter = 1
        for clause in clauses:
            if not clause.parent1 and not clause.parent2:
                print(f'{counter}. {clause}')
                counter += 1

        print("===============")
        for clause in clauses:
            if clause.clause == "NIL":
                curr_parent1, curr_parent2 = clause.parent1, clause.parent2
                curr_clause = clause

        output_list = []
        while curr_parent2:
            output_list = [(curr_clause, curr_parent1, curr_parent2)] + output_list
            curr_clause = curr_parent2
            curr_parent1 = curr_clause.parent1
            curr_parent2 = curr_clause.parent2

        for tupl in output_list:
            print(f'{counter}. {tupl[0]} ({tupl[1]}, {tupl[2]})')
            counter += 1
        
        print("===============")
        print(f"[CONCLUSION]: {targetClause} is true")
    else:
        print(f"[CONCLUSION]: {targetClause} is unknown")
    return

# Parsing input arguments
if sys.argv[1] == "resolution":
    clauses = loadData(sys.argv[2])
    found, targetClause, clauses = plResolution(clauses)
    outputData(found, targetClause, clauses)
elif sys.argv[1] == "cooking":
    clauses, command_list = loadData(sys.argv[2], sys.argv[3])
    cooking(clauses, command_list)
else:
    print("Wrong argument!")
