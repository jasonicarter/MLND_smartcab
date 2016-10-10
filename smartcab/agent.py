import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import Counter

# Track results of trials
results = Counter()


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(
            env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # TODO: Initialize any additional variables here
        random.seed()  # initialize number generator
        self.state = None
        self.qtable = {}
        self.alpha = 0.2  # learning rate
        self.epsilon = 0.1  # exploration rate
        self.gamma = 0.4  # discount factor
        self.total_reward = 0
        self.last_reward = 0
        self.last_action = None
        self.last_state = None
        self.valid_actions = Environment.valid_actions
        # self.results = Counter()

    def reset(self, destination=None):
        self.planner.route_to(destination)

        # TODO: Prepare for a new trip; reset any variables here, if required
        self.state = None
        self.total_reward = 0
        self.last_reward = 0
        self.last_action = None
        self.last_state = None

    def get_action(self):
        if random.random() > self.epsilon and (self.state in self.qtable):
            # assign max Q value for current state
            max_q = self.qtable[self.state].index(max(self.qtable[self.state]))
            # assign action based on max Q value
            action = self.valid_actions[max_q]
        else:
            action = random.choice(self.valid_actions)

        return action

    def update_policy(self, action, reward):
        if self.state not in self.qtable:
            self.qtable[self.state] = [0, 0, 0, 0]

        if self.last_state not in self.qtable:
            self.qtable[self.last_state] = [0, 0, 0, 0]

        # Update q table based on the Q-learning =>
        # Q(state, action) = alpha(r + gamma * max[Q(next state, actions)] - Q[s,a])

        self.qtable[self.state][self.valid_actions.index(action)] = \
            (
                self.qtable[self.last_state][self.valid_actions.index(self.last_action)] +  # Q[s,a] +
                self.alpha * (reward + self.gamma * max(self.qtable[self.state]) -  # alpha ( r+gamma*maxQ[s',a'] -
                              self.qtable[self.last_state][self.valid_actions.index(self.last_action)])  # Q[s,a])
            )

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        # input['right'] is not required
        self.state = (inputs['light'], inputs['oncoming'], inputs['left'], self.next_waypoint)

        # TODO: Select action according to your policy
        action = self.get_action()

        # Execute action and get reward
        reward = self.env.act(self, action)
        results['penalties'] += reward if reward < 0 else 0
        self.total_reward += reward

        # TODO: Learn policy based on state, action, reward
        self.update_policy(action, reward)

        self.last_action = action
        self.last_reward = reward
        self.last_state = self.state

        # print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}" \
        #     .format(deadline, inputs, action, reward)  # [debug]

        # Track results
        if self.env.done:  # if destination reached
            results['win'] += 1
            results['reward'] += self.total_reward
            # print 'Results {}'.format(self.results)
        elif deadline == 0:
            results['lose'] += 1
            results['reward'] += self.total_reward
            # print 'Results {}'.format(self.results)


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.05,
                    display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=10)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()

print 'Results {}'.format(results)
