import os, fnmatch, pickle

import numpy as np
import random

from dqn_env import Game2048Env 

from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Conv2D, Flatten, Input
from keras.layers.merge import concatenate
from keras.optimizers import Adam
import keras.backend as K

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy, LinearAnnealedPolicy, GreedyQPolicy
from rl.memory import SequentialMemory
from rl.core import Processor

prj_path = 'E:\\Dqn'
data_filepath = prj_path + '\\data' 
if not os.path.exists(data_filepath): 
    os.makedirs(data_filepath)

TRAIN_TEST_MODE = 'train'
MODEL_TYPE = 'dnn' 
NUM_ACTIONS_OUTPUT_NN = 4 
WINDOW_LENGTH = 1
INPUT_SHAPE = (4, 4) 

PREPROC="onehot2steps" 
NUM_ONE_HOT_MAT = 16 

NB_STEPS_TRAINING = int(5e6) 
NB_STEPS_ANNEALED = int(5e4) 
NB_STEPS_WARMUP = 5000
MEMORY_SIZE = 6000
TARGET_MODEL_UPDATE = 1000

INPUT_SHAPE_DNN = (WINDOW_LENGTH, 4+4*4, NUM_ONE_HOT_MAT,) + INPUT_SHAPE 

# NUM_DENSE_NEURONS_DNN_L1 = 128
# NUM_DENSE_NEURONS_DNN_L2 = 64 
# NUM_DENSE_NEURONS_DNN_L3 = 32
NUM_DENSE_NEURONS_DNN_L1 = 1024 
NUM_DENSE_NEURONS_DNN_L2 = 512  
NUM_DENSE_NEURONS_DNN_L3 = 256  
ACTIVATION_FTN_DNN = 'relu'
ACTIVATION_FTN_DNN_OUTPUT = 'linear'

ENV_NAME = '2048'
env = Game2048Env()

random_seed = 123
random.seed(random_seed)
np.random.seed(random_seed)
env.seed(random_seed)

class OneHotNNInputProcessor(Processor):
    def __init__(self, num_one_hot_matrices=16, window_length=1, model="dnn"):
        self.num_one_hot_matrices = num_one_hot_matrices
        self.window_length = window_length
        self.model = model
        
        self.game_env = Game2048Env() 
        
        
        self.table = {2**i:i for i in range(1,self.num_one_hot_matrices)} 
        self.table[0] = 0 
    
    def one_hot_encoding(self, grid):
        grid_onehot = np.zeros(shape=(self.num_one_hot_matrices, 4, 4))
        for i in range(4):
            for j in range(4):
                grid_element = grid[i, j]
                grid_onehot[self.table[grid_element],i, j]=1
        return grid_onehot

    def get_grids_next_step(self, grid):
        grids_list = [] 
        for movement in range(4): 
            grid_before = grid.copy()
            self.game_env.set_board(grid_before)
            try:
                _ = self.game_env.move(movement) 
            except:
                pass
            grid_after = self.game_env.get_board()
            grids_list.append(grid_after)
        return grids_list

    def process_observation(self, observation):
        observation = np.reshape(observation, (4, 4))

        grids_list_step1 = self.get_grids_next_step(observation)
        grids_list_step2 =[]
        for grid in grids_list_step1:
            grids_list_step2.append(grid) 
            grids_temp = self.get_grids_next_step(grid)
            for grid_temp in grids_temp:
                grids_list_step2.append(grid_temp)
        grids_list = np.array([self.one_hot_encoding(grid) for grid in grids_list_step2])
        
        return grids_list
    
    def process_state_batch(self, batch):
        if self.model == "cnn": 
            try:
                batch = np.reshape(batch, (self.window_length, self.window_length*(4+4*4)*self.num_one_hot_matrices, 4, 4))
            except:
                batch = np.reshape(batch, (np.shape(batch)[0], self.window_length*(4+4*4)*self.num_one_hot_matrices, 4, 4))
                pass
        return batch

