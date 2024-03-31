import sys
from environment import Environment


if __name__ == "__main__":
    env = Environment(keyboard_control=True)

    env.run()


