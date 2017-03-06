"""
Obsolete code during large refactoring exercise
Some may go back into the code
"""

class CardCollection():
    """
    Card deck class - a collection of cards
    """
    def __init__(self, components):
        super().__init__(components)
        # self.cards = cards
        # self.location = None
        # self.player_order = None
        # self.scaling_factor = 1

        # shuffle(self.cards)

    def __len__(self):
        return len(self.cards)

    def empty(self):
        """
        Remove all cards
        """
        self.cards = []

    def pop(self):
        """
        Return the top card of the deck
        """
        return self.cards.pop() if self.cards else None

    def take_card(self, card):
        index = self.cards.index(card)
        if index > -1:
            del(self.cards[index])

    def add(self, card):
        """
        Add the card to the deck
        """
        self.cards.append(card)

    def contains(self, card):
        """
        Returns True if the card is in this deck
        """
        return card in self.cards

    @property
    def counts_for_type(self):
        """
        Returns a dict {chip_type: number of cards which produce these}
        :return:
        """
        return {
            chip_type: self._count_for_reward_type(chip_type)
            for chip_type in ChipType
        }

    def produces_for_chip_type(self, chip_type):
        # TODO: make a single function?
        return self._count_for_reward_type(chip_type)

    def _count_for_reward_type(self, chip_type):
        """
        How many cards are there of the given chip type
        """
        return sum([1 for c in self.cards
                    if c.reward_chip.chip_type == chip_type])

    @property
    def points(self):
        """
        Total number of (victory) points in this deck
        """
        return sum(c.points for c in self.cards)

    def embody(self, location,
               scaling_factor=1, player_order=None):
        """
        Draw the card deck at this location
        """
        self.location = location
        self.player_order = player_order
        self.scaling_factor = scaling_factor
        if self.player_order is not None:
            self.draw_as_cards()
        else:
            self._draw_as_deck()

    def draw_as_cards(self):
        """
        Draw as a spread out row of cards
        """
        for i, card in enumerate(self.cards):
            card.embody(
                location=self.location + Vector(
                    1.1 * i * config.card_size.x, 0
                ),
                player_order=self.player_order
            )

    def _draw_as_deck(self):
        """
        Draw the card deck: rectangle and number of cards
        """
        if len(self.cards):
            draw_rectangle(self.location.to_rectangle(config.card_size),
                           ColourPalette.card_deck_background)
            draw_text(
                self.location + config.points_location,
                str(len(self.cards))
            )


class CardGrid():
    """
    Grid, 3 rows of 4 cards
    """
    def __init__(self, cards):
        self.cards = cards

    def contains(self, card):
        """
        Is this card anywhere in the grid?
        """
        return any(card in row for row in self.cards)

    def fill_empty_spaces(self):
        """
        Goes through every card slot. If it is empty, draws
        a card (if available) to fill the empty slot
        """
        for i, row in enumerate(self.cards):
            for j, card in enumerate(row):
                if not card:
                    self.cards[i][j] = game.table.card_decks[i].pop()

    def return_card(self, card):
        """
        Note: Should only be called if there is one slot free
        Puts the card in the first (and only) free slot
        """
        for i, row in enumerate(self.cards):
            for j, c in enumerate(row):
                if not c:
                    self.cards[i][j] = card
                    return

    def take_card(self, card):
        """
        Removes the card from the grid
        """
        for i in range(3):
            for j in range(4):
                if self.cards[i][j] == card:
                    self.cards[i][j] = None

        # # self.player_order = player_order
        # self.sub_components = [
        #     (chip_cost, self.location + config.cost_location,
        #      config.chip_cost_scaling),
        #     # (chip_type, config.reward_chip_location,
        #     #  config.reward_chip_scaling)
        # ]

    # @property
    # def position(self):
    #     """
    #     Where is the card: holding_area, player's hand or card grid
    #     """
    #     if self == game.holding_area.card:
    #         return ComponentState.holding_area
    #
    #     if game.current_player.cards.contains(self):
    #         return ComponentState.player
    #
    #     if game.table.card_grid.contains(self):
    #         return ComponentState.card_grid
    #
    #     if game.current_player.reserved.contains(self):
    #         return ComponentState.reserved




    # def move_to_holding_area(self):
    #     self.previous_position = self.position
    #     if self.position == ComponentState.card_grid:
    #         game.table.card_grid.take_card(self)
    #     elif self.position == ComponentState.reserved:
    #         game.current_player.reserved.take_card(self)
    #     game.holding_area.card = self

    # def move_to(self, target):
    #     self.remember_position()
    #     # Remove from current position
    #
    #     if self.position == ComponentState.table:
    #     # Move to target