processor = OneHotNNInputProcessor(num_one_hot_matrices=NUM_ONE_HOT_MAT)


model = Sequential()
model.add(Flatten(input_shape=INPUT_SHAPE_DNN))
model.add(Dense(units=NUM_DENSE_NEURONS_DNN_L1, activation=ACTIVATION_FTN_DNN))
model.add(Dense(units=NUM_DENSE_NEURONS_DNN_L2, activation=ACTIVATION_FTN_DNN))
model.add(Dense(units=NUM_DENSE_NEURONS_DNN_L3, activation=ACTIVATION_FTN_DNN))
model.add(Dense(units=NUM_ACTIONS_OUTPUT_NN, activation=ACTIVATION_FTN_DNN_OUTPUT))
print(model.summary())

memory = SequentialMemory(limit=MEMORY_SIZE, window_length=WINDOW_LENGTH)

TRAIN_POLICY = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=0.05, value_min=0.05, value_test=0.01, nb_steps=NB_STEPS_ANNEALED)
TEST_POLICY = EpsGreedyQPolicy(eps=.01)
dqn = DQNAgent(model=model, nb_actions=NUM_ACTIONS_OUTPUT_NN, test_policy=TEST_POLICY, policy=TRAIN_POLICY, memory=memory, processor=processor,
                nb_steps_warmup=NB_STEPS_WARMUP, gamma=.99, target_model_update=TARGET_MODEL_UPDATE, train_interval=4, delta_clip=1.) 
dqn.compile(Adam(lr=.00025), metrics=['mse'])

weights_filepath = data_filepath + '/dqn_{}_{}_{}_weights.h5f'.format(ENV_NAME, MODEL_TYPE, PREPROC)
checkpoint_weights_filepath = data_filepath + '/dqn_' + ENV_NAME + '_' + MODEL_TYPE + '_' + PREPROC + '_weights_' + '{step}.h5f'
csv_filepath = data_filepath + '/dqn_{}_{}_{}_train.csv'.format(ENV_NAME, MODEL_TYPE, PREPROC)

dqn.fit(env, nb_steps=NB_STEPS_TRAINING, visualize=False, verbose=0) 

dqn.save_weights(weights_filepath, overwrite=True)

memory = (memory, memory.actions, memory.rewards, memory.terminals, memory.observations)

env.reset() 

dqn.test(env, nb_episodes=1, visualize=True, verbose=0) 
# if 'nb_training_steps_pickle' in locals(): 
    
#     agentmem_filepath = data_filepath + '/dqn_{}_{}_{}_{}_agentmem.pkl'.format(ENV_NAME, MODEL_TYPE, PREPROC, NB_STEPS_TRAINING + nb_training_steps_pickle)
#     pickle.dump(memory, open(agentmem_filepath, "wb"))
    
#     model_filepath = data_filepath + '/dqn_{}_{}_{}_{}_model.h5'.format(ENV_NAME, MODEL_TYPE, PREPROC, NB_STEPS_TRAINING + nb_training_steps_pickle)
#     model.save(model_filepath)  
# else:
    
#     agentmem_filepath = data_filepath + '/dqn_{}_{}_{}_{}_agentmem.pkl'.format(ENV_NAME, MODEL_TYPE, PREPROC, NB_STEPS_TRAINING)
#     pickle.dump(memory, open(agentmem_filepath, "wb"), protocol=-1) 
    
#     agent_filepath = data_filepath + '/dqn_{}_{}_{}_{}_agent.pkl'.format(ENV_NAME, MODEL_TYPE, PREPROC, NB_STEPS_TRAINING)
#     pickle.dump(dqn, open(agent_filepath, "wb"), protocol=-1) 
    
#     model_filepath = data_filepath + '/dqn_{}_{}_{}_{}_model.h5'.format(ENV_NAME, MODEL_TYPE, PREPROC, NB_STEPS_TRAINING)
#     model.save(model_filepath)  


env.reset() 

dqn.test(env, nb_episodes=5, visualize=False, verbose=0) 