import sys
from collections import Counter
from math import log
 

#sys.setrecursionlimit() method is used to set the maximum depth of the Python interpreter stack to the required limit. 
#This limit prevents any program from getting into infinite recursion, 
#Otherwise infinite recursion will lead to overflow of the C stack and crash the Python.

sys.setrecursionlimit(900)

class TreeNode:
    def __init__(self, input_data):
        self.attr = None
        self.label = None
        self.splitvalue = None
        self.left = None
        self.right = None
        self.info_content = self.information_content(input_data)
        
    def information_content(self, input_x):
        
        quality_list = ['5', '6', '7']
        count_quality = {'5': 0, '6': 0, '7': 0}
        
        ic = 0.0
        
        if len(input_x) == 0:
            return (ic, len(input_x))
            
        for r in range(len(quality_list)):
            count_quality[quality_list[r]] = input_x.count(quality_list[r])
            
            ct_qlt = float(count_quality[quality_list[r]])
            ct_ttl = float(len(input_x))
            c = ct_qlt/ct_ttl
            
            if (c == 0) or (c == 0.0):
                pass
            else: 
                ic = ic + (-(c*log(c,2)))
        return (ic, float(len(input_x)))

    def information_gain(self, x, data_t, x_attr, split_val):

        data_left_lbl = []
        for j in range(len(data_t[x_attr])):
            if data_t[x_attr][j] <= split_val:
                data_left_lbl.append(x[j][11])
                
        data_right_lbl = []
        for j in range(len(data_t[x_attr])):
            if data_t[x_attr][j] > split_val:
                data_right_lbl.append(x[j][11])
                
        ic_left, count_left = self.information_content(data_left_lbl)
        ic_right, count_right = self.information_content(data_right_lbl)
        ic , count_total = self.information_content(data_t[11])
        
        ic_left_gain = (float(count_left)/count_total)*ic_left
        
        ic_right_gain = (float(count_right)/count_total)*ic_right
       
        iContent_gain = ic - ic_left_gain - ic_right_gain
        
        return iContent_gain

    def chooseSplit(self, x):
        best_gain = 0
        best_attr = 0
        best_spiltval = 0
        
        for attr in range(11):
            x.sort(key=lambda x: x[attr])
            data_T = [[row[i] for row in x] for i in range(len(x[0]))]
            
            for i in range(len(x)-1):
                splitvalue = 0.5*(data_T[attr][i] + data_T[attr][i+1])
                gain = self.information_gain(x, data_T, attr, splitvalue)
                
                if gain > best_gain:
                    best_attr = attr
                    best_spiltval = splitvalue
                    best_gain = gain
                    
        return (best_attr, best_spiltval)

    def predict(n_node, test_x):
        while n_node.label == None:
            if test_x[n_node.attr] <= n_node.splitvalue:
                n_node = n_node.left
            else:
                n_node = n_node.right
        return n_node.label


    def DTL(self, data, min_leaf):
            
        if len(data) == 0:
            n = TreeNode(data)
            return n
        
        data_T = [[row[i] for row in data] for i in range(len(data[0]))]
        stop_split = False
        
        if len(data) <= min_leaf:
            stop_split = True

        for i in range(len(data_T)):
            if len(set(data_T[i])) == 1:
                stop_split = True
        
        if stop_split == True:
            n = TreeNode(data)
            quality_mode = mode_qlt(data_T[len(data_T)-1])
            if quality_mode == "There's no unique mode":
                n.label = 'undefined'
            else:
                n.label = quality_mode
            return n
        
        attr , splitvalue = self.chooseSplit(data)
        
        n = TreeNode(data)
        n.attr = attr
        n.splitvalue = splitvalue
        
        data.sort(key=lambda x: x[attr])
               
        data_T = [[row[i] for row in data] for i in range(len(data[0]))]
        
        data_left = []
        for j in range(len(data_T[n.attr])):
            if data_T[n.attr][j] <= splitvalue:
                data_left.append(data[j])
        
        data_right = []
        for j in range(len(data_T[n.attr])):
            if data_T[n.attr][j] > splitvalue:
                data_right.append(data[j])
        
        n.left = self.DTL(data_left, min_leaf)
        n.right = self.DTL(data_right, min_leaf)
        
        return n



def mode_qlt(data_list):
    count_dict = Counter(data_list)
    top_mode = count_dict.most_common(2) 
    if len(top_mode) < 2:
        return top_mode[0][0]
    if top_mode[0][1] == top_mode[1][1]:
        return "There's no unique mode"
    else:
        mode = top_mode[0][0]
    return mode



if __name__ == "__main__":

    train_txt = sys.argv[1]
    test_txt = sys.argv[2]
    minlf_txt = sys.argv[3]
    min_leaf = int(minlf_txt)
    
    #train_txt = 'train_txt'
    #test_txt = 'test_txt gradescope.txt'
    #min_leaf = int(30)

    f = open(train_txt,'r')

    f_acid = []
    v_acid = []
    c_acid = []
    res_sugar = []
    chlorides = []
    fs_dioxide = []
    ts_dioxide = []
    density = []
    pH = []
    sulphates = []
    alcohol = []
    quality = []

    next(f)

    for line in f:
        row = line.split()
        f_acid.append(float(row[0]))
        v_acid.append(float(row[1]))
        c_acid.append(float(row[2]))
        res_sugar.append(float(row[3]))
        chlorides.append(float(row[4]))
        fs_dioxide.append(float(row[5]))
        ts_dioxide.append(float(row[6]))
        density.append(float(row[7]))
        pH.append(float(row[8]))
        sulphates.append(float(row[9]))
        alcohol.append(float(row[10]))
        quality.append(str(row[11]))

    trainx_T = list([f_acid, v_acid, c_acid, res_sugar, chlorides, fs_dioxide, ts_dioxide, density, pH, sulphates, alcohol, quality])
    
    train_x = [[row[i] for row in trainx_T] for i in range(len(trainx_T[0]))]
    
    f.close()
    
    root = TreeNode(train_x)
    
    n = root.DTL(train_x, min_leaf)
    
    h = open(test_txt,'r')
    next(h)

    test_x_ = []
    for line in h:
        test_x = line.split()
        test_row = [float(i) for i in test_x]
        if len(test_row)!= 0:
            test_x_.append(test_row)

    result = []
    for i in range(len(test_x_)):
        try:
            test_y = n.predict(test_x_[i])
            result.append(test_y)
            print(test_y)
        except:
            None    