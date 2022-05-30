import csv
import math
import sys
import numpy as np


# from maths_learning centre
def Viterbi(state_space, transition_matrix, emission_matrix, Sequence_y):
    Observation_space = ['0000', '1000', '0100', '0010', '0001','1100', '1010', '1001', 
                         '0110', '0101', '0011','0111', '1011', '1101', '1110','1111']
   
    state_space = traverable_position
    initial_probability = np.repeat(1/len(traverable_position), len(traverable_position))
    Sequence_y = Sequence_y
    T_ = transition_matrix
    O_ = emission_matrix.T 
    
    observation_steps_prob = []
    for indx in observation_index:
        observation_prob = O_[indx]
        observation_steps_prob.append(observation_prob)

    # t_0 to t_1  
    trellis = np.zeros((len(traverable_position), len(Sequence_y)))
    
    for i in range(len(traverable_position)):
        trellis[i,0] = 1/len(traverable_position) * observation_steps_prob[0][i]
        
    for j in range(1, len(Sequence_y)):
        for i in range(len(traverable_position)):
            observation_y = observation_steps_prob[j][i]
            max_index = 0
            max_trellis = 0
            for k in range(len(traverable_position)):
                temp_value = trellis[k, j-1] * T_[k][i] * observation_y
                if temp_value > max_trellis:
                    max_index = k
                    max_trellis = temp_value
            trellis[i,j] = max_trellis
            
    trellis = trellis.T
    
    final_map_list = []
    for state_map in trellis:
        final_X = []
        np_inx = 0
        for i in range(size_of_map[0]*size_of_map[1]):
            if i not in remove_obstacle_rows:
                final_X.append(state_map[np_inx])
                np_inx += 1
            else:
                final_X.append(0.0)
        final_X = np.array(final_X)
        final_map = final_X.reshape(size_of_map[0], size_of_map[1])
        final_map_list.append(final_map)
    
    np.savez("output.npz", *final_map_list)
            
    return T_, O_, final_map_list, trellis



