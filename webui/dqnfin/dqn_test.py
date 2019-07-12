import os, fnmatch, pickle

import numpy as np
import random
import time

from dqnfin.dqn_env import Game2048Env 
import dqnfin.eval_func

from keras.models import Sequential, Model, load_model
from keras.layers import Dense, Conv2D, Flatten, Input, concatenate, Reshape
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
MODEL_TYPE = 'cnn' 
NUM_ACTIONS_OUTPUT_NN = 4 
WINDOW_LENGTH = 1
INPUT_SHAPE = (4, 4) 

PREPROC="onehot2steps" 
NUM_ONE_HOT_MAT = 16 

NB_STEPS_TRAINING = int(1e6) 
NB_STEPS_ANNEALED = int(2e4) 
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

random_seed = int(time.time())
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
        try:
            batch = np.reshape(batch, (self.window_length, self.window_length*(4+4*4)*self.num_one_hot_matrices, 4, 4))
        except:
            batch = np.reshape(batch, (np.shape(batch)[0], self.window_length*(4+4*4)*self.num_one_hot_matrices, 4, 4))
            pass
        return batch

class IllegalMove(Exception):
    pass

processor = OneHotNNInputProcessor(num_one_hot_matrices=NUM_ONE_HOT_MAT)


K.set_image_dim_ordering('th') # th: theano, tf: tensorflow
# Otherwise we can use the data_format parameter to be passed to the Conv2D() functions:
#    data_format = 'channels_first'
#    data_format = 'channels_last'

# Set the CNN hyperparameters:
# CNN Layers:
NUM_FILTERS_LAYER_1 = 512   # number of filters in 1st layer
NUM_FILTERS_LAYER_2 = 4096  # number of filters in 2nd layer
# NUM_FILTERS_LAYER_1 = 32
# NUM_FILTERS_LAYER_2 = 64
FILTERS_SIZE_LAYER_1 = 3 # Filter Size = 3 x 3
FILTERS_SIZE_LAYER_2 = 1 # Filter Size = 1 x 1
ACTIVATION_FTN_CNN = 'relu'
# Dense/Output Layers:
NUM_DENSE_NEURONS = 512
ACTIVATION_FTN_DENSE = 'relu'
ACTIVATION_FTN_OUTPUT = 'linear'
INPUT_SHAPE_CNN = (WINDOW_LENGTH*(4+4*4)*NUM_ONE_HOT_MAT,) + INPUT_SHAPE # Ex. (320,4,4)
# CNN model definition:
#    We use the Functional API of Keras (https://keras.io/getting-started/functional-api-guide/) 
_input = Input(shape=INPUT_SHAPE_CNN)
conv_a = Conv2D(filters=NUM_FILTERS_LAYER_1, kernel_size=FILTERS_SIZE_LAYER_1, strides=(2,1), padding='valid', activation=ACTIVATION_FTN_CNN)(_input)
conv_b = Conv2D(filters=NUM_FILTERS_LAYER_1, kernel_size=FILTERS_SIZE_LAYER_1, strides=(1,2), padding='valid', activation=ACTIVATION_FTN_CNN)(_input)
conv_aa = Conv2D(filters=NUM_FILTERS_LAYER_2, kernel_size=FILTERS_SIZE_LAYER_2, strides=(2,1), padding='valid', activation=ACTIVATION_FTN_CNN)(conv_a)
conv_ab = Conv2D(filters=NUM_FILTERS_LAYER_2, kernel_size=FILTERS_SIZE_LAYER_2, strides=(1,2), padding='valid', activation=ACTIVATION_FTN_CNN)(conv_a)
conv_ba = Conv2D(filters=NUM_FILTERS_LAYER_2, kernel_size=FILTERS_SIZE_LAYER_2, strides=(2,1), padding='valid', activation=ACTIVATION_FTN_CNN)(conv_b)
conv_bb = Conv2D(filters=NUM_FILTERS_LAYER_2, kernel_size=FILTERS_SIZE_LAYER_2, strides=(1,2), padding='valid', activation=ACTIVATION_FTN_CNN)(conv_b)
merge = concatenate([Flatten()(x) for x in [conv_aa, conv_ab, conv_ba, conv_bb, conv_a, conv_b]])
_output = Dense(units=NUM_ACTIONS_OUTPUT_NN, activation='linear')(merge)
model = Model(inputs=_input, outputs=_output)
print(model.summary())

memory = SequentialMemory(limit=MEMORY_SIZE, window_length=WINDOW_LENGTH)

TRAIN_POLICY = LinearAnnealedPolicy(EpsGreedyQPolicy(), attr='eps', value_max=0.05, value_min=0.05, value_test=0.01, nb_steps=NB_STEPS_ANNEALED)
TEST_POLICY = EpsGreedyQPolicy(eps=.01)
dqn = DQNAgent(model=model, nb_actions=NUM_ACTIONS_OUTPUT_NN, test_policy=TEST_POLICY, policy=TRAIN_POLICY, memory=memory, processor=processor,
                nb_steps_warmup=NB_STEPS_WARMUP, gamma=.99, target_model_update=TARGET_MODEL_UPDATE, train_interval=4, delta_clip=1.) 
dqn.compile(Adam(lr=.00025), metrics=['mse'])

weights_filepath = data_filepath + '/dqn_new_{}_{}_{}_weights.h5f'.format(ENV_NAME, MODEL_TYPE, PREPROC)
dqn.load_weights(weights_filepath)

memory = (memory, memory.actions, memory.rewards, memory.terminals, memory.observations)

prehot = np.array([[2,2,2,2],[2,2,2,2],[2,2,2,2],[2,2,2,2]])


def predict(grid):
    env.reset() 
    batch = processor.process_observation(grid)
    state = dqn.memory.get_recent_state(batch)
    q_values = dqn.compute_q_values(state)
    action = dqn.test_policy.select_action(q_values=q_values)
    env.set_board(np.array(grid))
    moved = env.move2(action, trial=True)
    if moved:
        return action
    else:
        return random.randint(0, 3)
    # return action
    # dqn.test(env, nb_episodes=1, visualize=True, verbose=0)
    
predict(prehot)

