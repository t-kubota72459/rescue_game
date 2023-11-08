import os

def setup(fn):
    with open(fn, mode='w') as f:
        f.write("0\n")
    return 0

def oneup(fn):
    num = read(fn) + 1
    write(fn, num)
    return num

def read(fn):
    if os.path.isfile(fn):
        with open(fn) as f:
            ln = f.readline()
        return int(ln)
    else:
        return setup(fn)

def write(fn, num):
    if os.path.isfile(fn):
        with open(fn, "w") as f:
            f.write(f"{str(num)}" + "\n")

if __name__ == "__main__":
    print(oneup("./visitor_test.txt"))
