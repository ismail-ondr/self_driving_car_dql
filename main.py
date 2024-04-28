import torch
from environment import Environment
from dql_agent import DQLAgent
import matplotlib.pyplot as plt

if __name__ == "__main__":
    env = Environment(keyboard_control=False)
    #env.run()


    agent = DQLAgent(env)

    batch_size = 16
    episodes = 200
    time_array = []
    reward_array = []

    for e in range(episodes):

        state = env.reset()

        time = 0
        total_reward = 0
        while True:
            # act
            action = agent.act(state)  # select an action

            # step
            next_state, reward, done = env.update(action)

            total_reward += reward

            # remember / storage
            agent.remember(state, action, reward, next_state, done)

            # update state
            state = next_state

            # replay
            agent.replay(batch_size)

            # adjust epsilon
            agent.adaptiveEGreedy()

            time += 1

            if done or total_reward > 10000:
                time_array.append(time)
                reward_array.append(total_reward)

                print("Episode: {}, time: {}, reward: {}".format(e, time, total_reward))
                if e % 20 == 0:
                    torch.save(agent.model.state_dict(), "model/model" + str(e) + ".pt")
                break

    torch.save(agent.model.state_dict(), "model/final_model.pt")

    plt.plot(time_array, label='Time')
    plt.plot(reward_array, label='Reward')

    plt.legend()
    plt.grid(True)
    plt.savefig('plot.png')