class ChipCollection():
    # def __init__(self):
    #     self.chips = []
    #     self.location = None

    def return_chips(self):
        for chip in self.chips[:]:
            # chip.return_to_supply()
            chip.return_to_previous_position()
        # self.chips = []

    def transfer_chips(self, target):
        for chip in self.chips[:]:
        #     chip.move_to(target)
            target.add_one(chip)
        self.chips = []

    def contains(self, chip):
        return chip in self.chips

    def count(self, chip_type):
        return sum(1 for chip in self.chips if chip.chip_type == chip_type)

    @property
    def counts_for_type(self):
        return {
            chip_type: self.count(chip_type=chip_type)
            for chip_type in ChipType
        }

    def top_chips(self):
        return [
            self.first_chip_of_type(chip_type) for chip_type in ChipType
            if self.first_chip_of_type(chip_type)
            ]

    def chips_for_type(self, chip_type):
        return [chip for chip in self.chips if chip.chip_type == chip_type]

    def chips_by_type(self):
        chips = OrderedDict()
        for chip_type in ChipType:
            c = self.chips_for_type(chip_type)
            if c:
                chips[chip_type] = c
        return chips

    def top_two_chips_by_type(self):
        return [chips[:2] for chip_type, chips in self.chips_by_type().items()
                if len(chips) >= 2
                and chip_type is not ChipType.yellow_gold]

    def pay_chip_of_type(self, chip_type):
        chip = self.first_chip_of_type(chip_type)
        if chip:
            chip.return_to_previous_position()
            return True
        return False

    def has_other_colours(self, colours):
        return any(
            c for c in self.chips
            if c.chip_type not in [b.chip_type for b in colours] +
            [ChipType.yellow_gold]
        )

    def _position_of_first_chip_of_type(self, chip_type):
        indices = [i for i, chip in enumerate(self.chips)
                   if chip.chip_type == chip_type]

        # No chip of this type found
        if not indices:
            return None

        return indices[0]

    def first_chip_of_type(self, chip_type):
        position = self._position_of_first_chip_of_type(chip_type)

        # No chip of this type found
        if position is None:
            return None

        return self.chips[position]

    def any_non_yellow_chips(self):
        return any(chip for chip in self.chips
                   if chip.chip_type is not ChipType.yellow_gold)

    @property
    def empty(self):
        return not self.chips

    def __len__(self):
        return len(self.chips)

    def any_chip_of_type(self, chip_type):
        return any(chip for chip in self.chips
                   if chip.chip_type == chip_type)

    @property
    def different_types(self):
        return len({chip.chip_type for chip in self.chips})

    def take_one(self, chip_type):
        """
        Remove a chip of the requested type off the stack
        Assumption: A chip of this type exists
        :param chip_type:
        :return:
        """

        # Find the first chip of this type
        position = self._position_of_first_chip_of_type(chip_type)

        if position is None:
            return None

        chip = self.chips[position]
        del(self.chips[position])

        return chip

    def take_chip(self, chip):
        index = self.chips.index(chip)
        del(self.chips[index])

    def add_one(self, chip):
        """
        Add the chip to the list of chips
        :param chip:
        :return:
        """
        self.chips.append(chip)

    def embody(self, location, scaling_factor=1.0,
               player_order=None, can_click=False,
               direction='vertical',
               show_empty=False):
        self.location = location

        chips_by_type = self.chips_by_type()
        for i, (chip_type, chip_stack) in enumerate(chips_by_type.items()):
            top_chip = chip_stack[0]
            if direction == 'vertical':
                stack_location = \
                    self.location + \
                    Vector(0, i * 2.5 * scaling_factor * config.chip_size)
            else:
                stack_location = \
                    self.location + \
                    Vector(i * 2.5 * scaling_factor * config.chip_size, 0)

            top_chip.embody(
                location=stack_location,
                scaling_factor=scaling_factor * config
                    .holding_area_chip_scaling,
                player_order=player_order,
                can_click=(can_click or top_chip in game.valid_actions)
            )

            text_colour = top_chip.chip_type

            draw_text(
                stack_location - Vector(3, 6),
                str(len(chip_stack)),
                text_colour=text_colour,
                reverse_colour=True,
                font_size=config.chip_font_size * scaling_factor,
                player_order=player_order
            )

