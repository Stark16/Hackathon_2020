import numpy as np


def activation_funct(Yin):
    if Yin > 0:
        return 1
    elif Yin == 0:
        return 0
    elif Yin < 0:
        return -1


def test(x1, x2):
    Yin = x1 * int(weights[0]) + x2 * int(weights[1]) + bias
    Y = activation_funct(Yin)
    print("Output:", Y)


ip_mat = np.matrix([
    [1, 1],
    [1, -1],
    [-1, 1],
    [-1, -1]
])

op_mat = np.matrix([
    [-1],
    [-1],
    [-1],
    [1]
])

weights = np.matrix([[0], [0]])
bias = 0
alpha = 1
epoch = 0
trained = 0

while trained != ip_mat.shape[0]:
    trained = 0

    for i in range(int(ip_mat.shape[0])):

        Yin = int(ip_mat[i] * weights + bias)
        Y = activation_funct(Yin)

        if Y != int(op_mat[i]):
            print("Weight Change Needed!")
            del_w1 = int(alpha * op_mat[i] * ip_mat[i, 0])
            weights[0] += del_w1
            del_w2 = int(alpha * op_mat[0] * ip_mat[i, 1])
            weights[1] += del_w2
            bias += int(alpha * op_mat[i])
            # print(weights)
        else:
            trained += 1

    epoch += 1
print("Network Trained!")
print("Epochs:", epoch)
print("Final Wights:", weights, "Bias:", bias)

choice = int(input("To test network press 1, To exit press 2"))

if choice == 1:
    x1 = int(input("Enter 1st bit:"))
    x2 = int(input("Enter 2nd Bit:"))
    test(x1, x2)
else:
    exit()
