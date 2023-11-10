import time

from board import Board
from bogo import BogoVacuum, RandomMovementVacuum, NoRepeatVacuum
from predefined import SpiralVacuum
from sight import SuperSightVacuum, OptimizedSuperSightVacuum


def carregar_ambiente(linhas, colunas, porcentagem):
    arquivo = "ambiente_{}x{}_{}.txt".format(linhas, colunas, porcentagem)
    environment = Board(linhas, colunas)

    with open(arquivo, "r") as arquivo:
        for linha in arquivo:
            for ch in linha.strip().split():
                environment.board = not bool(int(ch))

    return environment


if __name__ == "__main__":
    agents = [
        # BogoVacuum,
        # RandomMovementVacuum,
        NoRepeatVacuum,
        # SpiralVacuum,
        # SuperSightVacuum,
        # OptimizedSuperSightVacuum,
    ]
    boards = [
        (100, 100, 3500, 35),
        (100, 100, 6500, 65),
        (200, 200, 14000, 35),
        (200, 200, 26000, 65),
        (300, 300, 31500, 35),
        (300, 300, 58500, 65),
        (400, 300, 42000, 35),
        (400, 300, 78000, 65),
    ]
    for settings in boards:
        M, N, dirty_spaces, percentage = settings

        environment = carregar_ambiente(M, N, percentage)
        # environment = Board(M, N)
        # environment.dirt(dirty_spaces)
        board = environment.board

        for agent in agents:
            # Creating board
            print(
                "# Creating environment",
                f"Board Size: {M}x{N}",
                f"Dirty squares: {dirty_spaces}",
                sep="\n",
                end="\n\n",
            )
            agent_env = Board(M, N)
            agent_env.board = [row.copy() for row in board]

            # Create a vacuum
            print("# Creating agent")
            print(f"Agent type: {agent.__name__}")
            battery = input("Agent battery (empty for infinite): ")
            if not battery:
                battery = None
            else:
                battery = int(battery)
            vacuum = agent(battery=battery, position=[0, 0])

            # Run the vacuum
            print("\n# Running agent...")
            real_time = time.time()
            vacuum.run(agent_env, False)

            print("# Finished!")
            real_time = time.time() - real_time

            # Count cleaned spaces based on the vacuum's memory
            cleaned_spaces = sum(
                action.startswith("Cleaned") for action in vacuum.history
            )

            battery_used = sum(
                action.startswith("Tried") or action.startswith("Moved")
                for action in vacuum.history
            )

            # Calculate the percentage of the total board that is cleaned
            total_spaces = M * N
            percentage_cleaned = (cleaned_spaces / total_spaces) * 100

            # Print the results
            print("\n# Results")
            if cleaned_spaces == dirty_spaces:
                print("The floor is clean. Mission accomplished!")

            print(f"Dirty squares cleaned: {cleaned_spaces}/{dirty_spaces}")
            print(f"Percentage of the total board cleaned: {percentage_cleaned:.2f}%")
            print(f"Total time elapsed: {real_time:.4f} seconds")
            if battery is not None:
                print(f"Left over battery: {vacuum.battery}/{battery}")
            else:
                print(f"Total battery used: {battery_used}")
            print("=======================\n")
