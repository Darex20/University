import numpy as np

#input x
x0 = float(input("Unesite prvo rjesenje x_0 karakteristicne jednadzbe: "))
x1 = float(input("Unesite drugo rjesenje x_1 karakteristicne jednadzbe: "))
x2 = float(input("Unesite trece rjesenje x_2 karakteristicne jednadzbe: "))

#input a
a0 = float(input("Unesite vrijednost nultog clana niza a_0: "))
a1 = float(input("Unesite vrijednost prvog clana niza a_1: "))
a2= float(input("Unesite vrijednost drugog clana niza a_2: "))

#input n
n = int(input("Unesite redni broj n trazenog clana niza: "))

def usingformula():
    a = np.array([[1, 1, 1], [x0, x1, x2], [x0**2, x1**2, x2**2]])
    b = np.array([a0, a1, a2])
    x = np.linalg.solve(a, b)
    solution = (x[0] * (x0 ** n)) + (x[1] * (x1 ** n)) + (x[2] * (x2 ** n))
    print("Vrijednost n-tog clana niza pomocu formule: ", solution)

#printing out value using the formula
usingformula()

def usingRecursion(num):
    coef3 = x0 * x1 * x2
    coef2 = -(x0*x1 + x1*x2 + x0*x2)
    coef1 = x0 + x1 + x2
    if(num == 0): sol = a0
    elif(num == 1): sol = a1
    elif(num == 2): sol = a2
    else:
        sol = coef3*usingRecursion(num-3) + coef2*usingRecursion(num-2) + coef1*usingRecursion(num-1)
    return sol

print("Vrijednost n-tog clana niza iz rekurzije: ", usingRecursion(n))
