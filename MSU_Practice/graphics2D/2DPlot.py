from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np


fig = plt.figure()

ax = fig.gca(projection='3d')

'''
X = np.arange(-10, 10, 0.1)
Y = np.arange(-10, 10, 0.1)
X, Y = np.meshgrid(X, Y)
Z = X**2 - Y**2
'''

X=np.loadtxt("X.txt")
Y=np.loadtxt("Y.txt")
Z=np.loadtxt("Z.txt")
# X, Y, Z - матрицы. X из одинаковых строк, Y из одинаковых столбцов, Z из строк, в каждой из которых y фиксируется, а x бегает.



surf = ax.plot_surface(X, Y, Z, color="g")

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_zlim(-110, 110)

fig.suptitle("Чипсы Принглс", fontsize=12)
