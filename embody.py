from settings import config
from vector import Vector
from util_classes import ChipType, PlayerStates, ComponentStates

from graphics import draw_rectangle, draw_text, \
    draw_circle, draw_card
from graphics import ColourPalette, circle_location_to_rectangle, \
    grow_rectangle, translate_to_player

from game_actions import Cancel, Confirm
from game import game
from game_actions import ToDo


class AbstractEmbodyMixin:
    pass


class EmbodyChipStackMixin(AbstractEmbodyMixin):
    def embody(self):
        location = config.central_area_location + config.chip_stack_location
        for i, chip_type in enumerate(
                [c for c in ChipType if c in self.colour_count]
        ):
            chip_location = location + Vector(0, i * 2.5 * config.chip_size)

            chip = game.components.chip_from_supply(chip_type)

            # TODO: Tidy up passing in current player here?
            if game.mechanics.is_valid_action(chip):
                game.buttons.add(
                    circle_location_to_rectangle(chip_location,
                                                 config.chip_size),
                    ToDo([chip.to_holding_area])
                ).embody()

            draw_circle(chip_location, config.chip_size, chip_type)
            draw_text(
                location=chip_location - Vector(4, 6),
                text=str(self.colour_count[chip_type]),
                text_colour=chip_type,
                reverse_colour=True
            )


class EmbodyChipCostMixin(AbstractEmbodyMixin):
    def embody(self, location):
        for i, chip_type in enumerate(
                [c for c in ChipType if c in self.colour_count]
        ):
            chip_location = location + Vector(
                0,
                i * 2.5 * config.chip_size * config.chip_cost_scaling
            )
            draw_circle(
                chip_location,
                config.chip_size * config.chip_cost_scaling,
                chip_type
            )
            draw_text(
                location=chip_location - Vector(4, 6),
                text=str(self.colour_count[chip_type]),
                text_colour=chip_type,
                reverse_colour=True
            )


class EmbodyTileMixin(AbstractEmbodyMixin):
    def embody(self):
        """
        Show this component, plus any sub components,
        at the specified location and scaling factor
        If it can be clicked on, also add a button
        """
        self.buttonify()
        self.draw()

    @property
    def location(self):
        if self.state == ComponentStates.in_supply:
            return config.central_area_location + \
                   config.tiles_row_location +\
                   Vector(self.column *
                          (config.tile_size.x + config.tile_spacing), 0)

        if self.state == ComponentStates.in_holding_area:
            return config.holding_area_location + \
                   config.holding_area_tile_location

    def draw(self):
        draw_rectangle(
            self.location.to_rectangle(config.tile_size),
            ColourPalette.card_background
        )
        draw_text(self.location + config.points_location,
                  str(self.points)
                  )
        self.chip_cost.embody(self.location + config.cost_location)

    def buttonify(self):
        if game.mechanics.is_valid_action(self):
            game.buttons.add(
                self.location.to_rectangle(config.tile_size),
                ToDo([self.to_holding_area])
                if self.state == ComponentStates.in_supply
                else ToDo([self.to_supply])
            ).embody()


class EmbodyChipMixin(AbstractEmbodyMixin):
    def __init__(self):
        self.column = None

    @property
    def location(self):
        # Individual chips are only show in the holding area - if not, raise an error
        assert self.state == ComponentStates.in_holding_area

        return config.holding_area_location + \
               config.holding_area_chips_location + \
               Vector(self.column * config.chip_size * 2.5, 0)

    def embody(self, column):
        self.column = column
        self.buttonify()
        self._draw()

    def buttonify(self):
        """
        If this chip can be moved, turn it into a button
        """
        # Only embodied (as a single chip) if it is in the holding area
        # so always make it a button - unless there is also a card in the holding area
        if game.components.holding_area_cards.is_empty:
            game.buttons.add(
                circle_location_to_rectangle(self.location, config.chip_size),
                ToDo([self.to_supply if game.current_player.state == PlayerStates.turn_started
                      else self.to_player_area])
            ).embody()

    def _draw(self):
        """
        Draw the chip
        """
        draw_circle(
            self.location,
            int(config.chip_size),
            self.chip_type
        )


