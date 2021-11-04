import numpy as np
import random
from itertools import groupby
from itertools import product
import time


class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()# Didn't add any code inside reset. Re-instantiating the env class for every episode in the notebook


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        winning_value = 15
        if (sum(curr_state[0:9:4]) == winning_value): # diagonal1
            return True
        elif (sum(curr_state[2:7:2]) == winning_value): # diagonal2
            return True
        elif (sum(curr_state[0:3]) == winning_value): # row1
            return True
        elif (sum(curr_state[3:6]) == winning_value): # row2
            return True
        elif (sum(curr_state[6:9]) == winning_value): # row3
            return True
        elif (sum(curr_state[0:7:3]) == winning_value): # column1
            return True
        elif (sum(curr_state[1:8:3]) == winning_value): # column2
            return True
        elif (sum(curr_state[2:9:3]) == winning_value): # column3
            return True
        else:
            return False
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) == 0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_env_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) env values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return env_values

    def allowed_agent_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) agent values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]

        return agent_values


    def agent_actions(self, curr_state):
        """Takes the current state as input and returns all possible agent actions, i.e, all combinations of allowed positions and allowed values"""
        agent_values = self.allowed_agent_values(curr_state)
        allowed_positions = self.allowed_positions(curr_state)
        agent_actions = product(allowed_positions, agent_values)
        return agent_actions

    def env_actions(self, curr_state):
        """Takes the current state as input and returns all possible env actions, i.e, all combinations of allowed positions and allowed values"""
        env_values = self.allowed_env_values(curr_state)
        allowed_positions = self.allowed_positions(curr_state)
        env_actions = product(allowed_positions, env_values)
        return env_actions



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        curr_state[curr_action[0]] = curr_action[1]
        return curr_state


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        It also returns whether the agent has won or not. This is helpful in calculating the agent's winning % in the notebook
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False, 0)"""

        #Agent action
        agent_state = self.state_transition(curr_state,curr_action)
        terminate, result = self.is_terminal(agent_state)
        reward = 0
        agent_win = 0
        # Checking the status after agent action
        if terminate:
            if result == 'Win':
                reward = 10-1 # 10-1 because we need to give the reward as -1 for every step that agent takes
                agent_win = 1
            else: # Tie
                reward = 0-1 # 0-1 because we need to give the reward as -1 for every step that agent takes

            return agent_state, reward, terminate, agent_win

        else: # If it is not terminate after agent's action, going ahead with the environment's random action

            # Environment random action
            env_actions = list(self.env_actions(agent_state))
            random_env_action = random.choice(env_actions)
            env_state = self.state_transition(agent_state,random_env_action)
            terminate, result = self.is_terminal(env_state) 

            # Checking the status after env action
            if terminate:
                if result == 'Win':
                    reward = -10-1 # -10-1 because we need to give the reward as -1 for every step that agent takes
                else: #Tie
                    reward = 0-1 # 0-1 because we need to give the reward as -1 for every step that agent takes
            else: # Resume
                reward = -1

            return env_state, reward, terminate, agent_win



    def reset(self):
        return self.state


'''env = TicTacToe()
state = [1, 2, np.nan, 
         4, np.nan, 6, 
         np.nan, 9, 3]
curr_action = (2,5)
number =1000
start_time = time.time()
for i in range(number):
    env.step(state, curr_action)
end_time = time.time()
print((end_time-start_time)/number)'''