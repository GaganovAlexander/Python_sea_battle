import pygame as pg


CELL_WIDTH = 70


class Field:
    def __init__(self, surface: pg.surface.Surface, left: int, top: int) -> None:
        self.field = [[0 for _ in range(10)] for _ in range(10)]
        self.__surface = surface
        self.__colors = [(255, 255, 255), (0, 0, 255), (0, 255, 0), (255, 0, 0)]
        self.__left = left
        self.__top = top
        self.fields_rects = [[pg.Rect(self.__left + i*CELL_WIDTH, self.__top + j*CELL_WIDTH, CELL_WIDTH, CELL_WIDTH) for i in range(10)] for j in range(10)]

    def draw(self) -> None:
        for i in range(10):
            for j in range(10):
                pg.draw.rect(self.__surface, self.__colors[self.field[i][j]], self.fields_rects[i][j])
                pg.draw.rect(self.__surface, (0, 0, 0), self.fields_rects[i][j], 2)

    def check(self, pos: tuple, new_status: int) -> bool:
        for i in range(10):
            for j in range(10):
                if self.fields_rects[i][j].collidepoint(pos):
                    if self.field[i][j] != new_status:
                        self.field[i][j] = new_status
                        return True
                    else:
                        return False
        return False
    
    def get_pos(self, pos: tuple) -> str:
        for i in range(10):
            for j in range(10):
                if self.fields_rects[i][j].collidepoint(pos):
                    return f'{i}{j}'
                    