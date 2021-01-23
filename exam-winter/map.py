"""
Sam Bridges task solution
"""
import typing as tp
import pathlib


def load_map(mapfile: tp.Union[pathlib.Path, str] = "default.map") -> tp.List[tp.List[str]]:
    map: tp.List[tp.List[str]] = [[]]
    path = pathlib.Path(mapfile)
    with open(path, "r") as f:
        map = [[j for j in i] for i in str(f.read()).split("\n")]

    return map

def find_path(map, sam = None):
    if not sam:
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == "☺":
                    sam = (i, j)
    
    possible_moves = [(sam[0]-1, sam[1]), (sam[0]+1, sam[1]), (sam[0], sam[1]-1), (sam[0], sam[1]+1)]

    for move in possible_moves:
        if map[move[0]][move[1]] == ".":
            map[move[0]][move[1]] = "☺"
            sam = move
            find_path(map, sam)
     
    return map

def reconstruct_map(map: tp.List[tp.List[str]]) -> str:
    list_map = []
    for i in map:
        list_map.append("".join(i) + "\n")
    return "".join(list_map)

if __name__ == "__main__":
    solution = find_path(load_map())
    print(reconstruct_map(solution))

