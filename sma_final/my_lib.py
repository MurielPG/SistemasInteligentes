import random
x0 = 1000
x1 = -1000

def converte_inteiro_1g(numeros): 
    k = 0
    a = ""
    b = ""
    for i in range(len(numeros)):
        if (numeros[i] == ","):
            k += 1
            continue
        if(k==0):
            a += numeros[i]
        if(k==1):
            b += numeros[i]
    a = int(a)
    b = int(b)
    return a,b

def converte_inteiro_2g(numeros): 
    k = 0
    a = ""
    b = ""
    c = ""
    for i in range(len(numeros)):
        if (numeros[i] == ","):
            k += 1
            continue
        if(k==0):
            a += numeros[i]
        if(k==1):
            b += numeros[i]
        if(k==2):
            c += numeros[i]
    a = int(a)
    b = int(b)
    c = int(c)
    return a,b,c

def converte_inteiro_3g(numeros): 
    k = 0
    a = ""
    b = ""
    c = ""
    d = ""
    for i in range(len(numeros)):
        if (numeros[i] == ","):
            k += 1
            continue
        if(k==0):
            a += numeros[i]
        if(k==1):
            b += numeros[i]
        if(k==2):
            c += numeros[i]
        if(k==3):
            d += numeros[i]
    a = int(a)
    b = int(b)
    c = int(c)
    d = int(d)
    return a,b,c,d

def bsc_1g(a,b):
    global x1
    global x0
    p = round( (x0+x1) / 2)
    res_x0 = a*x0 + b	
    res_p = a*p + b
    if((res_p*res_x0)>0):
        x0 = p
    else:												
        x1 = p
    return p

def bsc_2g(a,b,c):
    global x1
    global x0
    p = round( (x0+x1) / 2)
    res_x0 = a*x0**2 + b*x0 + c		
    res_p = a*p**2 + b*p + c
    if((res_p*res_x0)>0):
        x0 = p
    else:												
        x1 = p
    return p

def bsc_3g(a,b,c,d):
    global x1
    global x0
    p = round( (x0+x1) / 2)
    res_x0 = a*x0**3 + b*x0**2 + c*x0 + d	
    res_p = a*p**3 + b*p**2 + c*p + d
    if((res_p*res_x0)>0):
        x0 = p
    else:												
        x1 = p
    return p

menor_valor = -10
maior_valor = 10

def gera_1g():
    valores = list(range(menor_valor, maior_valor))
    valores.remove(0)
    a = random.choice(valores)
    x = random.choice(valores)
    b = (a*x)*(-1)
    return a,b,x

def gera_2g():
    valores = list(range(menor_valor, maior_valor))
    valores.remove(0)
    a = random.choice(valores)
    b = random.choice(valores)
    x = random.choice(valores)
    c = (a*x**2 + b*x)*(-1)
    return a,b,c,x

def gera_3g():
    valores = list(range(menor_valor, maior_valor))
    valores.remove(0)
    a = random.choice(valores)
    b = random.choice(valores)
    c = random.choice(valores)
    x = random.choice(valores)
    d = (a*x**3 + b*x**2 + c*x)*(-1) 
    return a,b,c,d,x