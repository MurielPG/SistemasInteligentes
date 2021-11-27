import queue
import numpy as np

# para o labirinto, necessariamente precisa ter um tamanho de no maximo 9x9
# o labirinto consiste em uma matriz de arrays inteiros
# valores 1 sao considerados obstaculos ou paredes, 2 onde inicia, 3 onde termina
# os valores 0 sao caminhos possiveis para percorrer
# foi utilizado um sistema de fila FIFO

def criaLab1():
    labirinto = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1, 1]])
    return labirinto

def criaLab():
    labirinto = np.array([
    [1, 1, 1, 1, 0, 0, 0, 1, 2],
    [1, 1, 1, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 3, 1, 1, 1, 1, 1]])
    return labirinto

def coordenada_inicio(labirinto):
    l = 0
    c = 0
    for x in labirinto:
        c=0
        for y in x:
            if (y == 2):
                return l,c
            c+=1
        l+=1

def encontraFinal(labirinto, linha, coluna):
    if labirinto[linha][coluna] == 3:
        return True
    else:
        return False

def posicaoValida(lab, linha, coluna):
    if not(0 <= linha < len(lab) and 0 <= coluna < len(lab[0])):
        return False
    if (lab[linha][coluna] == 0):
        return True
    elif (lab[linha][coluna] == 3):
        return True
    return False

def coordenadas(lab, caminho):
    if caminho is None:
        return coordenada_inicio(lab)

    l, c = coordenada_inicio(lab)
    for passo in caminho:
        if passo == "C":
            l-=1
        if passo == "B":
            l+=1
        if passo == "E":
            c-=1
        if passo == "D":
            c+=1 
        if not(0 <= l <= 9 and 0 <= c <= 9):
            return False
        elif (lab[l][c] == "#"):
            return False
    return l, c

def encontraCaminho(lab, l, c, caminho):
    if posicaoValida(lab, l+1, c): #baixo
        add = caminho + "B"
        if not visitado(caminho):
            fila.put(add)

    if posicaoValida(lab, l, c-1): #esquerda
        add = caminho + "E"
        if not visitado(caminho):
            fila.put(add)

    if posicaoValida(lab, l, c+1): #direita
        add = caminho + "D"
        if not visitado(caminho):
            fila.put(add)
    if posicaoValida(lab, l-1, c): #cima
        add = caminho + "C"
        if not visitado(caminho):
            fila.put(add)

def visitado(caminho):
    if len(caminho) < 3:
        return False
    if (caminho[-1] == "E" and caminho[-2] == "D"):
        return True
    if (caminho[-1] == "D" and caminho[-2] == "E"):
        return True
    if (caminho[-1] == "C" and caminho[-2] == "B"):
        return True
    if (caminho[-1] == "B" and caminho[-2] == "C"):
        return True
    return False

def imprimeLabirinto(lab, caminho):
    if caminho is None:
        return False
    caminho_ = caminho[:-1]
    l, c = coordenada_inicio(lab)
    for passo in caminho_:
        if passo == "B":
            l+=1
            lab[l][c] = 8
        if passo == "E":
            c-=1
            lab[l][c] = 8
        if passo == "D":
            c+=1 
            lab[l][c] = 8
        if passo == "C":
            l-=1 
            lab[l][c] = 8
        
    return lab

labirinto = criaLab()
linha, coluna = coordenada_inicio(labirinto)

fila = queue.Queue()
fila.put("")

while not encontraFinal(labirinto, linha, coluna):
    caminho = fila.get()
    linha, coluna = coordenadas(labirinto, caminho)
    encontraCaminho(labirinto, linha, coluna, caminho)

print(caminho)
print(imprimeLabirinto(labirinto, caminho))
