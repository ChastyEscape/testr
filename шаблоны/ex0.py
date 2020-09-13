import numpy as np

#matrixs = np.zeros((4,4))
#matrixs[0]=[0,1,1,1]
#matrixs[1]=[0,0,1,0]
#matrixs[2]=[0,0,0,1]
#matrixs[3]=[0,1,0,0]

matrix0 = np.array([[[4,18,-8],
[10,0,0],
[3,0,-24],
[-6,0,0]],
[[0,1,1,1],
[0,0,1,0],
[0,0,0,1],
[0,1,0,0]]])

print(matrix0)

for i in range (2):
    if(i==0):
        for j in range(4):
            a=matrix0[i,j]
            for k in range (3):
                print(i,j,k, a[k])
    else:
        for j in range(4):
            a=matrix0[i,j]
            for k in range (4):
                print(i,j,k, a[k])

np.save('matrix0', matrix0)
