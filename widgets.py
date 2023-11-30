import pygame as pg
import settings


class WidgetArestaWeight:
    def __init__(self):
        self.width = settings.WIDTH_WIDGET
        self.height = settings.HEIGHT_WIDGET
        self.rect = pg.Rect(
            settings.WIDTH / 2 - self.width / 2,
            settings.HEIGHT / 2 - self.height / 2,
            self.width,
            self.height
        )
        self.color = settings.COLOR_WIDGET
        self.text = ''
        self.font = pg.font.SysFont(settings.BASE_FONT, settings.ARESTAS_FONT)
        self.active = False

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
        txt = self.font.render(self.text, True, settings.WHITE)
        screen.blit(txt, (self.rect.x + 5, self.rect.y + 5))

    def check_collision(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)