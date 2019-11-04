#! /usr/bin/env python3
import A_star


def easy_grid():
    """Converts grid to more readable: # - obstacle, O - track."""
    with open("easy_track.txt", "w") as save_grid_file:
        new_easy_grid = []
        with open("grid_output.txt") as grid_file:
            for line in grid_file:
                row = line.strip("\n").split(" ")
                for n, i in enumerate(row):
                    if i == "0":
                        row[n] = " "
                    elif i == "5":
                        row[n] = "#"
                    elif i == "3":
                        row[n] = "O"
                else:
                    new_easy_grid.append(row)
        for line in new_easy_grid:
            save_grid_file.write(" ".join(line) + "\n")


if __name__ == "__main__":
    # A_star.main()
    easy_grid()
