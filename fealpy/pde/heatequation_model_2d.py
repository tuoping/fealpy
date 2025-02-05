import numpy as np

class SinSinExpData:
    """

    u_t - c*\Delta u = f

    c = 1/16
    u(x, y, t) = sin(2*PI*x)*sin(2*PI*y)*exp(-t)

    domain = [0, 1]^2


    """
    def __init__(self):
        self.diffusionCoefficient = 1/16

    def domain(self):
        return [0, 1, 0, 1]

    def init_value(self, p):
        return self.solution(p, 0.0)

    def solution(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        u = np.sin(2*pi*x)*np.sin(2*pi*y)*np.exp(-t)
        return u
    
    def diffusion_coefficient(self, p):
        return self.diffusionCoefficient

    def source(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        k = self.diffusionCoefficient
        rhs = (-1+k*8*pi**2)*np.sin(2*pi*x)*np.sin(2*pi*y)*np.exp(-t)
        return rhs

    def dirichlet(self, p, t):
        return self.solution(p,t)

    def is_dirichlet_boundary(self, p):
        eps = 1e-14 
        return (p[..., 0] < eps) | (p[..., 1] < eps) | (p[..., 0] > 1.0 - eps) | (p[..., 1] > 1.0 - eps)


class SinCosExpData:
    def __init__(self):
        self.diffusionCoefficient = 1/16

    def init_value(self, p):
        return self.solution(p, 0.0)

    def diffusion_coefficient(self):
        return self.diffusionCoefficient 

    def solution(self, p, t):
        """ The exact solution 
        """
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        u = np.sin(pi*x)*np.cos(pi*y)*np.exp(-pi**2/8*t)
        return u

    def source(self, p, t):
        """ The right hand side of Possion equation
        INPUT:
            p: array object, N*2 
        """
        return 0.0

    def dirichlet(self, p, t):
        """ Dilichlet boundary condition
        """
        return 0.0 

    def neuman(self, p, t):
        """ Neuman boundary condition
        """
        return 0.0

    def is_dirichlet_boundary(self, p):
        eps = 1e-14 
        return (p[..., 0] < eps) | (p[..., 0] > 1.0 - eps) 

    def is_neuman_boundary(self, p):
        eps = 1e-14
        return (p[..., 1] < eps) | (p[..., 1] > 1.0 - eps)

class ExpCosData:
    """

    u_t - c*\Delta u = f

    c = 1
    u(x, y, t) = exp(-a((x-0.5)^2 + (y-0.5)^2))*cos(2*pi*t)

    domain = [0, 1]^2


    """
    def init_mesh(self, n=1, meshtype='tri'):
        node = np.array([
            (0, 0),
            (1, 0),
            (1, 1),
            (0, 1)], dtype=np.float64)

        if meshtype == 'tri':
            cell = np.array([(1, 2, 0), (3, 0, 2)], dtype=np.int_)
            mesh = TriangleMesh(node, cell)
            mesh.uniform_refine(n)
            return mesh
        elif meshtype == 'quadtree':
            cell = np.array([(0, 1, 2, 3)], dtype=np.int_)
            mesh = Quadtree(node, cell)
            mesh.uniform_refine(n)
            return mesh
        elif meshtype == 'tritree':
            cell = np.array([(1, 2, 0), (3, 0, 2)], dtype=np.int_)
            mesh = TriangleMesh(node, cell)
            mesh.uniform_refine(n)
            node = mesh.entity('node')
            cell = mesh.entity('cell')
            mesh = Tritree(node, cell)
            return mesh
        else:
            raise ValueError("I don't know the meshtype %s".format(meshtype))



    def __init__(self):
        self.diffusionCoefficient = 1
        self.a = 100

    def domain(self):
        return [0, 1, 0, 1]

    def init_value(self, p):
        return self.solution(p, 0.0)

    def solution(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        a = self.a
        u = np.exp(-a*((x - 0.5)**2 + (y - 0.5)**2))*np.cos(2*pi*t)
        return u

    def u_t(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        a = self.a
        u = np.exp(-a*((x - 0.5)**2 + (y - 0.5)**2))*np.sin(2*pi*t)*(-2*pi)
        return u

    def u_x(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        a = self.a
        u = -2*a*(x - 0.5)*np.exp(-a*((x - 0.5) **
                                      2 + (y - 0.5)**2))*np.cos(2*pi*t)
        return u

    def u_y(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        a = self.a
        u = -2*a*(y - 0.5)*np.exp(-a*((x - 0.5) **
                                      2 + (y - 0.5)**2))*np.cos(2*pi*t)
        return u

    def u_xx(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        a = self.a
        u = (-2*a*np.exp(-a*((x - 0.5)**2 + (y - 0.5)**2)) + 4*a*a *
             (x - 0.5)**2*np.exp(-a*((x - 0.5)**2 + (y - 0.5)**2)))*np.cos(2*pi*t)
        return u

    def u_yy(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        a = self.a
        u = (-2*a*np.exp(-a*((x - 0.5)**2 + (y - 0.5)**2)) + 4*a*a *
             (y - 0.5)**2*np.exp(-a*((x - 0.5)**2 + (y - 0.5)**2)))*np.cos(2*pi*t)
        return u

    def diffusion_coefficient(self, p):
        return self.diffusionCoefficient

    def source(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        k = self.diffusionCoefficient
        rhs = self.u_t(p, t) - k*(self.u_xx(p, t) + self.u_yy(p, t))
        return rhs

    def gradient(self, p, t):
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        val = np.zeros(p.shape, dtype=np.float64)
        val[..., 0] = self.u_x(p, t)
        val[..., 1] = self.u_y(p, t)
        return val

    def dirichlet(self, p, t):
        return self.solution(p, t)

    def is_dirichlet_boundary(self, p):
        eps = 1e-14
        return (p[..., 0] < eps) | (p[..., 1] < eps) | (p[..., 0] > 1.0 - eps) | (p[..., 1] > 1.0 - eps)


