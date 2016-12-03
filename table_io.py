import hashlib

def load_room(f):
    room = []
    for i in f:
        l = [c for c in i.rstrip()]
        if len(l) > 0:
            room.append(l)
    return room

def load_escape(f):
    e = []
    cnt = []
    for i in f:
        l = [c for c in i.rstrip()]
        if len(l) > 0:
            e.append(l)
    for (ypos, l) in enumerate(e):
        for (xpos, c) in enumerate(l):
            if c == 'c':
                cnt = [xpos, ypos]
    return (e, cnt)

def get_table_start_offset(table):
    for (ypos, l) in enumerate(table):
        for (xpos, c) in enumerate(l):
            if c == 'c':
                return [xpos, ypos]

# Remove comments and strip whitespaces from the right.
def parse(s):
    return s.partition("#")[0].rstrip()

def load_table():
    table = [c for i in open("tisch.txt") for c in parse(i) if len(parse(i)) > 0]
    table_start_offset = get_table_start_offset(table)
    return (table, table_start_offset)

# -----------------------------------------------------------------------------

def test_load_table():
    t, o = load_table()
    assert hashlib.md5("".join(["".join(i) for i in t])).hexdigest() == "3aae9e1e4b7f3804e168dcc03ff1c4c6"

if __name__ == "__main__":
    test_load_table()