import sys
# Taking input from stdin
lines = []
lines = sys.stdin.readlines()

keywords = ["za", "od", "do", "az"]
operators = ["=", "+", "-", "*", "/", "(", ")"]
dictionary = {"=": "OP_PRIDRUZI", "+": "OP_PLUS", "-": "OP_MINUS", "*": "OP_PUTA", "/": "OP_DIJELI", "(": "L_ZAGRADA", ")": "D_ZAGRADA", "za": "KR_ZA", "od": "KR_OD", "do": "KR_DO", "az": "KR_AZ"}
output = ""

lineNum = 1
for line in lines:
    line = line + " "
    index = 0
    idn = ""
    number = ""
    for letter in line:
        if letter in operators:
            if idn:
                if idn in keywords:
                    output += f'{dictionary[idn]} {lineNum} {idn}\n'
                else:
                    output += f'IDN {lineNum} {idn}\n'
                idn = ""
            elif number:
                output += f'BROJ {lineNum} {number}\n'
                number = ""
            if letter == "/" and line[index+1] == "/":
                break
            else:
                output += f'{dictionary[letter]} {lineNum} {letter}\n'
        elif letter == " ":
            if idn:
                if idn in keywords:
                    output += f'{dictionary[idn]} {lineNum} {idn}\n'
                else:
                    output += f'IDN {lineNum} {idn}\n'
                idn = ""
            elif number:
                output += f'BROJ {lineNum} {number}\n'
                number = ""
        elif letter.isalpha():
            if number:
                output += f'BROJ {lineNum} {number}\n'
                number = ""
            idn += letter
        elif letter.isdigit():
            if idn:
                idn += letter
            else:
                number += letter
        index += 1
    lineNum += 1

print(output)