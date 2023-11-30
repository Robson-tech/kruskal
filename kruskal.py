# Estrutura para representar um subconjunto do algoritmo de Kruskal
class Subconjunto:
    def __init__(self, pai, classificacao):
        self.pai = pai
        self.classificacao = classificacao


# Estrutura para representar uma aresta do grafo
class Aresta:
    def __init__(self, origem, destino, peso):
        self.origem = origem
        self.destino = destino
        self.peso = peso


# Função para encontrar a árvore geradora mínima utilizando o algoritmo de Kruskal
def encontrar_AGM(arestas, n):
    agm = []  # Árvore geradora mínima
    subconjuntos = []

    # Função auxiliar para encontrar o subconjunto de um elemento 'i'
    def encontrar(subconjuntos, i):
        if subconjuntos[i].pai != i:
            subconjuntos[i].pai = encontrar(subconjuntos, subconjuntos[i].pai)
        return subconjuntos[i].pai

    # Função auxiliar para realizar a união de dois subconjuntos x e y
    def unir(subconjuntos, x, y):
        raiz_x = encontrar(subconjuntos, x)
        raiz_y = encontrar(subconjuntos, y)

        if subconjuntos[raiz_x].classificacao < subconjuntos[raiz_y].classificacao:
            subconjuntos[raiz_x].pai = raiz_y
        elif subconjuntos[raiz_x].classificacao > subconjuntos[raiz_y].classificacao:
            subconjuntos[raiz_y].pai = raiz_x
        else:
            subconjuntos[raiz_y].pai = raiz_x
            subconjuntos[raiz_x].classificacao += 1

    # Ordena as arestas em ordem crescente de peso
    arestas.sort(key=lambda x: x.peso)

    # Inicializa os subconjuntos
    for i in range(n):
        subconjuntos.append(Subconjunto(i, 0))

    i = 0  # Índice para percorrer as arestas
    while len(agm) < n - 1 and i < len(arestas):
        aresta = arestas[i]

        raiz_origem = encontrar(subconjuntos, aresta.origem)
        raiz_destino = encontrar(subconjuntos, aresta.destino)

        # Se a adição da aresta não forma um ciclo, adiciona-a à árvore geradora mínima
        if raiz_origem != raiz_destino:
            agm.append(aresta)
            unir(subconjuntos, raiz_origem, raiz_destino)

        i += 1
    return agm


if __name__ == '__main__':
    arestas = [
        Aresta(0, 2, 7),
        Aresta(0, 4, 4),
        Aresta(0, 5, 7),
        Aresta(2, 1, 8),
        Aresta(2, 4, 6),
        Aresta(4, 1, 7),
        Aresta(1, 5, 5),
        Aresta(1, 3, 3),
        Aresta(5, 3, 4),
    ]

    agm = encontrar_AGM(arestas, 6)

    print('Árvore geradora mínima:')
    for aresta in agm:
        print(f'{aresta.origem} - {aresta.destino}: {aresta.peso}')