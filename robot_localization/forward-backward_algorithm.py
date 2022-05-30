import csv
import math
import sys
import numpy as np


def forward_backward_(observations, states, start_probability, trans_probability, emm_probability, end_state):
    forward = list()  
    for i, observation_i in enumerate(observations):
        f_curr = dict()
        for st in states:
            if i == 0:
                prev_f_sum = start_probability[st]
            else:
                for s in states:
                    prev_f_sum = sum(f_prev[s]* trans_probability[st][s] for s in states)
            f_curr[st] = emm_probability[st][observation_i]* prev_f_sum
        forward.append(f_curr)
        f_prev=f_curr

    backward = list()
    for i, observation_i_ in enumerate(reversed( observations[1:] + (None,))):
        b_curr = dict()
        for state in states:
            if i == 0:
                b_curr[state] = trans_probability[state][end_state] 
            else:
                b_curr[state] = sum(emm_probability[l][observation_i_]* trans_probability[state][l]* b_prev[l] for l in states)
        backward.insert(0, b_curr)
        b_prev=b_curr

    fv = [list(i.values()) for i in forward]
    b = [list(i.values()) for i in backward]
    
    posterior = list()
    for i in range(len(observations)):
        sv = np.array(fv[i])* np.array(b[i])
        sv = np.divide(sv, np.sum(sv))
        posterior.append(sv)

    return posterior


if __name__ == "__main__":

    map_txt = sys.argv[1]
    
    #map_txt = 'A3_txt3'
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
    
    #Delete columns of 'X' in emission matrix 
    
    emission_matrix = np.delete(observation_code_prob_np, remove_obstacle_rows, axis=0)
    
    state_space = traverable_position
    
    state_space = [str(state[0])+'_'+str(state[1]) for state in state_space]
    
    start_probability = dict(zip(state_space, [1/len(traverable_position)] * (len(traverable_position))))
    
    #initial b all 1
    state_space_T = state_space + ['end']
    
    alist = np.repeat(1, transition_matrix.shape[0])
    
    transition_matrix_E = np.column_stack((transition_matrix, alist))
    
    t_dict_list = []
    for i in range(len(transition_matrix_E)):
        value = transition_matrix_E[i].tolist()
        key = state_space_T
        t_dict = dict(zip(key, value))
        t_dict_list.append(t_dict)
    
    transition_probability = dict(zip(state_space, t_dict_list))
    
    O_dict_list = []
    for i in range(len(emission_matrix)):
        value = emission_matrix[i]
        key = Observation_space
        o_dict = dict(zip(key, value))
        O_dict_list.append(o_dict)
        
    emission_probability = dict(zip(state_space, O_dict_list))

    end_state = 'end'
    
    states = state_space
    observations = tuple(Sequence_y)
    start_probability = start_probability
    trans_probability = transition_probability
    emm_probability = emission_probability
    end_state = end_state
    
    posterior = forward_backward_(observations, states, start_probability, trans_probability, emm_probability, end_state)
    
    final_map_list = []
    for state_map in posterior:
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



