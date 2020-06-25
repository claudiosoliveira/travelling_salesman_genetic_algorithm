
import numpy as np
import math
import random
import operator
import pandas as pd

regiao = {}


class Cidade:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    



def calcularDistancia(indiceGene1, indiceGene2):
    # distancia euclidiana
    return math.sqrt((regiao[indiceGene1].x - regiao[indiceGene2].x)**2 + (regiao[indiceGene1].y - regiao[indiceGene2].y)**2)

def funcaoObjetivo(cromossomo):
    custo = 0.

    for indiceGene in range(0, len(cromossomo)-1):
        custo += calcularDistancia(cromossomo[indiceGene],cromossomo[indiceGene+1])

    return custo


def melhorCromossomo(populacao, flag, melhor):
    melhorIndice = 0

    for i in range(1, len(populacao)):
        if funcaoObjetivo(populacao[i]) < funcaoObjetivo(populacao[melhorIndice]):
            melhorIndice = i
    
    if len(melhor) == 0:
        for cr in populacao[melhorIndice]:
            melhor.append(cr)
        flag = True
    elif funcaoObjetivo(populacao[melhorIndice]) < funcaoObjetivo(melhor):
        melhor = populacao[melhorIndice]
        flag = True
    else:
        flag = False

    return melhor

def mutacao_cromossomo(cromossomo, taxa_mutacao):
    cromossomoMutado = cromossomo.copy()

    for indiceGene in range(0, len(cromossomo)):

        valor = random.uniform(0, 1)

        if valor <= taxa_mutacao:
            indiceMudado = int(int((valor*100)) % len(cromossomo))

            cromossomoMutado[indiceGene], cromossomoMutado[indiceMudado] = cromossomoMutado[indiceMudado], cromossomoMutado[indiceGene]
            if funcaoObjetivo(cromossomoMutado) < funcaoObjetivo(cromossomo):
                cromossomo = cromossomoMutado

    return cromossomo


def mutacao(populacao, taxaMutacao):
    for cromossomo in populacao:
        cromossomo = mutacao_cromossomo(cromossomo, taxaMutacao)
    
    return populacao


def cruzamento_cromossomo(c1, c2, pcorte):
    filho = np.zeros(len(c1), dtype=np.int32)
    indiceFilho = 0

    for i in range(0, pcorte):
        filho[indiceFilho] = c1[i]
        indiceFilho += 1

    indicePai = indiceFilho
    
    while indiceFilho < len(c1)-1:

        gene = c2[indicePai%len(c2)]
        gene_esta = np.where(filho==gene)[0].shape[0]
        
        if gene_esta is 0:
            filho[indiceFilho] = gene
            indiceFilho += 1
        indicePai += 1
    return filho


def cruzamento(populacao):
    filhos = []
    pcorte = len(populacao[0])//2
    for i in range(0, len(populacao)-1):
        # fazer o cruzamento para o primeiro
        filhos.append([cruzamento_cromossomo(
            populacao[i], populacao[i+1], pcorte), i])
        # fazer o cruzamento invertendo as ordens do cromossomo
        filhos.append([cruzamento_cromossomo(
            populacao[i+1], populacao[i], pcorte), i+1])
   
    for filho in filhos:
        # filho => [cromossomo, indice do pai]
        # cromossomo = [0, 1, 2, 3, 4, 5]
        # se o custo do filho for menor, populacao ira receber o cromossomo do filho
        if funcaoObjetivo(filho[0]) < funcaoObjetivo(populacao[filho[1]]):
            populacao[filho[1]] = filho[0]
    return populacao



def criarRota(listaCidades):
    rotaAleatoria = np.zeros(len(listaCidades), dtype=np.int32)
    
    for i in range(0, len(listaCidades)):
        rotaAleatoria[i] = int(i)

    random.shuffle(rotaAleatoria)

    return rotaAleatoria

def populacaoInicial(tamanhoPopulacao, listaCidades):
    populacao_inicial = []

    for i in range(0, tamanhoPopulacao):
        populacao_inicial.append(criarRota(listaCidades))

    return populacao_inicial

def algoritmoGenetico(listaCidade, tamanhoPopulacao, taxaMutacao, geracoes):
    populacao = populacaoInicial(tamanhoPopulacao, listaCidade)

    flag = False
    melhor = []

    for i in range(0, geracoes):

        # calcular cruzamento
        populacao = cruzamento(populacao)
        
        # calcular mutacao
        populacao = mutacao(populacao, taxaMutacao)

        # pegar o melhor caminho
        melhor = melhorCromossomo(populacao, flag, melhor)


        # mostrar melhor caminho
        print("Melhor Caminho: {}".format(melhor))
        print("Custo: {}".format(funcaoObjetivo(melhor)))



listaCidades = []
listaCidades.append(Cidade(0, 0)) # 0
listaCidades.append(Cidade(8.3, 16)) # 1 
listaCidades.append(Cidade(16, 12.8)) # 2
listaCidades.append(Cidade(2.23, 15)) # 3
listaCidades.append(Cidade(9, 7.87)) # 4
listaCidades.append(Cidade(6.7, 12)) # 5


for i,cidade in enumerate(listaCidades):
    regiao[i] = Cidade(cidade.x, cidade.y)


algoritmoGenetico(listaCidades, tamanhoPopulacao=10, taxaMutacao=0.1, geracoes=100)

