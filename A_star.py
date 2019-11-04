import math


def show_grid(my_grid):
    """
    Displays grid i console.

    :param my_grid: array to display
    :return: None
    """
    for row in my_grid:
        print(" ".join(row))


def grid_setup(load_grid):
    """
    Creates new array from given file.

    :param load_grid: name of file with array
    :type load_grid: str
    :return: array in reverse order and tuple with size of a grid (y, x)
    """
    new_grid = []
    grid_size = [0, 0]
    with open(load_grid) as grid_file:
        for line in grid_file:
            new_grid.append(line.strip('\r\n').split(' '))
            grid_size[0] += 1
    grid_size[1] = len(new_grid[0])
    return new_grid[::-1], (grid_size[0], grid_size[1])


def grid_save(save_grid, save_file):
    """
    Saves grid into a file.

    :param save_grid: variable with grid
    :param save_file: filename to save grid
    :return: None
    """
    with open(save_file, "w") as grid_file:
        for line in save_grid:
            grid_file.write(" ".join(line) + "\n")


def heuristic_setup(stop, source_grid):
    """
    Calculates heuristic for given array.

    :param stop: end point coordinates (y,x)
    :type stop: string or integer tuple
    :param source_grid: base for calculation
    :return: heuristic grid as array of floating point values
    """
    y, x = stop
    new_h_grid = []
    for i, n in enumerate(source_grid[:]):
        h_row = []
        for j, m in enumerate(n):
            if int(m) == 0:
                h_row.append(str(round(math.sqrt((j - x) ** 2 + (i - y) ** 2), 2)))
            else:
                h_row.append('-1')
        else:
            new_h_grid.append(h_row)
    else:
        return new_h_grid


def grid_fill(grid, new_track):
    """
    Marks track in given array as '3'

    :param grid: list with array to be marked
    :param new_track: list of coordinates, formatted as 'y/x'
    :return: None
    """
    for i in new_track:
        grid[int(i.split("/")[0])][int(i.split("/")[1])] = "3"


def coordinates_input(max_coord):
    """
    Function takes start/end coordinates from user input. If values are not correct loads default coordinates: start='0/0', end='max-1/max-1'.

    :param max_coord: size of array as a tuple of integers (y, x)
    :return: start, end coordinates as tuples of integers (y_start, x_start), (y_end, x_end)
    """
    while True:
        try:
            coordinates = input("start/end coordinates in format x_start/y_start x_end/y_end : \n")
            coordinates = [coordinates.split(" ")[0].split("/"), coordinates.split(" ")[1].split("/")]
            try:
                start_coord = tuple((int(coordinates[0][1]), int(coordinates[0][0])))
                end_coord = tuple((int(coordinates[1][1]), int(coordinates[1][0])))
                if start_coord[0] >= max_coord[0] or start_coord[1] >= max_coord[1] or end_coord[0] >= max_coord[0] or \
                        end_coord[1] >= max_coord[1]:
                    raise ValueError
            except ValueError:
                start_coord = (0, 0)
                end_coord = (max_coord[0] - 1, max_coord[1] - 1)
                print("ERROR, default coordinates loaded. ")
            break
        except IndexError:
            print("ERROR, try again...")

    return start_coord, end_coord


def a_star(main_grid, start=(0, 0), end=(19, 19), move_cost=1):
    """
    A star algorithm implementation.

    :param main_grid: array to probe
    :param start: starting point coordinates tuple formatted as (y,x), by default (0,0)
    :param end: ending point coordinates tuple formatted as (y,x), by default (19,19)
    :param move_cost: move cost between adjacent cells in a grid as integer value, by default 1
    :return: grid array
    """

    def new_cell(new_gy, new_gx, grid, h_grid):
        nonlocal potential_cells, visited_cells, current_cost, move_cost, gy, gx
        try:
            if grid[int(new_gy)][int(new_gx)] != "5" and new_gy >= 0 and new_gx >= 0:
                next_cell = f"{int(new_gy)}/{int(new_gx)}"
                if (next_cell not in visited_cells and next_cell not in potential_cells) or (
                        next_cell in potential_cells and potential_cells[next_cell]["summary_cost"] > (
                        current_cost + move_cost + float(h_grid[int(new_gy) + move_cost][int(new_gx)]))):
                    potential_cells.update({next_cell: {"track_cost": current_cost + move_cost,
                                                        "heuristic_cost": h_grid[int(new_gy)][int(new_gx)],
                                                        "summary_cost": current_cost + move_cost + float(
                                                            h_grid[int(new_gy)][int(new_gx)]),
                                                        "parent_cell": f"{gy}/{gx}"}})
        except IndexError:
            pass

    def grid_track(end_cell):
        nonlocal visited_cells, track
        if not visited_cells[end_cell]["parent_cell"]:
            pass
        else:
            track.append(visited_cells[end_cell]["parent_cell"])
            grid_track(visited_cells[end_cell]["parent_cell"])

    # algorithm setup for starting point
    potential_cells = {}
    visited_cells = {}
    gy, gx = start
    heuristic_grid = heuristic_setup(end, main_grid)
    potential_cells[f'{gy}/{gx}'] = {"track_cost": 0, "heuristic_cost": float(heuristic_grid[gy][gx]),
                                     "summary_cost": float(heuristic_grid[gy][gx]), "parent_cell": None}

    # loop checks cells until it reaches end point or potential_cells is empty
    while True:
        # searching address of a cell with lowest summary cost
        new_min = []
        for grid_cell, values in potential_cells.items():
            new_min.append((values["summary_cost"], grid_cell))
        try:
            new_min = min(new_min)
        except ValueError:
            print("Valid track doesn't exist.")
            break
        # setting up new coordinates
        gy, gx = new_min[1].split("/")
        # calculating cost from start to new coordinates
        current_cost = potential_cells[f'{gy}/{gx}']["track_cost"]
        visited_cells[new_min[1]] = potential_cells.pop(new_min[1])
        # checking end point condition
        if (int(gy), int(gx)) == end:
            # retracing track from end to start
            track = [f"{end[0]}/{end[1]}"]
            grid_track(f"{end[0]}/{end[1]}")
            grid_fill(main_grid, track)
            break
        # probing for new potential_cells in order: up, down, left, right
        for i, j in ((1, 0), (-1, 0), (0, -1), (0, 1)):
            new_cell(int(gy) + i, int(gx) + j, main_grid, heuristic_grid)
    return main_grid


def main():
    input_grid, size = grid_setup('grid.txt')
    input_start, input_end = coordinates_input(size)
    output_grid = a_star(input_grid, input_start, input_end, 1)
    grid_save(output_grid[::-1], "grid_output.txt")


def test():
    """Test without user input and fixed start(0/0) and end(19/19)"""
    start = (0, 0)
    end = (19, 19)  # y,x
    input_grid, size = grid_setup('grid.txt')
    output_grid = a_star(input_grid, start, end, 1)
    grid_save(output_grid[::-1], "grid_output.txt")
    show_grid(output_grid[::-1])
    # TODO: dekorator show_grid()


if __name__ == '__main__':
    main()
