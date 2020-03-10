import numpy as np


def activation_funct(Yin):
    if Yin > 0:
        return 1
    elif Yin == 0:
        return 0
    elif Yin < 0:
        return -1


ip_mat = np.matrix([
    [1, 1],
    [1, -1],
    [-1, 1],
    [-1, -1]
])

weights = np.matrix([[0], [0]])
bias = 0
alpha = 1
op_mat = np.matrix([
    [1],
    [-1],
    [-1],
    [-1]
])

epoch = 0
trained = 0
while trained != ip_mat.shape[0]:
    trained = 0

    for i in range(int(ip_mat.shape[0])):

        Yin = int(ip_mat[i]*weights + bias)
        Y = activation_funct(Yin)

        if Y != int(op_mat[i]):
            print("Weight Change Needed!")
            del_w1 = int(alpha * op_mat[i] * ip_mat[i, 0])
            weights[0] += del_w1
            del_w2 = int(alpha * op_mat[0] * ip_mat[i, 1])
            weights[1] += del_w2
            bias += int(alpha * op_mat[i])
            #print(weights)
        else:
            trained += 1

        print("Network O/P:", Yin)
        print("weights and Bias:", weights, bias)
        print("Iteration", i + 1)
    epoch += 1
print("Network Trained!")
print("Epochs:", epoch)
