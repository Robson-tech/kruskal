import pygame as pg
import settings


class Vertice:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.color = settings.RED
        self.radius = settings.RAIO
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
    
    def __str__(self):
        return f'V{self.id}({self.x}, {self.y})'

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        txt = pg.font.SysFont(settings.BASE_FONT, settings.VERTICES_FONT).render(str(self.id), True, settings.WHITE)
        screen.blit(txt, (self.x - txt.get_width() / 2, self.y - txt.get_height() / 2))
    
    def turn_on(self):
        self.color = settings.GREEN

    def turn_off(self):
        self.color = settings.RED

    def check_collision(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def move(self, mouse_pos):
        self.x, self.y = mouse_pos
        self.rect = pg.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


class Aresta:
    def __init__(self, v1, v2, weight=1):
        self.v1 = v1
        self.v2 = v2
        self.weight = weight
        self.color = settings.ORANGE
        self.thickness = settings.ESPESSURA

    def __str__(self):
        return f'A({self.v1.id}, {self.v2.id}, {self.weight})'

    def draw(self, screen):
        pg.draw.line(screen, self.color, (self.v1.x, self.v1.y), (self.v2.x, self.v2.y), self.thickness)
        txt = pg.font.SysFont(settings.BASE_FONT, settings.ARESTAS_FONT).render(str(self.weight), True, settings.WHITE)
        screen.blit(txt, ((self.v1.x + self.v2.x) / 2, (self.v1.y + self.v2.y) / 2))


class Grafo:
    def __init__(self, vertices=[], arestas=[]):
        self.vertices = vertices
        self.arestas = arestas

    def __str__(self):
        return f'Vertices: {len(self.vertices)} - Arestas: {len(self.arestas)}'


class Subconjunto:
    def __init__(self, pai, classificacao):
        self.pai = pai
        self.classificacao = classificacao


# Função para encontrar a árvore geradora mínima utilizando o algoritmo de Kruskal
def encontrar_AGM(arestas: list, n: int):
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
    arestas.sort(key=lambda x: x.weight)

    # Inicializa os subconjuntos
    for i in range(n):
        subconjuntos.append(Subconjunto(i, 0))

    i = 0  # Índice para percorrer as arestas
    while len(agm) < n - 1 and i < len(arestas):
        aresta = arestas[i]

        raiz_origem = encontrar(subconjuntos, aresta.v1.id)
        raiz_destino = encontrar(subconjuntos, aresta.v2.id)

        # Se a adição da aresta não forma um ciclo, adiciona-a à árvore geradora mínima
        if raiz_origem != raiz_destino:
            agm.append(aresta)
            unir(subconjuntos, raiz_origem, raiz_destino)

        i += 1
    return agm


def procurar_aresta(arestas: list, v1: Vertice, v2: Vertice):
    encontrado = False
    for aresta in arestas:
        if (aresta.v1 == v1 and aresta.v2 == v2) or \
           (aresta.v1 == v2 and aresta.v2 == v1):
            encontrado = True
            break
    return encontrado


if __name__ == '__main__':
    vertices = [
        Vertice(100, 100, 0),
        Vertice(300, 100, 1),
        Vertice(100, 300, 2),
        Vertice(300, 300, 3),
        Vertice(100, 500, 4),
        Vertice(300, 500, 5),
    ]
    arestas = [
        Aresta(vertices[0], vertices[2], 7),
        Aresta(vertices[0], vertices[4], 4),
        Aresta(vertices[0], vertices[5], 7),
        Aresta(vertices[2], vertices[1], 8),
        Aresta(vertices[2], vertices[4], 6),
        Aresta(vertices[4], vertices[1], 7),
        Aresta(vertices[1], vertices[5], 5),
        Aresta(vertices[1], vertices[3], 3),
        Aresta(vertices[5], vertices[3], 4),
    ]

    agm = encontrar_AGM(arestas, 6)

    print('Árvore geradora mínima:')
    for aresta in agm:
        print(f'{aresta.v1.id} - {aresta.v2.id}: {aresta.weight}')