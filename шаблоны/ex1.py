import numpy as np


matrix0 = np.array([[[4,14,-8],
[4,0,-8],
[4,14,0],
[4,0,0,3],
[12,14,-8,1],
[12,0,-8,3],
[12,14,0,1],
[12,0,0,3]],
[[0,1,1,0,1,0,0,0],
[0,0,0,1,0,1,0,0],
[0,0,0,1,0,0,1,0],
[0,0,0,0,0,0,0,1],
[0,0,0,0,0,0,1,0],
[0,0,0,0,1,0,0,1],
[0,0,0,0,0,0,0,1],
[0,0,0,0,0,0,0,0]]])
print(matrix0)

for i in range (2):
    if(i==0):
        for j in range(8):
            a=matrix0[i,j]
            for k in range (3):
                print(i,j,k, a[k])
    else:
        for j in range(8):
            a=matrix0[i,j]
            for k in range (8):
                print(i,j,k, a[k])

np.save('ex1', matrix0)
