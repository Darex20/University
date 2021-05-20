import sys

# Taking input from stdin
lines = []
index = 0
try:
    while(True):
        a = input()
        if a == '' and index != 4:
            break
        else:
            lines.append(a)
        index = index + 1
except EOFError:
    pass

# Setting up variables
entrySymbolsList = lines[0].split('|')  # Entry symbols
allStates = lines[1]                # All states that are possible in automata
entryStates = lines[2]              # Entry states
stackSymbols = lines[3]             # Stack symbols
acceptableStates = lines[4]         # Acceptable states
startingState = lines[5]            # Starting state
startingSymbolStack = lines[6]      # Starting symbol on a stack
function = []                       # Transition function
for i in range(7, len(lines)):
    function.append(lines[i])

funcDict = {}
for i in function:
    word = i.split('>')
    funcDict[word[0].replace('-', '')] = word[1]  # Transition function as a dictionary


epsilon = '$'
comma = ','
outputList = []

for entrySymbols in entrySymbolsList:
    mainStack = []
    mainStack.append(startingSymbolStack)
    currentState = startingState
    outputLine = startingState + '#' + startingSymbolStack + '|'
    for symbol in entrySymbols.split(','):
        flag = False
        check = False
        end = False
        if mainStack:
            stackSymbol = mainStack.pop()
        while funcDict.get(currentState + comma + epsilon + comma + stackSymbol):
            rightSide = funcDict.get(currentState + comma + epsilon + comma + stackSymbol)
            states = rightSide.split(',')[1]
            currentState = rightSide.split(',')[0]
            if states != epsilon:
                for state in reversed(states):
                    mainStack.append(state)
            line = ''
            if mainStack:
                for state in reversed(mainStack):
                    line = line + state
            else:
                line = '$'
            outputLine = outputLine + currentState + '#' + line + '|'
            flag = True
            if mainStack:
                stackSymbol = mainStack.pop()
            else:
                outputLine = outputLine + 'fail|0'
                check = True
                break

        if not check:
            if stackSymbol == epsilon and currentState in acceptableStates:
                outputLine = outputLine + '1'
                break
            elif stackSymbol == epsilon and currentState not in acceptableStates:
                outputLine = outputLine + '0'
                break

            if funcDict.get(currentState + comma + symbol + comma + stackSymbol):
                rightSide = funcDict.get(currentState + comma + symbol + comma + stackSymbol)
                states = rightSide.split(',')[1]
                currentState = rightSide.split(',')[0]
                if states != epsilon:
                    for state in reversed(states):
                        mainStack.append(state)
                line = ''
                for state in reversed(mainStack):
                    line = line + state
                outputLine = outputLine + currentState + '#' + line + '|'
                flag = True
            else:
                outputLine = outputLine + 'fail|0'
                end = True
                break
        else:
            break
    if mainStack:
        stackSymbol = mainStack.pop()
    if not end:
        while funcDict.get(currentState + comma + epsilon + comma + stackSymbol) and currentState not in acceptableStates:
            rightSide = funcDict.get(currentState + comma + epsilon + comma + stackSymbol)
            states = rightSide.split(',')[1]
            currentState = rightSide.split(',')[0]
            if states != epsilon:
                for state in reversed(states):
                    mainStack.append(state)
            line = ''
            if mainStack:
                for state in reversed(mainStack):
                    line = line + state
            else:
                line = '$'
            outputLine = outputLine + currentState + '#' + line + '|'
            flag = True
            if mainStack:
                stackSymbol = mainStack.pop()

    if currentState in acceptableStates and flag and 'fail' not in outputLine:
        outputLine = outputLine + '1'
    elif flag and 'fail' not in outputLine:
        outputLine = outputLine + '0'

    outputList.append(outputLine)

for el in outputList:
    print(el)