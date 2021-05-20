output = ''
index = 0
flag = False
input = input()


def A():
    global output
    global index
    global flag
    output = output + 'A'
    if index == len(input):
        flag = True
        return
    elif input[index] == 'b':
        index = index + 1
        C()
    elif input[index] == 'a':
        index = index + 1
    else:
        flag = True
        return


def B():
    global output
    global index
    global flag
    if flag:
        return
    output = output + 'B'
    if index + 1 > len(input) - 1:
        return
    if index == len(input):
        return
    if input[index] == 'c' and input[index+1] == 'c':
        index = index + 2
        S()
        index = index + 2


def C():
    global output
    global index
    if flag:
        return
    output = output + 'C'
    A()
    if flag:
        return
    A()


def S():
    global output
    global index
    output = output + 'S'
    if input[index] == 'a':
        index = index + 1
        A()
        B()
    elif input[index] == 'b':
        index = index + 1
        B()
        A()


S()
print(output)
if index == len(input) and flag is False:
    print('DA')
else:
    print('NE')