class TileCollection():
    def __init__(self, tiles):
        self.tiles = tiles
        self.location = None

    def shuffle_and_limit(self, count):
        shuffle(self.tiles)
        self.tiles = self.tiles[:count]

    def contains(self, tile):
        return tile in self.tiles

    @property
    def points(self):
        return sum(t.points for t in self.tiles)

    def embody(self, location):
        self.location = location
        for i, tile in enumerate(self.tiles):
            tile.embody(
                self.location +
                Vector(i * (config.tile_size.x + config.tile_spacing), 0)
            )


# class Table(object):
#     """
#     Central playing area - shared space for all players
#     Contains all game components, apart from what's in the players' hands
#     """
#     def __init__(self, player_count):
#         component_collection_factory = ComponentCollectionFactory()
#
#         # 7 for 4 player, 5 for 3 player, 4 for 2 player plus 5 gold
#         chips = component_collection_factory(
#             'chip',
#             {
#                 4: '7 white, 7 blue, 7 red, 7 green, 7 black, 5 yellow',
#                 3: '5 white, 5 blue, 5 red, 5 green, 5 black, 5 yellow',
#                 2: '4 white, 4 blue, 4 red, 4 green, 4 black, 5 yellow',
#             }[player_count]
#         )
#
#         card_decks = [
#             component_collection_factory('card', raw_cards)
#             for raw_cards in (row_1, row_2, row_3)
#             ]
#
#         card_grid = []
#         for card_deck in card_decks:
#             card_grid.append([card_deck.pop() for _ in range(4)])
#
#         tiles = component_collection_factory(
#             'tile',
#             [
#                 '4 blue, 4 green',
#                 '4 white, 4 red',
#                 '4 black, 4 red',
#                 '4 green, 4 red',
#                 '4 black, 4 green',
#                 '4 white, 4 black',
#                 '4 blue, 4 white',
#                 '3 green, 3 blue, 3 red',
#                 '3 blue, 3 green, 3 white',
#                 '3 black, 3 red, 3 white',
#                 '3 black, 3 red, 3 green',
#                 '3 blue, 3 white, 3 red',
#                 '3 black, 3 red, 3 blue',
#                 '3 black, 3 white, 3 blue'
#             ]
#         )
#         tiles.shuffle_and_limit(player_count + 1)
#
#         self.chips = chips
#         self.card_decks = card_decks
#         self.card_grid = CardGrid(card_grid)
#         self.tiles = tiles
#
#     def embody(self):
#         self._draw()
#         self.chips.embody(
#             config.central_area_location +
#             config.chip_stack_location,
#             can_click=True,
#         )
#         for i, card_deck in enumerate(self.card_decks):
#             card_deck.embody(config.central_area_location +
#                              config.card_decks_location +
#                              Vector(0, i * (config.card_size.y +
#                                             config.card_spacing)))
#
#         for i, card_row in enumerate(self.card_grid.cards):
#             for j, card in enumerate(card_row):
#                 if card:
#                     card.embody(
#                         config.central_area_location +
#                         config.card_decks_location +
#                         Vector(
#                             (j + 1) *
#                             (config.card_size.x + config.card_spacing),
#                             i * (config.card_size.y + config.card_spacing))
#                     )
#
#         self.tiles.embody(
#             config.central_area_location +
#             config.tiles_row_location
#         )
#
#     def _draw(self):
#         # self._draw_tablecloth()
#         # self._draw_player_corners()
#         pass