class EmbodyCardMixin(AbstractEmbodyMixin):
    def embody(self):
        """
        Show this component, plus any sub components,
        at the specified location and scaling factor
        If it can be clicked on, also add a button
        """
        self.buttonify()
        self.draw()

    @property
    def location(self):
        if self.face_up and self.state == ComponentStates.in_supply:
            return \
                config.card_decks_location + \
                config.central_area_location + \
                Vector(
                    (self.column + 1) *
                    (config.card_size.x + config.card_spacing),
                    self.row * (config.card_size.y + config.card_spacing)
                )

        elif self.state == ComponentStates.in_holding_area:
            return config.holding_area_location + \
                   config.holding_area_card_location

        elif self.state == ComponentStates.in_reserved_area:
            return translate_to_player(
                self.player.player_order,
                config.player_reserved_location +
                Vector(self.column * (config.card_size.x + config.card_spacing), 0))

    def buttonify(self):
        """
        Turn the card into a 'button' so the user can click on it
        """
        valid_actions = game.mechanics.valid_actions

        # If currently in supply - move it to the holding area
        if self.state in [ComponentStates.in_supply,
                          ComponentStates.in_reserved_area] \
                and self in valid_actions:
            game.buttons.add(
                self.location.to_rectangle(config.card_size),
                ToDo(
                    [self.to_holding_area]
                )
            ).embody()
        elif self.state == ComponentStates.in_holding_area:
            game.buttons.add(
                self.location.to_rectangle(config.card_size),
                ToDo([self.move_back])
            ).embody()

    def draw(self):
        """
        Draw the rectangle and the value (points)
        The cost (chips) and resulting chip types
        will draw themselves
        """
        draw_card(self.location)
        if self.points:
            draw_text(
                self.location + config.points_location,
                str(self.points)
            )

        draw_circle(self.location + config.reward_chip_location,
                    config.chip_size * config.reward_chip_scaling,
                    self.chip_type)

        self.chip_cost.embody(self.location + config.cost_location)


class EmbodyCardGridMixin(AbstractEmbodyMixin):
    def embody(self):
        for row in self.card_grid:
            for card in row:
                if card:
                    card.embody()


class EmbodyCardDeckCountMixin(AbstractEmbodyMixin):
    def embody(self, location):
        for row in range(3):
            if self.card_deck_count[row]:
                deck_location = location + Vector(
                    0,
                    row * (config.card_size.y + config.card_spacing)
                )

                draw_rectangle(deck_location.to_rectangle(config.card_size),
                               ColourPalette.card_deck_background)
                draw_text(
                    deck_location + config.points_location,
                    str(self.card_deck_count[row])
                )


class EmbodyPlayerMixin(AbstractEmbodyMixin):
    def embody(self):
        self._draw()
        game.components.chip_count_for_player(self).embody(self)
        game.components.card_reward_for_player(self).embody(self)
        for i, card in enumerate(game.components.reserved_cards_for_player(self)):
            card.column = i
            card.embody()

    def _draw(self):
        draw_rectangle(
            (0, 0, config.player_area_size.x, config.player_area_size.y),
            player_order=self.player_order,
            colour=ColourPalette.active_player_area
            if self.state != PlayerStates.player_waiting
            else ColourPalette.player_area
        )
        draw_text(
            (config.player_name_location.x, config.player_name_location.y),
            self.name,
            player_order=self.player_order
        )
        # points = game.mechanics.points_for_player(self)
        if self.points:
            draw_text(
                list(config.player_points_location),
                str(self.points),
                player_order=self.player_order
            )

        if game.finished and self in game.mechanics.winners:
            draw_text(
                list(config.player_winner_message_location),
                font_size=config.player_winner_font_size,
                text='Winner',
                player_order = self.player_order
            )


