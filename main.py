import itertools
from random import randint
from typing import List

import emoji

from helpers import index_in_list, bcolors


class Building:
    def __init__(self, counter) -> None:
        self.counter = counter

    @property
    def floors(cls):
        """
        Returns a random number between 5 and 20
        """
        return randint(5, 20)


class Passenger:
    def __init__(self, floor_num, id, arrival_floor: int) -> None:
        self.floor_num = floor_num
        self._id = id
        self.arrival_floor = arrival_floor

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def __str__(self) -> str:
        return f"P{self.id} -> {self.arrival_floor}"


class Floor:
    def __init__(
        self, floor_num: int, building_floors_num: int, counter
    ) -> None:
        self.building_floors_num = building_floors_num
        self.floor_num = floor_num
        self._passengers = []
        self.counter = counter

        # generate a random number of passengers between 1 and 10
        # and assign a unique identifier for each
        self._passengers.extend(
            (
                Passenger(
                    self.floor_num,
                    next(self.counter),
                    self.arrival_floor(),
                )
                for _ in range(randint(0, 9))
            )
        )

    @property
    def passengers(self):
        return self._passengers

    def generate_random_arrival_floor_for_passenger(self):
        return randint(1, self.building_floors_num - 1)

    def arrival_floor(self):
        """
        Returns random arrival floor if it's not equal to the current floor
        """
        while True:
            arrival_floor = self.generate_random_arrival_floor_for_passenger()
            if arrival_floor != self.floor_num:
                try:
                    return arrival_floor
                except ValueError:
                    pass

    def __str__(self) -> str:
        return f"F{self.floor_num}"