if __name__ == "__main__":

    map_txt = sys.argv[1]
    
    #map_txt = 'A3_txt'
    f = open(map_txt)
    readMap = csv.reader(f)

    size_of_map_text = next(readMap)
    size_of_map = size_of_map_text[0].split(" ")
    size_of_map = [int(i) for i in size_of_map]
    
    state_map_list = []
    for row in readMap:
        state_map_list.append(row[0].split(" "))
        
    state_map = state_map_list[:size_of_map[0]]
    
    sensors = state_map_list[size_of_map[0]]
    sensors = int(sensors[0])
    
    Sequence_y = []
    for i in range(1, sensors+1):
        step = state_map_list[size_of_map[0]+i][0]
        Sequence_y.append(step)
    
    err = float(state_map_list[size_of_map[0]+sensors+1][0])
    
    state_map = np.array(state_map)
    
    traverable_position = []
    non_traverable_position = []
    for i in range(state_map.shape[0]):
        for j in range(state_map.shape[1]):
            if state_map[i][j] == '0':
                traverable_position.append((i,j))
            if state_map[i][j] == 'X':
                non_traverable_position.append((i,j))
                
    temp_map = []
    for iy in range(size_of_map[0]+2):
        temp_row = []
        if iy == 0:
            for ix in range(size_of_map[1]+2):
                temp_row.append("-")
        elif iy == size_of_map[0]+1:
            for ix in range(size_of_map[1]+2):
                temp_row.append("-")
        else:
            temp_row.append("-")
            for ix in range(size_of_map[1]):
                temp_row.append(state_map_list[iy-1][ix])
            temp_row.append("-")
        temp_map.append(temp_row)
        
    
    #Find observation of each state
    Observation_list = []
    for i in range(1, len(temp_map)-1):
        Observation_ = []
        for j in range(1, len(temp_map[i])-1):
            current_position = temp_map[i][j]
            N = temp_map[i-1][j]
            E = temp_map[i][j+1]
            S = temp_map[i+1][j]
            W = temp_map[i][j-1]
            observation = str(N)+str(E)+str(S)+str(W)
            Observation_.append(observation)
        Observation_list.append(Observation_)
    Observation_list = np.array(Observation_list)
    
    #Get index (i, j) of each state
    index_list = []
    for i in range(0, size_of_map[0]):
        for j in range(0, size_of_map[1]):
            index_list.append((i, j))
            
    #Transformation matrix - for each position probability = 1/number of traversable neighour cells (includes "X")
    dict_list = []
    for i in range(Observation_list.shape[0]):
        for j in range(Observation_list.shape[1]):
            indx_key = index_list
            value = np.repeat(0, size_of_map[0]*size_of_map[1])
            count_dict = dict(zip(indx_key, value))
            position = [i,j]
            observation = Observation_list[i][j]
            N = (i-1, j)
            E = (i, j+1)
            S = (i+1, j)
            W = (i, j-1)
            count_0 = observation.count('0')
            count_X = observation.count('X')
            
            if count_0 == 0:
                prob_X = 0
            else:
                prob_X = round(1/(count_0), 4)
            
            #find the direction i.e NESW of '0' and put into list, and put probability in the direction NESW coordinate (i,j).
            position_0 = [i for i, e in enumerate(list(observation)) if e == '0']

            if 0 in position_0:
                count_dict[N] = prob_X
            if 1 in position_0:
                count_dict[E] = prob_X
            if 2 in position_0:
                count_dict[S] = prob_X
            if 3 in position_0:
                count_dict[W] = prob_X
            dict_list.append(count_dict)    
            
            
    #transform the probability value to transformation matrix
    value_list = []
    for i in range(len(dict_list)):
        values = list(dict_list[i].values())
        value_list.append(values)
            
    T_np = np.array(value_list)
    T_np = T_np.T

                    
    #find the index of non_traverable_position'X' for removal in transformation numpy matrix 
    remove_obstacle_rows = []
    for i, index in zip(list(range(len(index_list))), index_list):
        if index in non_traverable_position:
            remove_obstacle_rows.append(i)
                
    T_ = np.delete(T_np, remove_obstacle_rows, axis=1)
    T_ = np.delete(T_, remove_obstacle_rows, axis=0)
    T_ = T_.T
    transition_matrix = T_
        
    #Create emission matrix, -> from observation forming emission representation ie.'1001' for each state
    Observation_list_O = []
    for i in range(1, len(temp_map)-1):
        Observation_ = []
        for j in range(1, len(temp_map[i])-1):
            current_position = temp_map[i][j]
            N = temp_map[i-1][j]
            E = temp_map[i][j+1]
            S = temp_map[i+1][j]
            W = temp_map[i][j-1]
            if (N == '0'):
                N_O = 0
            elif (N == 'X' or N == '-'):
                N_O = 1
            
            if (E == '0'):
                E_O = 0
            elif (E == 'X' or E == '-'):
                E_O = 1
            
            if (S == '0'):
                S_O = 0
            elif (S == 'X' or S == '-'):
                S_O = 1
            
            if (W == '0'):
                W_O = 0
            elif (W == 'X' or W == '-'):
                W_O = 1
            observation = str(N_O)+str(E_O)+str(S_O)+str(W_O)
            Observation_.append(observation)
        Observation_list_O.append(Observation_)
        
    
    Observation_space = ['0000', '1000', '0100', '0010', '0001','1100', '1010', '1001', 
                        '0110', '0101', '0011','0111', '1011', '1101', '1110','1111'] 
      
    #Create emission matrix O_, K*16, calculate P(observation|state)
    Observation_list_O = np.array(Observation_list_O)    
    Observation_list_flat = Observation_list_O.flatten()
    observation_code_prob_list = []
    for i in range(Observation_list_flat.shape[0]):
        observation = Observation_list_flat[i]
        N = observation[0]
        E = observation[1]
        S = observation[2]
        W = observation[3]
        observation_code_prob = []
        for obs_code in Observation_space:
            N_c = obs_code[0]
            E_c = obs_code[1]
            S_c = obs_code[2]
            W_c = obs_code[3]
        
            correct = 0
            if N == N_c:
                correct +=1
            if E == E_c:
                correct +=1
            if S == S_c:
                correct +=1
            if W == W_c:
                correct +=1
        
            obs_prob = math.pow((1-err),correct) * math.pow(err,(4-correct))
            observation_code_prob.append(obs_prob)
        observation_code_prob_list.append(observation_code_prob)    
    observation_code_prob_np = np.array(observation_code_prob_list)
    
    emission_matrix = np.delete(observation_code_prob_np, remove_obstacle_rows, axis=0)
    
    state_space = traverable_position
    
    observation_index = []
    for steps in Sequence_y:
        index = Observation_space.index(steps)
        observation_index.append(index)

    T_, O_, final_map_list_4, trellis_4 = Viterbi(state_space, transition_matrix, emission_matrix, Sequence_y) 



