"""
Projeto 1 da disciplina Teoria e Aplicação de Grafos

Universidade de Brasilia
Instituto de Ciencias Exatas
Departamento de Ciencia da Computacao
Teoria e Aplicação de Grafos – 2/2020
Professor: Díbio Leandro Borges
Desenvolvido por: Guilherme Silva Souza
02/03/2021

Descrição: O objetivo desse programa é aplicar o algoritimo de Bron-Kerbosh para achar cliques maximais em um grafo e encontrar o coeficiente de aglomeração. O grafo que foi utilizado foi disponibilizado no artigo “David Lusseau et al., The bottelenose dolphin community of Doubful Sound features a large proportion of long-lasting associations, Journal of Behavioral Ecology and Sociobiology 54:4, 396--405 (2003).”. Ele consiste em uma rede social de relações duradouras é identificada em uma comunidade de 62 golfinhos e apresentada como um grafo (não direcionado) para estudos. O programa lê o arquivo (soc-dolphins.mtx), monta com esses dados um grafo não direcionado, sem pesos, e então realiza o seguinte:

(1) Implementa duas formas do algoritmo Bron-Kerbosch: uma com pivotamento, outra sem
pivotamento;
(2) Encontra e imprime na tela (duas vezes, uma para cada implementação do Bron-Kerbosch) todos os
cliques maximais (indicando o número de vértices e quais);
(3) O Coeficiente médio de Aglomeração do Grafo.
"""

from pathlib import Path
import random
from collections import defaultdict


class Graph(object):
    """ Implementação básica de um grafo. """

    def __init__(self, edges):
        """
        Inicializa as estruturas base do grafo
        """
        self.adj = defaultdict(set)
        self.add_edges(edges)

    def get_edges(self):
        """ 
        Função para retornar a lista de arestas do grafo
        """
        return [(k, v) for k in self.adj.keys() for v in self.adj[k]]

    def add_edges(self, edges):
        """
        Função responsável por adicionar arestas ao grafo
        """
        for u, v in edges:
            self.adj[v].add(u)
            self.adj[u].add(v)


def createGraph():
    """
    Função onde eu monto o grafo a partir do arquivo dado
    """
    script_location = Path(__file__).absolute().parent
    file_location = script_location / 'soc-dolphins.mtx'

    edges = []
    with open(file_location) as file:
        for line in file:
            aux = [int(i) for i in line.split()]
            edges.append((aux[0], aux[1]))

    graph = Graph(edges)
    return dict(graph.adj)


def BronKerboschWithoutPivot(P, R=None, X=None):
    """
    A função é responsável pela aplicação do algoritimo de Bron-Kerbosh sem pivotamento. A forma básica do algoritmo de Bron-Kerbosch é uma função recursiva que procura todos os 
    cliques maximais em um dado grafo G . Ela recebe três conjuntos disjuntos de vértices R, P e X, nessa implementação o R e o X iniciam vazios, que encontra os cliques maximais que 
    incluem todos os vértices R, alguns dos vértices em P , e nenhum dos vértices em X . Em cada chamada para a função, P e X são conjuntos disjuntos cuja união é constituída por 
    aqueles que formam os vértices cliques quando adicionados a R. Em outras palavras, P ∪ X é o conjunto de vértices que são unidos a cada elemento de R . Quando P e X estão vazios, não há mais elementos que possam ser
    adicionados a R , então R é um clique máximo e o algoritmo gera R. 
    """
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R  
    while P:
        v = P.pop()
        yield from BronKerboschWithoutPivot(
            P=P.intersection(graph[v]), R=R.union([v]), X=X.intersection(graph[v]))
        X.add(v)


