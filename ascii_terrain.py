import colorama

from wave_function_collapse.grid import Grid
from wave_function_collapse.tile import RuleDirection, RuleMatchingType, Tile

TILESET = [
    Tile(
        "Mountain",
        rules={
            RuleDirection.ALL: (
                {
                    "frequency": 1,
                    # "frequency": 499,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "mountain",
                },
                {
                    "frequency": 1,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "hill",
                },
            )
        },
        # symbol="M",
        tags=("mountain",),
    ),
    Tile(
        "Hill",
        color=colorama.Fore.GREEN,
        rules={
            RuleDirection.ALL: (
                {
                    "frequency": 1,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "mountain",
                },
                {
                    "frequency": 1,
                    # "frequency": 998,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "hill",
                },
                {
                    "frequency": 1,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "grassland",
                },
            )
        },
        # symbol="H",
        tags=("hill",),
    ),
    Tile(
        "Grassland",
        color=colorama.Fore.LIGHTGREEN_EX,
        rules={
            RuleDirection.ALL: (
                {
                    "frequency": 1,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "hill",
                },
                {
                    "frequency": 1,
                    # "frequency": 998,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "grassland",
                },
                {
                    "frequency": 1,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "sea",
                },
            )
        },
        # symbol="G",
        tags=("grassland",),
    ),
    Tile(
        "Sea",
        color=colorama.Fore.BLUE,
        rules={
            RuleDirection.ALL: (
                {
                    "frequency": 1,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "grassland",
                },
                {
                    "frequency": 1,
                    # "frequency": 499,
                    "matching_type": RuleMatchingType.TAGS,
                    "matching_value": "sea",
                },
            )
        },
        # symbol="S",
        tags=("sea",),
    ),
]

if __name__ == "__main__":
    grid = Grid(TILESET, size=(30, 15))
    grid.assign_all_tiles()
    print(grid)
