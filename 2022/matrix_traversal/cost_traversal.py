nodes = {
    "A": 1,
    "B": 3,
    "C": 3,
    "D": 7,
    "E": 4,
    "F": 2,
    "G": 3
}


def get_permutations_under_cost_limit(cost_limit, nodes):
    def r(cost=0, path=[]):
        if cost > cost_limit:
            return
        if path:
            yield cost, path
        for node in nodes:
            if node in path:
                continue
            yield from r(cost + nodes[node], path + [node])

    return {k: v for k, v in r()}


if __name__ == '__main__':
    print(get_permutations_under_cost_limit(10, nodes))
