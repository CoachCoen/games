from settings import config
import pygame

from graphics import draw_table


class Game:
    """
    Container for game elements - components, players - and mechanics
    """
    def __init__(self):
        self.components = None
        self.current_player = None
        self.buttons = None
        self.players = None
        self.mechanics = None

    def init_game(self, players, buttons, components, mechanics):
        self.players = players
        self.components = components
        self.buttons = buttons
        self.mechanics = mechanics

    @property
    def last_player(self):
        return self.current_player == self.players[-1]

    def embody(self):
        game.buttons.reset()
        draw_table(self.mechanics.final_round)

        self.components.table_chips.embody()

        self.components.table_card_stacks.embody(
            location=config.central_area_location + config.card_decks_location
        )

        self.components.table_card_grid.embody()

        for tile in self.components.table_tiles.components:
            tile.embody()

        self.components.holding_area.embody()

        # There can only be one card in the holding area -
        # no need to specify a column
        for card in self.components.holding_area_cards:
            card.embody()

        for player in self.players:
            player.embody()

        pygame.display.flip()


game = Game()
