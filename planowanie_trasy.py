import math


def show_grid(my_grid):
    for row in my_grid:
        print(" ".join(row))


def grid_setup(load_grid):
    new_grid = []
    with open(load_grid) as grid_file:
        for line in grid_file:
            new_grid.append(line.strip('\r\n').split(' '))
    return new_grid[::-1]


def grid_save(save_grid, save_file):
    with open(save_file, "w") as grid_file:
        for line in save_grid:
            grid_file.write(" ".join(line) + "\n")


def h_setup(stop, grid):
    y, x = stop
    h_grid = []
    for i, n in enumerate(grid[:]):
        h_row = []
        for j, m in enumerate(n):
            if int(m) == 0:
                h_row.append(str(round(math.sqrt((j - x) ** 2 + (i - y) ** 2), 2)))
            else:
                h_row.append('-1')
        else:
            h_grid.append(h_row)
    else:
        return h_grid


def grid_track(end_cell):
    if LZ[end_cell]["r"] == None:
        pass
    else:
        track.append(LZ[end_cell]["r"])
        grid_track(LZ[end_cell]["r"])


def grid_fill():
    for i in track:
        grid[int(i.split("/")[0])][int(i.split("/")[1])] = "3"


def new_cell(new_gy, new_gx):
    try:
        if grid[int(new_gy)][int(new_gx)] != "5" and new_gy >= 0 and new_gx >= 0:
            next_cell = f"{int(new_gy)}/{int(new_gx)}"
            if (next_cell not in LZ and next_cell not in LO) or (
                    next_cell in LO and LO[next_cell]["F"] > (
                    g + 1 + float(heuristic_grid[int(new_gy) + 1][int(new_gx)]))):
                LO.update({next_cell: {"G": g + 1, "H": heuristic_grid[int(new_gy)][int(new_gx)],
                                       "F": g + 1 + float(heuristic_grid[int(new_gy)][int(new_gx)]),
                                       "r": f"{gy}/{gx}"}})
    except IndexError:
        pass


def coordinates_input():
    coordinates = input("start/end coordinates in format x_start/y_start x_end/y_end : ")
    coordinates = [coordinates.split(" ")[0].split("/"), coordinates.split(" ")[1].split("/")]
    start_coord = tuple((int(coordinates[0][1]), int(coordinates[0][0])))
    end_coord = tuple((int(coordinates[1][1]), int(coordinates[1][0])))
    return start_coord, end_coord


if __name__ == '__main__':
    # start = (0, 0)
    # end = (19, 19)  # y,x
    start, end = coordinates_input()
    track = [f"{end[0]}/{end[1]}"]
    grid = grid_setup('grid.txt')
    heuristic_grid = h_setup(end, grid)
    LO = {}
    LZ = {}
    gy, gx = start
    LO[f'{gy}/{gx}'] = {"G": 0, "H": float(heuristic_grid[gy][gx]), "F": float(heuristic_grid[gy][gx]), "r": None}
    grid_cell = ""

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
        g = LO[f'{gy}/{gx}']["G"]
        LZ[new_min[1]] = LO.pop(new_min[1])
        if (int(gy), int(gx)) == end:
            grid_track(f"{end[0]}/{end[1]}")
            grid_fill()
            grid_save(grid[::-1], "grid_output.txt")
            show_grid(grid[::-1])
            break
        new_cell(int(gy) + 1, int(gx))
        new_cell(int(gy) - 1, int(gx))
        new_cell(int(gy), int(gx) - 1)
        new_cell(int(gy), int(gx) + 1)
