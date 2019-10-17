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


def algorithm():
    pass


if __name__ == '__main__':
    start = (2, 3)
    end = (19, 19)  # y,x

    grid = grid_setup('grid.txt')
    heuristic_grid = h_setup(end, grid)
    # show_grid(heuristic_grid[::-1])
    # show_grid(grid[::-1])

    LO = {}  # adres: koszt G, heurystyka H, rodzic r,
    LZ = {}  # adres: rodzic
    gy, gx = start

    LO[f'{gy}/{gx}'] = {"G": 0, "H": float(heuristic_grid[gy][gx]), "F": float(heuristic_grid[gy][gx]), "r": None}
    grid_cell = ""
    f_min = None
    while True:
        # znajdz min w LO
        new_min = [(112, "00/11"), (220, "0/0"), (40, "19/12")]
        for grid_cell, values in LO.items():
            new_min.append((values["H"], grid_cell))
        print(LO, LZ)
        print(min(new_min), new_min)
        # przenies do LZ
        LZ[min(new_min)[1]] = LO.pop(min(new_min)[1])
        print(LO, LZ)
        # spr. czy koniec
        if (gy, gx) == end:
            break
        # pobierz sąsiadów


        break
