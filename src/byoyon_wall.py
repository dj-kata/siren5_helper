"""ボヨヨン壁の反射候補計算。"""

from dataclasses import dataclass


GRID_SIZE = 25
MAX_UNREFLECTED_STEPS = 10
MAX_REFLECTIONS = 24

NONE = "none"
BYYN = "byyn"
OUT_OF_RANGE = "out-of-range"

DIRECTIONS = {
    "左上": (-1, -1),
    "右上": (-1, 1),
    "左下": (1, -1),
    "右下": (1, 1),
}

SIDE_LABELS = {
    "top": "上",
    "bottom": "下",
    "left": "左",
    "right": "右",
}


@dataclass(frozen=True)
class ByoyonStep:
    row: int | None
    column: int | None
    direction: tuple[int, int]
    reflection_side: str = ""


@dataclass(frozen=True)
class ByoyonCandidate:
    row: int
    column: int
    direction: str
    reflections: tuple[str, ...]
    path: tuple[ByoyonStep, ...]
    split_path: tuple[ByoyonStep, ...]

    @property
    def display_text(self) -> str:
        route = " -> ".join(SIDE_LABELS[side] for side in self.reflections)
        return f"{self.row + 1}行{self.column + 1}列から{self.direction}に投げる ({route})"


def find_byoyon_candidates(walls, grid_size=GRID_SIZE):
    """上下左右のボヨヨン壁に当たって分裂できる投げ方を列挙する。"""
    normalized_walls = {(int(row), int(column)) for row, column in walls}
    path_list = []
    for row in range(grid_size):
        for column in range(grid_size):
            if (row, column) in normalized_walls:
                continue
            for direction_name, vector in DIRECTIONS.items():
                candidate = simulate_byoyon_route(
                    row, column, direction_name, vector, normalized_walls, grid_size
                )
                if candidate is not None:
                    path_list.append(candidate)
    return _reduce_candidates(path_list)


def simulate_byoyon_route(row, column, direction_name, vector, walls, grid_size):
    if _type_from(row, column, walls, grid_size) != NONE:
        return None

    hit_sides = {"top": False, "bottom": False, "left": False, "right": False}
    reflections = []
    path = [ByoyonStep(row, column, vector)]
    current_row = row
    current_column = column
    direction = vector
    reflection_count = 0
    unreflected_count = 0
    first_reflection_immediate = None
    split_reflections = None
    split_path = None

    while True:
        dr, dc = direction
        current_row += dr
        current_column += dc
        cell_type = _type_from(current_row, current_column, walls, grid_size)

        if cell_type == OUT_OF_RANGE:
            path.append(ByoyonStep(None, None, direction))
            return _candidate_if_valid(
                row,
                column,
                direction_name,
                reflections,
                path,
                hit_sides,
                first_reflection_immediate,
                split_reflections,
                split_path,
            )

        if cell_type == NONE:
            path.append(ByoyonStep(current_row, current_column, direction))
            unreflected_count += 1
            if unreflected_count >= MAX_UNREFLECTED_STEPS:
                return _candidate_if_valid(
                    row,
                    column,
                    direction_name,
                    reflections,
                    path,
                    hit_sides,
                    first_reflection_immediate,
                    split_reflections,
                    split_path,
                )
        elif cell_type == BYYN:
            if first_reflection_immediate is None:
                first_reflection_immediate = len(path) == 1
            if reflection_count >= MAX_REFLECTIONS:
                return _candidate_if_valid(
                    row,
                    column,
                    direction_name,
                    reflections,
                    path,
                    hit_sides,
                    first_reflection_immediate,
                    split_reflections,
                    split_path,
                )

            h_adj_type = _type_from(current_row, current_column - dc, walls, grid_size)
            v_adj_type = _type_from(current_row - dr, current_column, walls, grid_size)
            if h_adj_type == BYYN and v_adj_type == NONE:
                side = "top" if dr > 0 else "bottom"
                hit_sides[side] = True
                reflections.append(side)
                direction = (-dr, dc)
                current_row += direction[0]
                path.append(
                    ByoyonStep(current_row, current_column, direction, side)
                )
            elif h_adj_type == NONE and v_adj_type == BYYN:
                side = "right" if dc > 0 else "left"
                hit_sides[side] = True
                reflections.append(side)
                direction = (dr, -dc)
                current_column += direction[1]
                path.append(
                    ByoyonStep(current_row, current_column, direction, side)
                )
            elif h_adj_type == NONE and v_adj_type == NONE:
                direction = (-dr, -dc)
                current_row += direction[0]
                current_column += direction[1]
            else:
                return _candidate_if_valid(
                    row,
                    column,
                    direction_name,
                    reflections,
                    path,
                    hit_sides,
                    first_reflection_immediate,
                    split_reflections,
                    split_path,
                )

            reflection_count += 1
            unreflected_count = 1
            if split_reflections is None and _can_split(hit_sides):
                split_reflections = tuple(reflections)
                split_path = tuple(path)
        else:
            return None

        if current_row == row and current_column == column:
            return _candidate_if_valid(
                row,
                column,
                direction_name,
                reflections,
                path,
                hit_sides,
                first_reflection_immediate,
                split_reflections,
                split_path,
            )