class EmbodyPlayerChipStack(AbstractEmbodyMixin):
    # TODO: Lots of overlap with other chip count/stack embody methods
    # TODO: Split out into embody() and draw()?
    def embody(self, player):
        for i, chip_type in enumerate(
                [c for c in ChipType if c in self.colour_count]
        ):
            if self.colour_count[chip_type]:
                chip_location = config.player_chip_stack_location \
                                + Vector(i * 2.5 *
                                         config.player_chip_stack_scaling *
                                         config.chip_size, 0)

                if player.state == PlayerStates.too_many_chips and player.too_many_chips_in_hand:
                    chips = game.components.chips_for_player(player).filter(chip_type=chip_type).components
                    if chips:
                        chip_size = config.chip_size * config.player_chip_stack_scaling
                        # TODO: Tidy this up?
                        game.buttons.add(
                            (chip_location - Vector(chip_size, chip_size)).to_rectangle(Vector(chip_size * 2, chip_size * 2)),
                            ToDo([chips[0].to_holding_area]),
                            player_order=player.player_order
                        ).embody()

                draw_circle(
                    chip_location,
                    config.chip_size * config.player_chip_stack_scaling,
                    chip_type,
                    player_order=player.player_order,
                )

                draw_text(
                    location=chip_location - Vector(4, 6),
                    text=str(self.colour_count[chip_type]),
                    text_colour=chip_type,
                    reverse_colour=True,
                    player_order=player.player_order,

                )


class EmbodyPlayerCardStack(AbstractEmbodyMixin):
    # TODO: Lots of overlap with other chip count/stack embody methods
    def embody(self, player):
        for i, chip_type in enumerate(
                [c for c in ChipType if c in self.colour_count]
        ):
            if self.colour_count[chip_type]:
                location = config.player_chip_stack_location \
                                + Vector((i - 0.4) * 2.5 *
                                         config.player_chip_stack_scaling *
                                         config.chip_size,
                                         1.5 *
                                         config.player_chip_stack_scaling *
                                         config.chip_size
                                         )

                draw_rectangle(
                    location.to_rectangle(
                        Vector(2 * config.chip_size *
                               config.player_chip_stack_scaling,
                               config.chip_size *
                               config.player_chip_stack_scaling * 2)
                    ),
                    chip_type,
                    player_order=player.player_order,
                )
                draw_text(
                    location=location + Vector(6, 3),
                    text=str(self.colour_count[chip_type]),
                    text_colour=chip_type,
                    reverse_colour=True,
                    player_order=player.player_order,

                )


class EmbodyButtonMixin:
    def embody(self):
        self._draw()

    def _draw(self):
        draw_rectangle(
            grow_rectangle(self.rectangle, 2),
            ColourPalette.button,
        )


class EmbodyHoldingAreaMixin(AbstractEmbodyMixin):
    def embody(self):
        if self.is_empty and game.current_player.state is not PlayerStates.too_many_chips:
            return

        self._draw_holding_area()

        for i, chip in enumerate(self.holding_area_chips):
            chip.embody(column=i)

        for tile in game.components.holding_area_tiles:
            tile.embody()

        if not self.is_empty:
            game.buttons.add(
                (
                    config.holding_area_location + config.cancel_button_location
                ).to_rectangle(config.button_size),
                Cancel(),
                text='Cancel'
            ).embody()

        if (game.current_player.state == PlayerStates.turn_started
            and game.mechanics.turn_complete()) \
                or (game.current_player.state == PlayerStates.tiles_offered
                    and game.components.holding_area_tiles) \
                or (game.current_player.state == PlayerStates.too_many_chips
                    and not game.current_player.too_many_chips_in_hand):
            game.buttons.add(
                (
                    config.holding_area_location +
                    config.confirm_button_location
                ).to_rectangle(config.button_size),
                Confirm(),
                text='Confirm'
            ).embody()

        if game.current_player.state == PlayerStates.too_many_chips:
            draw_text(
                config.holding_area_location +
                config.holding_area_too_many_chips_location,
                text="Too many chips - return some"
            )

    @staticmethod
    def _draw_holding_area():
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
