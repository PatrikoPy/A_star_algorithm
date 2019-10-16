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
    show_grid(heuristic_grid[::-1])
    show_grid(grid[::-1])

    LO = {}  # adres,koszt G, heurystyka H, rodzic r,
    LZ = {}  # adres, rodzic
    gy, gx = start

    # LO[f'{gx}{gy}'] = {"G": 0, "H": float(heuristic_grid[gy][gx]), "F": float(heuristic_grid[gy][gx]), "r": None}
    # address = ""
    # f_min = None
    # while True:
    #     for fx in LO:
    #         if not f_min:
    #             f_min = LO[fx]["F"]
    #             address = fx
    #         elif LO[fx]["F"] < f_min:
    #             f_min = LO[fx]["F"]
    #             address = fx
    #     LZ[address] = LO.pop(address)
    #     if (gy, gx) == end:
    #         break

