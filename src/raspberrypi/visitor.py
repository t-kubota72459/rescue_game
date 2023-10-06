import os

FILENAME = "./visitor.txt"

def setup():
    with open(FILENAME, mode='w') as f:
        f.write("0\n")
    return 0

def oneup():
    num = read() + 1
    write(num)
    return num

def read():
    if os.path.isfile(FILENAME):
        with open(FILENAME) as f:
            ln = f.readline()
        return int(ln)
    else:
        return setup()

def write(num):
    if os.path.isfile(FILENAME):
        with open(FILENAME, "w") as f:
            f.write(f"{str(num)}" + "\n")

if __name__ == "__main__":
    print(oneup())
