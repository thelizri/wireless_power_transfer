import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#Dipole antenna RSSI
#0 degrees
x1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
y1 = [0, 40, 50, 75, 100, 150, 200, 250, 300, 350, 400]
z1 = [25.163, 13.886, 10.004, 4.336, 2.430, 1.150, 0.558, 0.280, 0.172, 0.167, 0.000]
#45 degrees 
x2 = [30, 50, 75, 100, 150, 250]
y2 = [30, 50, 75, 100, 150, 250]
z2 = [11.173, 3.137, 2.146, 0.401, 0.262, 0.155]
#90 degrees
x3 = [30, 40, 50, 75, 150, 200, 250]
y3 = [0, 0, 0, 0, 0, 0, 0]
z3 = [30.354, 12.065, 6.710, 3.620, 0.543, 0.744, 0.430 ]
# Plot the 3D points
ax.scatter(x1, y1, z1, c='r', marker='o')
ax.scatter(x2, y2, z2, c='b', marker='o')
ax.scatter(x3, y3, z3, c='g', marker='o')
plt.xlim(0, 400)
plt.ylim(0, 400)
# Set labels for axes
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
ax.set_zlabel('RSSI [mW]')
# Show the plot
plt.show()




#Dipole antenna Rate
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#Dipole antenna rate
#0 degrees
z1 = [3.259, 2.162, 1.701, 0.801, 0.441, 0.149, 0.078, 0.038, 0.011, 0.013, 0]
#45 degrees
z2 = [1.854, 0.572, 0.413, 0.057, 0.031, 0.012]
#90 degrees
z3 = [3.425, 2.030, 1.238, 0.682, 0.083, 0.113, 0.058]
# Plot the 3D points
ax.scatter(x1, y1, z1, c='r', marker='o')
ax.scatter(x2, y2, z2, c='b', marker='o')
ax.scatter(x3, y3, z3, c='g', marker='o')
plt.xlim(0, 400)
plt.ylim(0, 400)
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
ax.set_zlabel('Packet Rate [Hz]')
plt.show()



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#Patch antenna RSSI
#0 degrees
x1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
y1 = [50, 75, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
z1 = [39.555, 16.035, 8.595, 2.261, 1.329, 0.803, 0.719, 1.059, 0.583, 0.769, 0.864, 0.230, 0.290]
#45 degrees
x2 = [50, 75, 100, 150, 250]
y2 = [50, 75, 100, 150, 250]
z2 = [8.525, 3.423, 0.966, 0.455, 0.158]
#90 degrees
x3 = [50, 75, 100, 150, 200]
y3 = [0, 0, 0, 0, 0]
z3 = [8.249, 3.459, 0.815, 0.373, 0.588]
# Plot the 3D points
ax.scatter(x1, y1, z1, c='r', marker='o')
ax.scatter(x2, y2, z2, c='b', marker='o')
ax.scatter(x3, y3, z3, c='g', marker='o')
plt.xlim(0, 600)
plt.ylim(0, 600)
# Set labels for axes
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
ax.set_zlabel('RSSI [mW]')
# Show the plot
plt.show()

#Patch antenna Rate
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#Dipole antenna rate
#0 degrees
z1 = [4.286, 2.389, 1.466, 0.415, 0.226, 0.145, 0.121, 0.149, 0.097, 0.124, 0.138, 0.020, 0.042]
#45 degrees
z2 = [1.467, 0.622, 0.164, 0.074, 0.003]
#90 degrees
z3 = [1.417, 0.657, 0.138, 0.055, 0.090]
# Plot the 3D points
ax.scatter(x1, y1, z1, c='r', marker='o')
ax.scatter(x2, y2, z2, c='b', marker='o')
ax.scatter(x3, y3, z3, c='g', marker='o')
plt.xlim(0, 600)
plt.ylim(0, 600)
ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
ax.set_zlabel('Packet Rate [Hz]')
plt.show()

