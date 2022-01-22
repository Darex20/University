import sys
from types import DynamicClassAttribute
# Taking input from stdin
lines = []
for line in sys.stdin.readlines():
    lines.append(line.rstrip())

listUsless = ["<program>", "<lista_naredbi>", "<naredba>", "<za_petlja>", "<E>", "<E_lista>", "<T>", "<T_lista>", "<P>", "$", "<naredba_pridruzivanja>"]  
realLines = []

flag = False
for line in lines:
    for usless in listUsless:
        if usless in line:
            flag = True
            break
    if not flag:
        realLines.append(line.strip())
    flag = False

outputList = []
mainDictionary = {}
dictionary = {}
index = 0
depth = 0
mainDictionary[depth] = {}
for line in realLines:
    if "KR_ZA" in line:
        depth += 1
        mainDictionary[depth] = {}
depth = 0
realLines.append(" ")

for line in realLines:
    if "KR_ZA" in line:
        dictionary = {}
        depth += 1
    elif "KR_AZ" in line:
        mainDictionary[depth] = {}
        depth -= 1
        dictionary = mainDictionary[depth]
    elif "IDN" in line:
        varName = line.split(" ")[2]
        lineNum = line.split(" ")[1]
        if "OP_PRIDRUZI" in realLines[index+1]:
            if not dictionary or dictionary.get(varName) == None:
                plag = False
                for key in mainDictionary:
                    if varName in mainDictionary[key]:
                        plag = True
                if not plag:
                    dicti = mainDictionary[depth]
                    dicti[varName] = lineNum
                    mainDictionary[depth] = dicti
        elif "KR_ZA" in realLines[index-1] and index != 0:
            if not dictionary or dictionary.get(varName) == None:
                dicti = mainDictionary[depth]
                dicti[varName] = lineNum
                mainDictionary[depth] = dicti
            else:
                outputList.append(f'err {lineNum} {varName}')
                for output in outputList:
                    print(output)
                sys.exit()
        else:
            outputCurrent = ""
            flag = False
            for key in mainDictionary:
                if varName in mainDictionary[key]:
                    outputCurrent = f'{lineNum} {mainDictionary[key][varName]} {varName}'
                    if lineNum == mainDictionary[key][varName]:
                        outputList.append(f'err {lineNum} {varName}')
                        for output in outputList:
                            print(output)
                        sys.exit()
                    flag = True
            if outputCurrent:
                outputList.append(outputCurrent)
            if not flag:
                outputList.append(f'err {lineNum} {varName}')
                for output in outputList:
                    print(output)
                sys.exit()
    index += 1

for output in outputList:
    print(output)