class HoldingArea(object):
    """
    During a player's turn, holds the items which
    the player has selected, before they confirm this
    """
    def __init__(self):
        self.chips = ChipCollection()
        self.card = None
        self.location = None
        self.game = None

    def clear(self):
        self.__init__()

    def add_chip(self, chip):
        self.chips.add_one(chip)

    def embody(self):
        if not self.chips and not self.card:
            return
        self._draw()

        location = config.holding_area_location

        self.chips.embody(
            location=location + config.holding_area_chips_location,
            direction='horizontal',
            scaling_factor=0.7,
            can_click=True
        )

        if self.card:
            self.card.embody(
                location + config.holding_area_card_location,
                can_return=True
            )

        buttons.add(
            (
                location + config.cancel_button_location
             ).to_rectangle(config.button_size),
            Cancel(),
            text='Cancel'
        ).embody()

        # if game.is_turn_complete:
        # TODO: Import & use VALID
        if game.current_player.state == 'valid_turn':
            buttons.add(
                (
                    location + config.confirm_button_location
                ).to_rectangle(config.button_size),
                Confirm(),
                text='Confirm'
            ).embody()

    @staticmethod
    def _draw():
        draw_rectangle(
            config.holding_area_location.to_rectangle(
                config.holding_area_size
            ),
            ColourPalette.holding_area
        )

        draw_text(
            config.holding_area_location +
            config.holding_area_name_location,
            text=game.current_player.name
        )

    @property
    def is_empty(self):
        return not self.card and self.chips.empty

        #     *{
        #     'red': (ChipType.red_ruby, ),
        #     'blue': (ChipType.blue_sapphire, ),
        #     'white': (ChipType.white_diamond, ),
        #     'green': (ChipType.green_emerald, ),
        #     'black': (ChipType.black_onyx, ),
        #     'yellow': (ChipType.yellow_gold, )
        # }[details])

# class ComponentCollection(object):
#     pass



        # def _embody_table_chips(self):
        #     print("Hello")
        #     table_chip_counts.

        # def _embody_card_stack_counts(self):
        #     # Card stacks on the table
        #     card_stack_counts =
        #     card_stack_counts


        # self._embody_table_chips()
        # self._embody_card_stack_counts()
        # self._embody_card_grid()

        # Card grid on the table

        # Nobles tiles on the table
        # Players' chip counts
        # Players' card counts
        # Players' score
        # Players' reserved cards
        # Card in the reserved area
        # Chips in the reserved area
        # Nobles tiles in the reserved area

        print("Hello")





        # for row in range(3)
        #     for column in range(4):
        #         card = self.card_grid[row][column]
        #         if not card:
        #             continue
        #         card.embody(
        #             location=location + Vector(
        #                 1.1 * i * config.card_size.x, 0
        #             ),
        #         )
        #

    @property
    def position(self):
        """
        Where (holding area, current player's hand or supply)
        is this chip?
        """
        for (location, state) in [
            (game.holding_area.chips, ComponentState.holding_area),
            (game.current_player.chips, ComponentState.player),
            (game.table.chips, ComponentState.table)
        ]:
            if location.contains(self):
                return state


   def return_to_previous_position(self):
        if self.previous_position == ComponentState.table:
            game.holding_area.chips.take_chip(self)
            game.table.chips.add_one(self)
        self.previous_position = None

    def move_to_holding_area(self):
        self.remember_position()
        # self.previous_position = self.position
        game.table.chips.take_chip(self)
        game.holding_area.add_chip(self)

    def remember_position(self):
        self.previous_position = self.position




    def return_to_previous_position(self):
        if self.previous_position == ComponentState.card_grid:
            game.table.card_grid.return_card(self)
            game.holding_area.card = None
        self.previous_position = None