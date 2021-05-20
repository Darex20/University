import sys

# Taking input from stdin
lines = []

try:
    while(True):
        a = input()
        if a == '':
            break
        else:
            lines.append(a)
except EOFError:
    pass

# Setting up variables
entrySymbols = lines[0].split('|')  # Entry symbols
allStates = lines[1]                # All states that are possible in automata
                                    # Symbols are in lines[2]
                                    # Acceptable states are in lines[3]
startingState = lines[4]            # Starting state
function = []                       # Transition function
for i in range(5, len(lines)):
    function.append(lines[i])

funcDict = {}
for i in function:
    word = i.split('>')
    funcDict[word[0].replace('-', '')] = word[1]  # Transition function as a dictionary


specificSymbols = []
for i in entrySymbols:
    specificSymbols.append(i.split(','))   # 2d list for easier iterating trough automata inputs

epsilon = '$'
comma = ','
currentStates = []

# function to find all epsilon transition states
def epsilonFunction(states):
    states = states.split(',')
    stack = []
    s = set()
    finalStates = []
    for state in states:
        stack.append(state)
    while stack != []:
        curr = stack.pop()
        if(curr != '#'):
            finalStates.append(curr)
        s.add(curr)
        if curr+comma+epsilon in funcDict:
            l = funcDict.get(curr+comma+epsilon).split(',')
            for i in l:
                if i not in s:
                    stack.append(i)
    return finalStates

# function to make a string output as it was desired in the task
def makeString(tempList):
    finalString = ''
    for i in tempList:
        if finalString == '':
            finalString = finalString + i
        else:
            finalString = finalString + ',' + i
    return finalString

# outputList where each element is output for each entry
outputList = []
# iterating each separate input sequence
for entry in specificSymbols:
    # currentStates == list that contains current states
    currentStates = []

    # iterating over epsilon transitions of starting state
    for i in epsilonFunction(startingState):
        # appending epsilon transitions to current states
        currentStates.append(i)
    # sorting currentStates
    currentStates = sorted(currentStates)
    # iterating currentStates and appending them to output
    output = makeString(currentStates)

    # for each entry symbol in entry sequence
    for symbol in entry:
        # preparing nextStates variable that we will use to switch currentStates to next ones
        nextStates = []
        # preparing states string variable that we will use to append currentStates needed in output
        states = ''

        # iterating over every state in current states
        for state in currentStates:
            # preparing newState variable to nothing
            newState = ''
            # preparing tempList that will contain new states in list
            tempList = []

            # if there is a transition for certain [state] and [symbol]
            if funcDict.get(state+comma+symbol) != None:
                # fill in a newState variable with the new states from a function dictionary
                newState = funcDict.get(state+comma+symbol)

                # if newState contains # then newState equals None, because there is no transition
                if '#' in newState:
                    newState = None
                    continue

                # for epsilon transition states, append them to newState
                for k in epsilonFunction(newState):
                    newState = newState + ',' + k
                # fill in a tempList list with newStates
                tempList = newState.split(',')

            # for each newState in tempList
            for j in tempList:
                # if newState is not empty and each [j] state in tempList is not in states, append them to states
                if newState != None and states != '' and j not in states:
                    states = states + ',' + j
                elif newState != None and j not in states:
                    states = states + j
                # additional check if j is in states
                elif j in states:
                    temp = states.split(',')
                    if j not in temp:
                        states = states + ',' + j

            # filling in nextStates variable
            nextStates = nextStates + newState.split(',')
            # removing duplicates from nextStates
            nextStates = list(dict.fromkeys(nextStates))

            # filling in temp list with states
            temp = states.split(',')
            temp = sorted(temp)
            # finalising states string for output
            states = makeString(temp)

            # checks to see if allStates are equal to current states, if true break out from current entry sequence
            if states == allStates:
                break

        # in the end check if states stayed empty, if it did put its value to #
        if states == '':
            states = '#'

        # change current states to next states
        currentStates = nextStates
        # append states to output
        output = output + '|' + states

    # append output for each entry to outputList list
    outputList.append(output)

# iterate over output list to get final output string <line>
line = ''
for i in outputList:
    line = line + i + '\n'

# print out the final output string [line]
print(line)