class Board:
    def display(
        self,
        floor: Floor,
        elev_passengers: List[Passenger],
        previous_floor: Floor = None,
        next_floor: Floor = None,
        direct: str = "up",
    ):

        emoji_string = "  ".join(
            [
                emoji.emojize(":detective: ", language="en") + p.__str__()
                for p in elev_passengers
                if not (
                    p.arrival_floor == 1 and p.floor_num == floor.floor_num
                )
            ]
        )

        prev_floor_emoji_string = (
            ""
            if not previous_floor
            else self.generate_passengers_emoji_string(
                len(
                    [
                        p
                        for p in previous_floor.passengers
                        if not p.arrival_floor == previous_floor.floor_num
                    ]
                )
            )
        )
        next_floor_emoji_string = (
            ""
            if not next_floor
            else self.generate_passengers_emoji_string(
                len(
                    [
                        p
                        for p in next_floor.passengers
                        if not p.arrival_floor == next_floor.floor_num
                    ]
                )
            )
        )
        dashes_string = (
            len(
                sorted(
                    [
                        emoji_string,
                        prev_floor_emoji_string,
                        next_floor_emoji_string,
                    ],
                    key=lambda f_str: len(f_str),
                    reverse=True,
                )[0]
            )
            * "-"
        )

        floor_pointer = (
            (len(dashes_string) - len(emoji_string)) * " "
        ) + emoji.emojize(" :left_arrow:")
        fins_white_spaces = (
            (len(dashes_string) - len(next_floor_emoji_string)) + 1
        ) * " "

        direction_emoji = (
            emoji.emojize(":up_arrow: ", language="en")
            if direct == "up"
            else emoji.emojize(":down_arrow: ", language="en")
        )

        footer = "Direction: " + direction_emoji + f" Floor: {floor.floor_num}"
        fins = "|"

        print()
        print("...")
        print(footer)

        if previous_floor and previous_floor.floor_num < floor.floor_num:
            print(f"{fins}{dashes_string}")
            print(
                f"{fins}{previous_floor}{fins} ",
                fins_white_spaces,
                fins,
                self.generate_passenger_waiting_string(
                    floor.floor_num,
                    [
                        p
                        for p in previous_floor.passengers
                        if not p.arrival_floor == previous_floor.floor_num
                    ],
                ),
            )

        print(f"{fins}{dashes_string}")
        print(
            f"{fins}{floor}{fins} ",
            emoji_string,
            floor_pointer,
            fins_white_spaces,
            fins,
            self.generate_passenger_waiting_string(
                floor.floor_num,
                [
                    p
                    for p in floor.passengers
                    if not p.arrival_floor == floor.floor_num
                ],
            ),
        )

        if next_floor and floor.floor_num != 1:
            print(f"{fins}{dashes_string}")
            print(
                f"{fins}{next_floor}{fins} ",
                fins_white_spaces,
                fins,
                self.generate_passenger_waiting_string(
                    floor.floor_num,
                    [
                        p
                        for p in next_floor.passengers
                        if not p.arrival_floor == next_floor.floor_num
                    ],
                ),
            )

        print(f"{fins}{dashes_string}")
        print("...")
        print()

    def generate_passenger_waiting_string(
        self, current_floor: int, next_floor_passengers: List[Passenger]
    ):
        string = ""

        up = emoji.emojize(":arrow_up_small:", language="alias")
        down = emoji.emojize(":arrow_down_small:", language="alias")
        passenger_em = emoji.emojize(":detective:", language="en")
        space = "  "

        for passenger in next_floor_passengers:
            passenger_id = passenger.id
            if passenger.arrival_floor > current_floor:
                string += (
                    passenger_em
                    + " "
                    + str(passenger_id)
                    + "-> "
                    + str(passenger.arrival_floor)
                    + space
                    + up
                    + space
                )
            elif passenger.arrival_floor < current_floor:
                string += (
                    passenger_em
                    + " "
                    + str(passenger_id)
                    + "-> "
                    + str(passenger.arrival_floor)
                    + space
                    + down
                    + space
                )

        return string

    def generate_passengers_emoji_string(self, number_of_passenger: int):
        return "  ".join(
            [
                emoji.emojize(":detective:", language="en")
                for _ in range(number_of_passenger)
            ]
        )

    def display_passengers_status(
        self, passengers: List[Passenger], status: bool = True
    ):
        status_string = (
            "Entering passengers" if status else "Leaving passenger"
        )

        print()
        print(
            "*" * 5,
            status_string,
            "*" * 5,
        )

        for passenger in passengers:
            if status:
                print(
                    f"Passenger {passenger.id} has entered the elevator at floor {passenger.floor_num}"
                )

            else:
                print(
                    f"Passenger {passenger.id} has left the elevator at floor {passenger.arrival_floor}"
                )

        print(
            "*" * 5,
            len(status_string) * "*",
            "*" * 5,
        )
        print()

    def display_elevator_meta_data_passenegers(self, floors: List[Floor]):
        print("*" * 20)
        print("PASSENGERS IN EACH FLOOR")
        print("*" * 20)

        for floor in floors:
            print(floor, " : ", end=" ")
            [
                print(emoji.emojize(":detective:", language="en"), end=" | ")
                for p in floor.passengers
            ]
            print()

    def pop_up_text(self, text):
        print("*" * 30)
        print(bcolors.OKCYAN, text, bcolors.ENDC)
        print("*" * 30)

    def inline_text(self, text: str, color: str = None):
        if color == "red":
            print(bcolors.FAIL, text, bcolors.ENDC)
        elif color == "green":
            print(bcolors.OKGREEN, text, bcolors.ENDC)
        else:
            print(text)


