import pygame

from drawing_surface import scale_vertices


class ButtonCollection(object):
    def __init__(self):
        self.buttons = []

    def add(self, rectangle, action):
        self.buttons.append(Button(rectangle, action))

    def process_mouse_click(self):
        mouse_position = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.clicked(mouse_position):
                button.action.activate()

class Button(object):
    def __init__(self, rectangle, action):
        self.rectangle = scale_vertices(rectangle)
        self.action = action

    def clicked(self, mouse_position):
        return self.rectangle[0] <= \
               mouse_position[0] <= \
               self.rectangle[0] + self.rectangle[2] and \
               self.rectangle[1] <= \
               mouse_position[1] <= \
               self.rectangle[1] + self.rectangle[3]

buttons = ButtonCollection()
