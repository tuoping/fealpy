import numpy as np
import matplotlib.pyplot as plt
from fealpy.mg.DarcyForchheimerP0P1 import DarcyForchheimerP0P1
from fealpy.tools.show import showmultirate, show_error_table
from fealpy.pde.darcy_forchheimer_2d import LShapeRSinData
from fealpy.pde.darcy_forchheimer_2d import DarcyForchheimerdata1

box = [-1,1,-1,1]
mu = 1
rho = 1
beta = 10
alpha = 1/beta
tol = 1e-6
maxN = 2000
p = 1
n = 2

pde = LShapeRSinData (mu, rho, beta, alpha, tol, maxN)
mesh = pde.init_mesh(n)
integrator1 = mesh.integrator(p+2)
integrator0 = mesh.integrator(p+1)

errorType = ['$|| u - u_h||_0$','$|| p - p_h||$', '$||\\nabla p - \\nabla p_h||_0$']

maxit = 4
errorMatrix = np.zeros((len(errorType), maxit), dtype=np.float)
Ndof = np.zeros(maxit,dtype = np.int)


for i in range(maxit):
    fem = DarcyForchheimerP0P1(pde, mesh, integrator0, integrator1)
    fem.solve()
    
    NC = mesh.number_of_cells()
    NN = mesh.number_of_edges()
    Ndof[i] = 2*NC+NN
    errorMatrix[0, i] = fem.get_uL2_error()
    errorMatrix[1, i] = fem.get_pL2_error()
    errorMatrix[2, i] = fem.get_H1_error()
    print('i',i)

    if i < maxit -1:
        mesh.uniform_refine()

show_error_table(Ndof, errorType, errorMatrix)
showmultirate(plt, 0, Ndof, errorMatrix, errorType)
plt.show()

