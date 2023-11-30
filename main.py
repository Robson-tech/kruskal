import datetime
import pygame as pg
import grafos
import widgets
import settings


class State:
    def __init__(self, vertices: list, arestas: list, action: str):
        self.vertices = vertices
        self.arestas = arestas
        self.action = action

    def __str__(self):
        return f'vertices: {len(self.vertices)} - arestas: {len(self.arestas)} - action: {self.action}'


class Simulator:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.RES)
        pg.display.set_caption(settings.TITLE)
        self.clock = pg.time.Clock()
        self.fps = settings.FPS
        self.running = True
        self.states = []
        self.vertices = []
        self.arestas = []
        self.widget = widgets.WidgetArestaWeight()
        self.selected1 = None
        self.selected2 = None
        self.states.append(State(self.vertices.copy(), self.arestas.copy(), 'first_state'))
    
    def reset(self):
        self.vertices = []
        self.arestas = []
        self.widget = widgets.WidgetArestaWeight()
        self.selected1 = None
        self.selected2 = None

    def event_loop(self):
        for event in pg.event.get():
            # Fecha o programa ao apertar o botão de fechar ou ESC
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
            # Adiciona vértices com o botão esquerdo do mouse e arestas com o botão direito
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.widget.active:
                    self.vertices.append(grafos.Vertice(*event.pos, len(self.vertices)))
                    self.states.append(State(self.vertices.copy(), self.arestas.copy(), 'add_vertice'))
                if event.button == 3 and not self.widget.active:
                    for vertice in self.vertices:
                        if vertice.check_collision(event.pos):
                            vertice.turn_on()
                            if self.selected1 is None:
                                self.selected1 = vertice
                            elif self.selected2 is None:
                                self.selected2 = vertice
                                if not grafos.procurar_aresta(self.arestas, self.selected1, self.selected2):
                                    self.widget.active = True
                                else:
                                    self.selected1.turn_off()
                                    self.selected2.turn_off()
                                    self.selected1 = None
                                    self.selected2 = None
            # Adiciona o peso da aresta
            if event.type == pg.KEYDOWN and self.widget.active:
                if event.key == pg.K_RETURN:
                    self.widget.active = False
                    self.arestas.append(grafos.Aresta(self.selected1, self.selected2, int(self.widget.text)))
                    self.selected1.turn_off()
                    self.selected2.turn_off()
                    self.selected1 = None
                    self.selected2 = None
                    self.widget.text = ''
                    self.states.append(State(self.vertices.copy(), self.arestas.copy(), 'add_aresta'))
                if event.key == pg.K_BACKSPACE:
                    self.widget.text = self.widget.text[:-1]
                elif event.unicode.isdigit():
                    self.widget.text += event.unicode
            # Desseleciona o vértice ao apertar a tecla 'backspace'
            if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE and not self.widget.active:
                if self.selected1 is not None:
                    self.selected1.turn_off()
                    self.selected1 = None
            # Reseta o grafo ao apertar a tecla 'r'
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.reset()
                self.states.append(State(self.vertices.copy(), self.arestas.copy(), 'reset'))
            # Desfaz a última ação ao apertar a tecla 'z'
            if event.type == pg.KEYDOWN and event.key == pg.K_z:
                if len(self.states) > 1:
                    self.states.pop()
                    self.vertices = self.states[-1].vertices.copy()
                    self.arestas = self.states[-1].arestas.copy()
            # Encontra a árvore geradora mínima do grafo ao apertar a barra de espaço
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.arestas = grafos.encontrar_AGM(self.arestas, len(self.vertices))
                self.states.append(State(self.vertices.copy(), self.arestas.copy(), 'encontrar_AGM'))
            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                for num, state in enumerate(self.states):
                    print(f'{num}) {datetime.datetime.now()} - {state}')

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(settings.BG_COLOR)
        for vertice in self.vertices:
            vertice.draw(self.screen)
        for aresta in self.arestas:
            aresta.draw(self.screen)
        if self.widget.active:
            self.widget.draw(self.screen)
        num_vertices = len(self.vertices)
        num_arestas = len(self.arestas)
        font = pg.font.SysFont(settings.BASE_FONT, settings.BASE_FONT_SIZE)
        txt = font.render(f'Vertices: {num_vertices}', True, settings.WHITE)
        self.screen.blit(txt, (10, 10))
        txt = font.render(f'Arestas: {num_arestas}', True, settings.WHITE)
        self.screen.blit(txt, (10, 30))
        pg.display.set_caption(f'{settings.TITLE} - FPS: {self.clock.get_fps():.2f}')
        pg.display.update()

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(dt)
            self.draw()
        pg.quit()

if __name__ == '__main__':
    Simulator().run()