class Elevator:
    def __init__(self, building: Building, board: Board) -> None:
        self.building: Building = building
        self.board: Board = board
        self.max_floor: int = 0
        self.min_floor: int = 0
        self.current_floor: int = 0
        self.direct = "up"
        self.passengers_count: int = 0
        self.elev_passengers: List[Passenger] = []
        self.left_elev_passengers: List[Passenger] = []
        self.entered_passengers: List[Passenger] = []

    def manage_entering_passengers(self, floor: Floor, current_floor: int):
        newly_entered_passengers = []

        floor_passengers = floor.passengers

        for passenger in floor_passengers:
            # check whether the elevator is going up or down
            if self.direct == "up":
                if passenger.arrival_floor > current_floor and not (
                    passenger.arrival_floor == current_floor
                ):
                    self.add_passenger(passenger)
                    newly_entered_passengers.append(passenger)

            elif self.direct == "down":
                if passenger.arrival_floor < current_floor and not (
                    passenger.arrival_floor == current_floor
                ):
                    self.add_passenger(passenger)
                    newly_entered_passengers.append(passenger)

        # remove the passenger so we don't have any dupliction in the
        # next iteration
        for entered_pass in newly_entered_passengers:
            if entered_pass in self.elev_passengers:
                floor_passengers.remove(entered_pass)

    def manage_leaving_passengers(self, passengers: List[Passenger]):
        passenegers = []

        for passenger in self.elev_passengers:
            if passenger.arrival_floor == self.current_floor:
                passenegers.append(passenger)
                self.remove_passenger(passenger)

        self.left_elev_passengers = passenegers

        # remove the passenger so we don't have any dupliction in the
        # next iteration
        for leaving_pass in passenegers:
            self.elev_passengers.remove(leaving_pass)

    def add_passenger(self, passenger: Passenger):
        if not self.passengers_count >= 5:
            self.elev_passengers.append(passenger)
            self.passengers_count += 1

            # update max_floor or min_floor if it's not bigger than the
            # passenger' arrival floor
            if self.direct == "up":
                if not self.max_floor > passenger.arrival_floor:
                    self.max_floor = passenger.arrival_floor
            elif self.direct == "down":
                if not self.min_floor > passenger.arrival_floor:
                    self.min_floor = passenger.arrival_floor

    def remove_passenger(self, passenger: Passenger):
        self.board.inline_text(
            f"Passenger {passenger.id} arrived at {passenger.arrival_floor} floor",
            color="red",
        )
        self.passengers_count -= 1

    def generate_floors(self) -> List[Floor]:
        floors_list = []

        building_floor = self.building.floors

        for floor_num in range(1, building_floor):
            floors_list.append(
                Floor(floor_num, building_floor, self.building.counter)
            )

        return floors_list

    def SetUp(self, floor: Floor):
        self.current_floor = floor.floor_num

    def move_up(
        self,
        floors: List[Floor],
        start_floor: Floor = None,
        is_reversed: bool = False,
    ):
        self.board.pop_up_text("Elevator is moving Up")

        self.direct = "up"

        if not is_reversed:
            floors = sorted(
                floors
                if not start_floor
                else floors[: floors.index(start_floor)],
                key=lambda f: f.floor_num,
            )

        for floor in floors:
            self.SetUp(floor)
            self.manage_entering_passengers(floor, floor.floor_num)
            self.manage_leaving_passengers(self.elev_passengers)

            prev_floor = (
                None
                if not index_in_list(floors, floor.floor_num - 2)
                else floors[floor.floor_num - 2]
            )
            next_floor = (
                None
                if not index_in_list(floors, floor.floor_num)
                else floors[floor.floor_num]
            )

            if not self.is_elevator_empty:
                self.board.display(
                    floor,
                    self.elev_passengers,
                    prev_floor,
                    next_floor,
                    self.direct,
                )

        self.direct = "down"

    def move_down(
        self,
        floors: List[Floor],
        start_floor: Floor = None,
        is_reversed: bool = False,
    ):
        self.board.pop_up_text("Elevator is moving Down")

        self.direct = "down"

        reversed_floors = sorted(
            floors if not start_floor else floors[: floors.index(start_floor)],
            key=lambda f: f.floor_num,
            reverse=True,
        )

        for floor in reversed_floors:
            self.SetUp(floor)
            self.manage_entering_passengers(floor, floor.floor_num)
            self.manage_leaving_passengers(self.elev_passengers)

            prev_floor = (
                None
                if not index_in_list(floors, floor.floor_num - 2)
                else floors[floor.floor_num - 2]
            )
            next_floor = (
                None
                if not index_in_list(floors, floor.floor_num)
                else floors[floor.floor_num]
            )

            if not self.is_elevator_empty:
                self.board.display(
                    floor,
                    self.elev_passengers,
                    prev_floor,
                    next_floor,
                    self.direct,
                )

        self.direct = "up"

    def is_passengers_exists(self, floors: List[Floor]):
        for floor in floors:
            if len(floor.passengers) > 0:
                return True

        return False

    def find_nearest_floor_with_passengers(
        self, floor: Floor, floors: List[Floor]
    ):
        floor_indx = floors.index(floor)

    def run(self):
        """
        Runs the elevator until there's no 
        """
        floors = self.generate_floors()
        self.board.display_elevator_meta_data_passenegers(floors)

        while self.is_passengers_exists(floors):
            if self.direct == "up":
                self.move_up(floors)
            elif self.direct == "down":
                self.move_down(floors)

    @property
    def is_elevator_empty(self):
        return len(self.elev_passengers) == 0


if "__main__" == __name__:
    counter = itertools.count(start=1)
    board = Board()
    building = Building(counter)
    elevator = Elevator(building, board)
    elevator.run()
