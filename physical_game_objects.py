from drawing_surface import draw_rectangle, draw_pologon, draw_text, \
    draw_circle
from drawing_surface import ColourPalette, easel
from settings import config


class AbstractDrawAction(object):
    pass


class DrawCardCost(AbstractDrawAction):
    def draw(self, x, y):
        # TODO Tidy layout
        for (i, (jewel_type, number)) in \
                enumerate([(jewel_type, number)
                           for (jewel_type, number)
                           in self.cost.items() if number]):
            location = (x, y + (i * (config.chip_size + config.chip_spacing)))
            draw_circle(location, config.chip_size, jewel_type.value)

            location = (x + config.chip_size, y + ((i - 0.3) * (config.chip_size + config.chip_spacing)))
            # TODO Choose a contrasting colour for the number
            draw_text(location, str(number), font_size=18)


class DrawCard(AbstractDrawAction):
    def draw(self, x, y):
        draw_rectangle((x, y, config.card_width, config.card_height),
                       ColourPalette.card_background)
        if self.points:
            draw_text((x + config.points_location_x, y + config.points_location_y),
                      str(self.points))

        self.cost.draw(x + config.cost_location_x, y + config.cost_location_y)

        # TODO Better variable name - top row?, top row left, top row right?
        draw_circle((x + config.card_width - config.points_location_x,
                     int(y + config.points_location_y + config.chip_size * 0.5)),
                    int(config.chip_size * 1.5), self.jewel_type.value)


# class DrawCardDeck(AbstractDrawAction):
#     pass


class DrawCardRow(AbstractDrawAction):
    def draw(self, x, y):
        for column, card in enumerate(self.columns):
            card.draw(x + column * config.column_width, y)


class DrawCentralTableArea(AbstractDrawAction):
    def draw(self, x, y):
        for (i, card_row) in enumerate(self.card_rows):
            card_row.draw(x, y + i * config.tabletop_height)


class DrawTable(object):
    def _draw_tablecloth(self):
        draw_rectangle((0, 0, config.tabletop_width, config.tabletop_height),
                       ColourPalette.table_cloth)

    def _draw_player_corners(self):
        for (x, y) in [
            (0, 0),
            (0, config.tabletop_height),
            (config.tabletop_width, config.tabletop_height),
            (config.tabletop_width, 0)
        ]:
            draw_pologon([
                (x, abs(y - config.tabletop_height / 2.2)),
                (abs(x - config.tabletop_width / 2.2), y),
                (x, y)],
                ColourPalette.corners
            )

    def draw(self):
        self._draw_tablecloth()
        self._draw_player_corners()
        self.central_table_area.draw(380, 150)
        # self._draw_cards()
