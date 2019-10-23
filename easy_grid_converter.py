import planowanie_trasy


def easy_grid():
    with open("easy_track.txt", "w") as save_grid_file:
        new_easy_grid = []
        with open("grid_output.txt") as grid_file:
            for line in grid_file:
                row = line.strip("\n").split(" ")
                for n, i in enumerate(row):
                    if i == "0":
                        row[n] = "-"
                    elif i == "5":
                        row[n] = "X"
                    elif i == "3":
                        row[n] = "+"
                    # print(row)
                else:
                    new_easy_grid.append(row)
        # print(easy_grid)
        for line in new_easy_grid:
            save_grid_file.write(" ".join(line) + "\n")


if __name__ == "__main__":
    planowanie_trasy.main()
    easy_grid()
