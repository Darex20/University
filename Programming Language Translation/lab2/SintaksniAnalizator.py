import sys
# Taking input from stdin
lines = []
for line in sys.stdin.readlines():
    lines.append(line.rstrip())
lines.append("⏊")

err = False
layer = 0
index = 0
output = ""
errorOutput = ""

def provjeriZavrsni(zavrsni):
    global index
    global output
    global lines
    global layer
    global errorOutput

    if lines[index].split(" ")[0] in zavrsni:
        output += " " * layer + lines[index] + "\n"
        index += 1
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()

def program():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += "<program>\n"
    layer += 1

    if lines[index].split(" ")[0] in "IDN KR_ZA ⏊":
        lista_naredbi()
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def lista_naredbi():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<lista_naredbi>\n"
    layer += 1

    if lines[index].split(" ")[0] in "IDN KR_ZA":
        naredba()
        lista_naredbi()
    elif lines[index].split(" ")[0] in "KR_AZ ⏊":
        output += " " * layer + "$\n"
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1    
    
def naredba():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<naredba>\n"
    layer += 1

    if lines[index].split(" ")[0] in "IDN":
        naredba_pridruzivanja()
    elif lines[index].split(" ")[0] in "KR_ZA":
        za_petlja()
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def naredba_pridruzivanja():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput
    
    if err:
        return

    output += " " * layer + "<naredba_pridruzivanja>\n"
    layer += 1

    if lines[index].split(" ")[0] in "IDN":  
        output += " " * layer + lines[index] + "\n"
        index += 1
        provjeriZavrsni("OP_PRIDRUZI")
        E()
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def za_petlja():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<za_petlja>\n"
    layer += 1

    if lines[index].split(" ")[0] in "KR_ZA":
        output += " " * layer + lines[index] + "\n"
        index += 1
        provjeriZavrsni("IDN")
        provjeriZavrsni("KR_OD")
        E()
        provjeriZavrsni("KR_DO")
        E()
        lista_naredbi()
        provjeriZavrsni("KR_AZ")
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def E():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<E>\n"
    layer += 1

    if lines[index].split(" ")[0] in "IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA":
        T()
        E_lista()
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def E_lista():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<E_lista>\n"
    layer += 1

    if lines[index].split(" ")[0] in "OP_PLUS":
        output += " " * layer + lines[index] + "\n"
        index += 1
        E()
    elif lines[index].split(" ")[0] in "OP_MINUS":
        output += " " * layer + lines[index] + "\n"
        index += 1
        E()
    elif lines[index].split(" ")[0] in "IDN KR_ZA KR_DO KR_AZ D_ZAGRADA ⏊":
        output += " " * layer + "$\n"
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def T():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<T>\n"
    layer += 1

    if lines[index].split(" ")[0] in "IDN BROJ OP_PLUS OP_MINUS L_ZAGRADA":
        P()
        T_lista()
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def T_lista():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<T_lista>\n"
    layer += 1

    if lines[index].split(" ")[0] in "OP_PUTA":
        output += " " * layer + lines[index] + "\n"
        index += 1
        T()
    elif lines[index].split(" ")[0] in "OP_DIJELI":
        output += " " * layer + lines[index] + "\n"
        index += 1
        T()
    elif lines[index].split(" ")[0] in "IDN KR_ZA KR_DO KR_AZ OP_PLUS OP_MINUS D_ZAGRADA ⏊":
        output += " " * layer + "$\n"
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

def P():
    global layer
    global index
    global lines
    global output
    global err
    global errorOutput

    if err:
        return

    output += " " * layer + "<P>\n"
    layer += 1

    if lines[index].split(" ")[0] in "OP_PLUS":
        output += " " * layer + lines[index] + "\n"
        index += 1
        P()
    elif lines[index].split(" ")[0] in "OP_MINUS":
        output += " " * layer + lines[index] + "\n"
        index += 1
        P()
    elif lines[index].split(" ")[0] in "L_ZAGRADA":
        output += " " * layer + lines[index] + "\n"
        index += 1
        E()
        provjeriZavrsni("D_ZAGRADA")
    elif lines[index].split(" ")[0] in "IDN":
        output += " " * layer + lines[index] + "\n"
        index += 1
    elif lines[index].split(" ")[0] in "BROJ":
        output += " " * layer + lines[index] + "\n"
        index += 1
    else:
        if(lines[index] == "⏊"):
            errorOutput = "err kraj" + "\n"
        else:
            errorOutput = "err " + lines[index] + "\n"
        print(errorOutput, end ="")
        sys.exit()
        err = True
    layer -= 1

program()
if not err:
    print(output, end ="")
else:
    print(errorOutput, end ="")
    