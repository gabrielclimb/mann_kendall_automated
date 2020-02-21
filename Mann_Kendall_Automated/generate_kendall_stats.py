import os

import glob

from .generate_excel import generate_xlsx


def main():

    file = glob.glob(os.getcwd() + "/input_tables" + "/*.xlsx")
    x = 0
    while x != "exit":
        count = 0
        for f in file:
            print(f"{count}: File {f}")
            count += 1

        x = input(f"Choose a file by number or type exit.\n")
        if x.isdigit():
            generate_xlsx(file[int(x)])
        else:
            x = "exit"


if __name__ == '__main__':
    main()
