def index_in_list(a_list, index):
    return index < len(a_list)


def has_more_passengers(f1, f2, f3):
    sorted_floors = sorted(
        [f1, f2, f3], key=lambda f: len(f.passengers), reverse=True
    )
    print(*[len(f) for f in sorted_floors])
    return sorted_floors[0]
