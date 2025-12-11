import os
import random
import time

GREN = "\033[32m"
END = "\033[0m"

def buses(n1, n2, n3):
    output = []
    output.append(115 * "-")
    output.append((n1 * " ") + "_______________  " + ((100 - n1) * " ") + "|")
    output.append((n1 * " ") + "|__|__|__|__|__|___ " + ((97  - n1) * " ") + "|")
    output.append((n1 * " ") + "|    RED BULL     |)" + ((96  - n1) * " ") + "|")
    output.append((n1 * " ") + "|~~~@~~~~~~~~~@~~~|)" + ((95  - n1) * " ") + "|")
    output.append(115 * "_")
    output.append((n2 * " ") + "_______________  " + ((100 - n2) * " ") + "|")
    output.append((n2 * " ") + "|__|__|__|__|__|___ " + ((97  - n2) * " ") + "|")
    output.append((n2 * " ") + "|    MONSTER      |)" + ((96  - n2) * " ") + "|")
    output.append((n2 * " ") + "|~~~@~~~~~~~~~@~~~|)" + ((95  - n2) * " ") + "|")
    output.append(115 * "_")
    output.append((n3 * " ") + "_______________  " + ((100 - n3) * " ") + "|")
    output.append((n3 * " ") + "|__|__|__|__|__|___ " + ((97  - n3) * " ") + "|")
    output.append((n3 * " ") + "|    Coca Cola    |)" + ((96  - n3) * " ") + "|")
    output.append((n3 * " ") + "|~~~@~~~~~~~~~@~~~|)" + ((95  - n3) * " ") + "|")
    output.append(115 * "_")
    return "\n".join(output)

class Race:
    def __init__(self):
        self.positions = [0, 0, 0]  # [RED BULL, MONSTER, Coca Cola]
        self.winner = None

    def advance_bus(self, bus_index):
        if 0 <= bus_index < len(self.positions):
            self.positions[bus_index] += 1
            if self.positions[bus_index] >= 97:
                self.winner = ["RED BULL", "MONSTER", "Coca Cola"][bus_index]

    def is_finished(self):
        return any(pos >= 97 for pos in self.positions)

    def get_winner(self):
        return self.winner

def main():
    race = Race()
    os.system("cls" if os.name == "nt" else "clear")
    presentacion = """
         <<<<<<<<<<< carrera de buses >>>>>>>>>>
             RED BULL VS MONSTER VS Coca Cola """
    print(presentacion)
    time.sleep(3)

    while not race.is_finished():
        bus_to_advance = random.randint(0, 2)
        race.advance_bus(bus_to_advance)
        os.system("cls" if os.name == "nt" else "clear")
        print(buses(*race.positions))
        time.sleep(0.07)

    winner = race.get_winner()
    if winner:
        print(f"{GREN}GANÓ LA CARRERA: {winner}{END}")
    else:
        print("La carrera terminó sin un ganador.")

if __name__ == "__main__":
    main()