def BronKerboschWithPivot(P, R=None, X=None):
    """
    A função é responsável pela aplicação do algoritimo de Bron-Kerbosh com pivotamento. O algoritimo de Bron-Kerbosh sem pivotamento é ineficiente no caso de grafos com muitos
    cliques não máximos: ele faz uma chamada recursiva para cada clique, máximo ou não. Para economizar tempo e permitir que o algoritmo retroceda mais rapidamente nos ramos da
    pesquisa que não contêm cliques máximos, Bron e Kerbosch introduziram uma variante do algoritmo envolvendo um "vértice pivô" u , escolhido de P (ou mais geralmente, como 
    investigadores posteriores realizado, a partir de P ⋃ X ). Qualquer clique máximo deve incluir u ou um de seus não vizinhos, caso contrário, o clique poderia ser aumentado
    adicionando u a ele. Portanto, apenas u e seus não vizinhos precisam ser testados como escolhas para o vértice v que é adicionado a R em cada chamada recursiva ao algoritmo. 
    Nessa implementação o pivô é escolhido de maneira aleatória.
    """
    P = set(P)
    R = set() if R is None else R
    X = set() if X is None else X
    if not P and not X:
        yield R
    try:
        u = random.choice(list(P.union(X)))  # escolha do pivô aleatorianente
        S = P.difference(graph[u])
    except IndexError:  # caso o u não esteja na lista
        S = P
    for v in S:
        yield from BronKerboschWithPivot(
            P=P.intersection(graph[v]), R=R.union([v]), X=X.intersection(graph[v]))
        P.remove(v)
        X.add(v)


def clustering(g):
    """
    A função é responsavel por calcular o coeficiente de aglomeração do grafo
    """

    def has_edge(n1, n2):
        """
        A subfunção é responsavel por verificar se dois vertices são conectados
        """

        neighbours = g.get(n1, [])
        if n2 in neighbours:
            return True

        neighbours = g.get(n2, [])
        if n2 in neighbours:
            return True

        return False

    result = {}
    
    # Esse laço é responsavel de achar os coeficiente de cada vertice. Ele verifica se um vertice tem o número de vizinhos maior que 1, se tiver ele olha cada vizinho e verifica se os 
    # dois vertices estão conectados, se sim ele calcula o coeficiente e adiciona o coeficiente na varivel result. 
    
    for node in g:

        neighbours = g[node]
        n_neighbors = len(neighbours)
        n_links = 0

        if n_neighbors > 1:
            for node1 in neighbours:
                for node2 in neighbours:
                    if has_edge(node1, node2):
                        n_links += 1

            n_links /= 2  # aqui é dividido por dois para evitar as duplicatas
            result[node] = (2*n_links) / (n_neighbors*(n_neighbors-1))
        else:
            result[node] = 0

    # Aqui eu calculo o coeficiente geral do grafo pela formula: 1/N * sum(Ci) 
    # onde N é o número de nós no grafo e ci é o coeficiente de aglomeração do nó i.
    
    coefficient = 0
    for i in result:
        coefficient += result[i]
    coefficient = (1 / 62) * coefficient
    return coefficient


if __name__ == "__main__":
    """
    Abaixo fica responsavel de chamar o algoritimo de Bron-Kerbosh, com e sem pivô, e calcular o coeficiente de aglomeção do grafo
    """
    graph = createGraph()
    P = graph.keys()  # aqui eu crio uma lista com todos os vertices do grafo

    print("\nExecutando o algoritimo de Bronkerbosck sem pivotamento:")
    print(f'{len(list(BronKerboschWithoutPivot(P)))} cliques maximais encontrados!')
    print(f'Cliques Maximais: {list(BronKerboschWithoutPivot(P))}\n')

    P = graph.keys()
    print("Executando o algoritimo de Bronkerbosck com pivotamento:")
    print(f'{len(list(BronKerboschWithPivot(P)))} cliques maximais encontrados!')
    print(f'Cliques Maximais: {list(BronKerboschWithPivot(P))}')

    print(f'\nCoeficiente de Aglomeração: {clustering(graph)}\n')
