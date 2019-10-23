import math


def show_grid(my_grid):
    for row in my_grid:
        print(" ".join(row))


def grid_setup(load_grid):
    new_grid = []
    grid_size = [0, 0]
    with open(load_grid) as grid_file:
        for line in grid_file:
            new_grid.append(line.strip('\r\n').split(' '))
            grid_size[0] += 1
    grid_size[1] = len(new_grid[0])
    return new_grid[::-1], (grid_size[0], grid_size[1])


def grid_save(save_grid, save_file):
    with open(save_file, "w") as grid_file:
        for line in save_grid:
            grid_file.write(" ".join(line) + "\n")


def heuristic_setup(stop, source_grid):
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
    for i in new_track:
        grid[int(i.split("/")[0])][int(i.split("/")[1])] = "3"


def coordinates_input(max_coord):
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
    def new_cell(new_gy, new_gx, grid, h_grid):
        nonlocal LO, LZ, current_cost, move_cost, gy, gx
        try:
            if main_grid[int(new_gy)][int(new_gx)] != "5" and new_gy >= 0 and new_gx >= 0:
                next_cell = f"{int(new_gy)}/{int(new_gx)}"
                if (next_cell not in LZ and next_cell not in LO) or (
                        next_cell in LO and LO[next_cell]["F"] > (
                        current_cost + move_cost + float(h_grid[int(new_gy) + move_cost][int(new_gx)]))):
                    LO.update({next_cell: {"G": current_cost + move_cost, "H": h_grid[int(new_gy)][int(new_gx)],
                                           "F": current_cost + move_cost + float(h_grid[int(new_gy)][int(new_gx)]),
                                           "r": f"{gy}/{gx}"}})
        except IndexError:
            pass

    def grid_track(LZ, end_cell, track):
        if LZ[end_cell]["r"] == None:
            pass
        else:
            track.append(LZ[end_cell]["r"])
            grid_track(LZ, LZ[end_cell]["r"], track)

    LO = {}
    LZ = {}
    grid_cell = ""
    # start = (0, 0)
    # end = (19, 19)  # y,x
    gy, gx = start
    heuristic_grid = heuristic_setup(end, main_grid)
    LO[f'{gy}/{gx}'] = {"G": 0, "H": float(heuristic_grid[gy][gx]), "F": float(heuristic_grid[gy][gx]), "r": None}
    while True:
        new_min = []
        for grid_cell, values in LO.items():
            new_min.append((values["F"], grid_cell))
        try:
            new_min = min(new_min)
        except ValueError:
            print("Valid track doesn't exist.")
            break
        gy, gx = new_min[1].split("/")
        current_cost = LO[f'{gy}/{gx}']["G"]
        LZ[new_min[1]] = LO.pop(new_min[1])
        if (int(gy), int(gx)) == end:
            track = [f"{end[0]}/{end[1]}"]
            grid_track(LZ, f"{end[0]}/{end[1]}", track)
            grid_fill(main_grid, track)
            break
        new_cell(int(gy) + 1, int(gx), main_grid, heuristic_grid)
        new_cell(int(gy) - 1, int(gx), main_grid, heuristic_grid)
        new_cell(int(gy), int(gx) - 1, main_grid, heuristic_grid)
        new_cell(int(gy), int(gx) + 1, main_grid, heuristic_grid)
    return main_grid


def main():
    input_grid, size = grid_setup('grid.txt')
    input_start, input_end = coordinates_input(size)
    output_grid = a_star(input_grid, input_start, input_end, 1)
    grid_save(output_grid[::-1], "grid_output.txt")


def test():
    start = (0, 0)
    end = (19, 19)  # y,x
    input_grid, size = grid_setup('grid.txt')
    output_grid = a_star(input_grid, start, end, 1)
    grid_save(output_grid[::-1], "grid_output.txt")
    show_grid(output_grid[::-1])
    # TODO: dekorator show_grid()


if __name__ == '__main__':
    main()
