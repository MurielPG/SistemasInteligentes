# para o labirinto, necessariamente precisa ter um tamanho de no maximo 9x9
# o labirinto consiste em uma matriz de arrays inteiros
# valores 1 sao considerados obstaculos ou paredes, 2 onde inicia, 3 onde termina
# os valores 0 sao caminhos possiveis para percorrer
# por fim, o melhor caminho eh representado por 8


import numpy as np
import queue

fila = queue.Queue()

class Node:
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val

class Tree:
    def __init__(self, root):
        self.root = Node(root)

    def getRoot(self):
        return self.root

    def add(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if val < node.v:
            if node.l is not None:
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if node.r is not None:
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        if self.root is not None:
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if val == node.v:
            return node
        elif (val < node.v and node.l is not None):
            return self._find(val, node.l)
        elif (val > node.v and node.r is not None):
            return self._find(val, node.r)

    def deleteTree(self):
        self.root = None

    def printTree(self):
        global fila
        if self.root is not None:
            self._printTree(self.root)

    def _printTree(self, node):
        global fila
        if node is not None:
            self._printTree(node.l)
            #print(str(node.v) + ' ')
            fila.put(node.v)
            self._printTree(node.r)
        

def criaLab1():
    labirinto = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1, 1]])
   
    return labirinto

def criaLab():
    labirinto = np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 2],
    [1, 1, 1, 0, 0, 0, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 0, 1, 0],
    [1, 1, 1, 0, 1, 1, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 3, 1, 1, 1, 1, 1]])
   
    return labirinto



def matrizCoordenada():    
    matriz_coordenadas = np.array([
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],
    [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8],
    [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8],
    [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8],
    [5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8],
    [6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8],
    [7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8],
    [8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8]])

    return matriz_coordenadas

def coordenada_inicio():
    l = 0
    c = 0
    for x in criaLab():
        c=0
        for y in x:
            if (y == 2):
                return(l,c)
            c+=1
        l+=1

def posicaoValida(lab, x_, y_, tree):
    if not(0 <= x_ < len(lab) and 0 <= y_ < len(lab[0])):
        return False
    elif (lab[x_][y_] == 1):
        return False
    elif tree.find((x_)*10 + (y_)):
        return False
    return True
    
def procuraCaminho(lab, l, c, tree):
    if ( posicaoValida(lab, l+1, c, tree )): #baixo
        l+=1
        testaChegada(lab, l, c)
        tree.add( (l)*10 + (c) )
        return l, c
    elif ( posicaoValida(lab, l, c+1, tree) ): #direita
        c+=1
        testaChegada(lab, l, c)
        tree.add( (l)*10 + (c) )
        return l, c

    elif ( posicaoValida(lab, l, c-1, tree )): #esquerda
        c-=1
        testaChegada(lab, l, c)
        tree.add( (l)*10 + (c) )
        return l, c

    elif ( posicaoValida(lab, l-1, c, tree )): #cima
        l-=1
        testaChegada(lab, l, c)
        tree.add( (l)*10 + (c) )
        return l, c
    
    return False

def imprimeLabirinto(lab, fila):
    for _ in range(fila.qsize()-1):
        pos = fila.get()
        if pos == 2:
            continue
        if pos < 10:
            l = 0
            c = pos
        else:
            l = int(pos/10)
            c = pos - l*10
        lab[l][c] = 8
    print(lab)
    
def testaChegada(lab, l, c):
    if (lab[l][c] == 3):
        return True
    return False

labirinto = criaLab()
l_, c_ = coordenada_inicio()
arvore = Tree( labirinto[l_][c_] )

while not testaChegada(labirinto, l_, c_):
    l_, c_ = procuraCaminho(labirinto, l_, c_, arvore)

arvore.printTree()
imprimeLabirinto(labirinto, fila)
