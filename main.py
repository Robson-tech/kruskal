import datetime
import pygame as pg
import grafos
import widgets
import settings
import copy


class State:
    def __init__(self, grafo: grafos.Grafo):
        self.time = datetime.datetime.now()
        self.grafo = grafo

    def __str__(self):
        return f'{datetime.datetime.now()} - {self.grafo} - Action: {self.action}'


class Memory:
    def __init__(self):
        self.slots = 10
        self.states = [None for _ in range(self.slots)]

    def save_state(self, state: State, index: int):
        if index < 0 or index > self.slots - 1:
            raise IndexError('Index out of range')
        self.states.insert(index, state)
        
    def load_state(self, index: int):
        return self.states[index]


class Simulator:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(settings.RES)
        pg.display.set_caption(settings.TITLE)
        self.clock = pg.time.Clock()
        self.fps = settings.FPS
        self.running = True
        self.move_vertices = False
        self.grafo = grafos.Grafo()
        self.memory = Memory()
        self.widget = widgets.WidgetArestaWeight()
        self.selected1 = None
        self.selected2 = None
        self.moving_vertice = None
    
    def reset(self):
        self.grafo.vertices = []
        self.grafo.arestas = []
        self.widget = widgets.WidgetArestaWeight()
        self.selected1 = None
        self.selected2 = None

    def event_loop(self):
        for event in pg.event.get():
            # Fecha o programa ao apertar o botão de fechar ou ESC
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.running = False
            # Adiciona vértices com o botão esquerdo do mouse e arestas com o botão direito
            if event.type == pg.MOUSEBUTTONDOWN and not self.widget.active:
                if event.button == 1:
                    if not self.move_vertices:
                        self.grafo.vertices.append(grafos.Vertice(*event.pos, len(self.grafo.vertices)))
                    else:
                        for vertice in self.grafo.vertices:
                            if vertice.check_collision(event.pos):
                                self.moving_vertice = vertice
                if event.button == 3:
                    for vertice in self.grafo.vertices:
                        if vertice.check_collision(event.pos):
                            vertice.turn_on()
                            if self.selected1 is None:
                                self.selected1 = vertice
                            elif self.selected2 is None and vertice != self.selected1:
                                self.selected2 = vertice
                                if not grafos.procurar_aresta(self.grafo.arestas, self.selected1, self.selected2):
                                    self.widget.active = True
                                else:
                                    self.selected1.turn_off()
                                    self.selected2.turn_off()
                                    self.selected1 = None
                                    self.selected2 = None
            # Move o vértice selecionado
            if event.type == pg.MOUSEMOTION and self.moving_vertice is not None:
                self.moving_vertice.move(event.pos)
            # Solta o vértice selecionado
            if event.type == pg.MOUSEBUTTONUP and self.moving_vertice is not None:
                self.moving_vertice = None
            # Adiciona o peso da aresta
            if event.type == pg.KEYDOWN and self.widget.active:
                if event.key == pg.K_RETURN:
                    self.widget.active = False
                    self.grafo.arestas.append(grafos.Aresta(self.selected1, self.selected2, int(self.widget.text)))
                    self.selected1.turn_off()
                    self.selected2.turn_off()
                    self.selected1 = None
                    self.selected2 = None
                    self.widget.text = ''
                if event.key == pg.K_BACKSPACE:
                    self.widget.text = self.widget.text[:-1]
                elif event.unicode.isdigit():
                    self.widget.text += event.unicode
            # Move os vértices ao apertar a tecla 'm'
            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.move_vertices = not self.move_vertices
                pg.mouse.set_system_cursor(pg.SYSTEM_CURSOR_HAND if self.move_vertices else pg.SYSTEM_CURSOR_ARROW)
            # Desseleciona o vértice ao apertar a tecla 'backspace'
            if event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE and not self.widget.active:
                if self.selected1 is not None:
                    self.selected1.turn_off()
                    self.selected1 = None
            # Reseta o grafo ao apertar a tecla 'r'
            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.reset()
            # Encontra a árvore geradora mínima do grafo ao apertar a barra de espaço
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.grafo.arestas = grafos.encontrar_AGM(self.grafo.arestas, len(self.grafo.vertices))
            # Salva o estado atual do grafo ao apertar a tecla 's'
            if event.type == pg.KEYDOWN and event.key == pg.K_s:
                self.memory.save_state(State(copy.deepcopy(self.grafo)), 0)
            # Carrega o estado anterior do grafo ao apertar a tecla 'l'
            if event.type == pg.KEYDOWN and event.key == pg.K_l:
                self.grafo = self.memory.load_state(0).grafo

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(settings.BG_COLOR)
        for aresta in self.grafo.arestas:
            aresta.draw(self.screen)
        for vertice in self.grafo.vertices:
            vertice.draw(self.screen)
        if self.widget.active:
            self.widget.draw(self.screen)
        num_vertices = len(self.grafo.vertices)
        num_arestas = len(self.grafo.arestas)
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