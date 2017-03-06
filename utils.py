from chip_types import ChipType


def chip_type_for_colour_name(colour_name):
    return {
        'red': ChipType.red_ruby,
        'blue': ChipType.blue_sapphire,
        'white': ChipType.white_diamond,
        'green': ChipType.green_emerald,
        'black': ChipType.black_onyx,
        'yellow': ChipType.yellow_gold
    }[colour_name]

