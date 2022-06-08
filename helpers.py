def index_in_list(a_list, index):
    return index < len(a_list)


def has_more_passengers(f1, f2, f3):
    sorted_floors = sorted(
        [f1, f2, f3], key=lambda f: len(f.passengers), reverse=True
    )
    print(*[len(f) for f in sorted_floors])
    return sorted_floors[0]

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'