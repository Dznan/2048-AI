import h5py  #导入工具包  
import numpy as np  

#HDF5的读取：  
f = h5py.File('dqn_new_2048_cnn_onehot2steps_weights.h5f','r')   #打开h5文件  
print(f.keys())                            #可以查看所有的主键  
# a = f['data'][:]                    #取出主键为data的所有的键值  
f.close()  