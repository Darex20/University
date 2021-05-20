# Taking input from stdin
lines = []
index = 0
try:
    while(True):
        a = input()
        if a == '' and index != 2:
            break
        else:
            lines.append(a)
        index = index +1
except EOFError:
    pass

# Setting up variables
allStates = lines[0].split(',')         # All states
allSymbols = lines[1].split(',')        # All symbols
acceptableStates = lines[2].split(',')  # Acceptable states
startingState = lines[3]                # Starting state
function = []                           # Transition function
for i in range(4, len(lines)):
    function.append(lines[i])

funcDict = {}
for i in function:
    word = i.split('>')
    funcDict[word[0].replace('-', '')] = word[1]  # Transition function made into a dictionary


# ---------------------------------------------
# First Step - Removing all inaccessible states
comma = ','
currStates = []
currStates.append(startingState)

while True:
    flag = True
    for state in currStates:
        for symbol in allSymbols:
            var = state+comma+symbol
            if var in funcDict and funcDict.get(var) not in currStates:
                currStates.append(funcDict.get(var))
                flag = False
    if flag:
        break

currStates = sorted(currStates)

# States that are the same
identicalStates = []
for state in allStates:
    if state not in currStates:
        identicalStates.append(state)

keyList = []
# Finding all keys that that are identical in funcDict dictionary
for key in funcDict:
    for state in identicalStates:
        if state in key:
            keyList.append(key)
# Deleting all keys that are identical in funcDict dictionary
for key in keyList:
    del funcDict[key]

# Finding all states in allStates that are identical
tempList = []
for state in allStates:
    if state in identicalStates:
        tempList.append(state)
# Deleting all states in allStates that are identical
for state in tempList:
    allStates.remove(state)

# Finding all states in acceptableStates that are identical
tempList = []
for state in acceptableStates:
    if state in identicalStates:
        tempList.append(state)
# Deleting all states in acceptableState that are identical
for state in tempList:
    acceptableStates.remove(state)

# ---------------------------------------------------------------------------
# Second Step - Finding all pairs (p,q) where p is from F and q is not from F
markedList = []
for state in currStates:
    if state in acceptableStates:
        continue
    for accState in acceptableStates:
        if state not in acceptableStates:
            markedList.append(state + comma + accState)

# Third step - Main part of the algorithm
while True:
    # Setting flag value to know when to break out of main while loop
    flag = True
    # Iterating over all combination of (p,q) pairs, excluding ones where q equals p
    for p in currStates:
        for q in currStates:
            if q == p:
                continue
            # If (p,q) ∈ (FxF) or (p,q) ∈ (Q-FxQ-F)
            if (p in acceptableStates and q in acceptableStates) or (p not in acceptableStates and q not in acceptableStates):
                # Iterating over each symbol input
                for symbol in allSymbols:
                    # If p and q for some symbol have a transition
                    if p+comma+symbol in funcDict and q+comma+symbol in funcDict:
                        # newPair = (δ(p,a), δ(q,a))
                        newPair = funcDict.get(p+comma+symbol) + comma + funcDict.get(q+comma+symbol)
                        # If the new states that we transitioning to are in marked list
                        if newPair in markedList:
                            # If (p,q) is not marked, mark them too
                            if p+comma+q not in markedList:
                                markedList.append(p+comma+q)
                                flag = False
    if flag:
        break


# Finding all states that are identical
same = []
tempList = []
for p in currStates:
    tempList.append(p)
    for q in currStates:
        if q in tempList:
            continue
        if p + comma + q not in markedList and p != q and q + comma + p not in markedList:
            same.append(p+comma+q)

sameStates = []
for pair in same:
    i = pair.split(',')
    if i[0] > i[1]:
        pair = i[1]+','+i[0]
    sameStates.append(pair)

tempKeyList = []
for state in sameStates:
    right = state.split(',')[1]
    left = state.split(',')[0]
    if startingState == right:
        startingState = left
    if right in acceptableStates:
        acceptableStates.remove(right)
    if right in allStates:
        allStates.remove(right)
    for key in funcDict:
        if right in key:
            tempKeyList.append(key)
    for key, value in funcDict.items():
        if value == right:
            funcDict[key] = left

for key in tempKeyList:
    if key in funcDict:
        del funcDict[key]


def makeString(tempList):
    finalString = ''
    for i in tempList:
        if finalString == '':
            finalString = finalString + i
        else:
            finalString = finalString + ',' + i
    return finalString


print(makeString(allStates))
print(makeString(allSymbols))
print(makeString(acceptableStates))
print(startingState)
for key, value in funcDict.items():
    print(key + '->' + value)




