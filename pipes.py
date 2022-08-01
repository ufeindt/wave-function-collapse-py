from wave_function_collapse.grid import Grid
from wave_function_collapse.tile import RuleDirection, RuleMatchingType, Tile

TILEDATA = [
    ["B", " "],
    ["EW", "─"],
    ["NS", "│"],
    ["ES", "┌"],
    ["SW", "┐"],
    ["NE", "└"],
    ["NW", "┘"],
    ["NES", "├"],
    ["NSW", "┤"],
    ["ESW", "┬"],
    ["NEW", "┴"],
    ["NESW", "┼"],
]

directions = {
    "N": RuleDirection.NORTH,
    "E": RuleDirection.EAST,
    "S": RuleDirection.SOUTH,
    "W": RuleDirection.WEST,
}


tags = {
    "N": {True: "north", False: "no-north"},
    "E": {True: "east", False: "no-east"},
    "S": {True: "south", False: "no-south"},
    "W": {True: "west", False: "no-west"},
}

opposites = {
    "N": "S",
    "E": "W",
    "S": "N",
    "W": "E",
}

TILESET = []
for name, symbol in TILEDATA:
    tile_tags = []
    rules = {}
    for char, direction in directions.items():
        present = char in name
        tile_tags.append(tags[char][present])
        rules[direction] = (
            {
                "frequency": 1,
                "matching_type": RuleMatchingType.TAGS,
                "matching_value": tags[opposites[char]][present],
            },
        )

    TILESET.append(
        Tile(name=name, symbol=symbol, tags=tuple(tile_tags), rules=rules)
    )

if __name__ == "__main__":
    grid = Grid(TILESET, size=(60, 30))
    grid.assign_all_tiles()
    print(grid)