def _candidate_if_valid(
    row,
    column,
    direction_name,
    reflections,
    path,
    hit_sides,
    first_reflection_immediate,
    split_reflections=None,
    split_path=None,
):
    if not first_reflection_immediate or not _can_split(hit_sides):
        return None
    if split_reflections is None:
        split_reflections = tuple(reflections)
    if split_path is None:
        split_path = tuple(path)
    return ByoyonCandidate(
        row,
        column,
        direction_name,
        tuple(split_reflections),
        tuple(path),
        tuple(split_path),
    )


def _reduce_candidates(candidates):
    loop_catch = []
    corner_return = []
    uncatchable = []
    for candidate in candidates:
        start = candidate.path[0]
        end = candidate.path[-1]
        if _same_position(start, end):
            if start.direction == end.direction:
                loop_catch.append(candidate)
            else:
                corner_return.append(candidate)
        else:
            uncatchable.append(candidate)

    reduced = []
    reduced.extend(_reduce_loop_catch(loop_catch))
    reduced.extend(_reduce_corner_return(corner_return))
    reduced.extend(_reduce_uncatchable(uncatchable))
    return reduced


def _reduce_loop_catch(candidates):
    remaining = list(candidates)
    reduced = []
    while remaining:
        candidate = remaining.pop(0)
        reduced.append(candidate)
        start = candidate.path[0]
        remaining = [
            other
            for other in remaining
            if not _path_has_position_and_direction(other.path, start)
        ]
    return reduced


def _reduce_corner_return(candidates):
    remaining = sorted(candidates, key=lambda candidate: len(candidate.path))
    reduced = []
    while remaining:
        candidate = remaining.pop(0)
        reduced.append(candidate)
        middle = candidate.path[(len(candidate.path) - 1) // 2]
        remaining = [
            other
            for other in remaining
            if not _same_step(middle, other.path[(len(other.path) - 1) // 2])
        ]
    return reduced


def _reduce_uncatchable(candidates):
    remaining = sorted(candidates, key=_uncatchable_sort_key)
    reduced = []
    while remaining:
        candidate = remaining.pop(0)
        reduced.append(candidate)
        end = _last_real_step(candidate.path)
        remaining = [
            other
            for other in remaining
            if not _same_step(end, _last_real_step(other.path))
        ]
    return reduced


def _path_has_position_and_direction(path, target):
    reverse_direction = (-target.direction[0], -target.direction[1])
    return any(
        _same_position(step, target)
        and step.direction in (target.direction, reverse_direction)
        for step in path
    )


def _last_real_step(path):
    return path[-2] if path[-1].row is None else path[-1]


def _uncatchable_sort_key(candidate):
    end = candidate.path[-1]
    return (end.row is None, len(candidate.path))


def _same_step(left, right):
    return _same_position(left, right) and left.direction == right.direction


def _same_position(left, right):
    return left.row is not None and left.row == right.row and left.column == right.column


def _can_split(hit_sides):
    return all(hit_sides.values())


def _type_from(row, column, walls, grid_size):
    if 0 <= row < grid_size and 0 <= column < grid_size:
        return BYYN if (row, column) in walls else NONE
    return OUT_OF_RANGE
