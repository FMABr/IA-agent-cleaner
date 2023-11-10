import time

from board import Board
from bogo import BogoVacuum, RandomMovementVacuum, NoRepeatVacuum
from predefined import SpiralVacuum
from sight import SuperSightVacuum, OptimizedSuperSightVacuum


if __name__ == "__main__":
    agents = [
        # BogoVacuum,
        # RandomMovementVacuum,
        # NoRepeatVacuum,
        SpiralVacuum,
        # SuperSightVacuum,
        # OptimizedSuperSightVacuum,
    ]
    boards = [
        (20, 20, 400),
        # (100, 100, 3500),
        # (100, 100, 6500),
        # (1000, 1000, 350000),
        # (1000, 1000, 650000),
    ]
    for settings in boards:
        M, N, dirty_spaces = settings

        environment = Board(M, N)
        environment.dirt(dirty_spaces)
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
            vacuum.run(agent_env, True)

            print("# Finished!")
            real_time = time.time() - real_time

            # Count cleaned spaces based on the vacuum's memory
            cleaned_spaces = sum(
                action.startswith("Cleaned") for action in vacuum.history
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
            print("=======================\n")
