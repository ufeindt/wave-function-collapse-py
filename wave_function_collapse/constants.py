from wave_function_collapse.tile import RuleDirection

ADJACENT_BORDERS = {
    RuleDirection.NORTH: RuleDirection.SOUTH,
    RuleDirection.EAST: RuleDirection.WEST,
    RuleDirection.SOUTH: RuleDirection.NORTH,
    RuleDirection.WEST: RuleDirection.EAST,
}
