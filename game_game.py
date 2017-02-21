import pygame
# TODO: Better name for this module?


class Game(object):
    """
    Container for game elements - table, players, holding area
    Plus some helper methods
    """

    def __init__(self):
        self.players = None
        self.table = None
        self.holding_area = None
        self.game_state = None
        self.buttons = None

    def init_game(self, players, table, holding_area, game_state, buttons):
        self.players = players
        self.table = table
        self.holding_area = holding_area
        self.game_state = game_state
        self.buttons = buttons

    @property
    def player_count(self):
        """
        Some of the game rules depend on the number of players
        :return: Number of players
        """
        return len(self.players)

    @property
    def current_player(self):
        """
        Players can be in different states. All but one player
        will always be 'waiting', whilst the other (current) player
        will be in one of the other states
        :return: The one player who currently isn't 'waiting'
        """
        return [p for p in self.players if p.is_current_player][0]

    def next_player(self):
        """
        Move to the next player
        """
        current = self.current_player

        # Confirm the current player's action
        current.confirm()

        # Find the index of the next player
        i = self.players.index(current)
        try:
            next_p = self.players[i + 1]
        except IndexError:
            next_p = self.players[0]

        # The next player can start their turn
        next_p.start()

    def embody(self):
        """
        Embody the game
        - Create all available buttons
        - Draw the table, holding and player areas
        """

        # Remove previously created buttons
        game.buttons.reset()

        self.table.embody()
        for player in self.players:
            player.embody()
        self.holding_area.embody()

    def refresh_display(self):
        """
        Show the current game state
        Called after every state change, e.g. after player
        clicks on a piece (which moves it to the holding area)
        """
        self.embody()
        pygame.display.flip()


game = Game()
