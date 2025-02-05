<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>
# Lagrange 有限元求解 Poisson 方程 

## PDE 模型

给定区域 $\Omega\subset\mathbb R^d$, 其边界 $\partial \Omega = \Gamma_D \cup \Gamma_N
\cup \Gamma_R$

$$
-\Delta u = f, \quad\text{in }\Omega\\
$$

满足如下的边界条件

$$
u = g_D, \quad\text{on }\Gamma_D \\
$$

$$
\frac{\partial u}{\partial\boldsymbol n}  = g_N, \quad\text{on }\Gamma_N\\
$$

$$
\frac{\partial u}{\partial\boldsymbol n} + \kappa u = g_R, \quad\text{on }\Gamma_R
$$


## 连续与离散变分形式

方程两端分别乘以测试函数 $v \in H_{D,0}^1(\Omega)$, 则连续的弱形式可以写为

$$
(\nabla u,\nabla v)+<\kappa u,v>_{\Gamma_R} = (f,v)+<g_R,v>_{\Gamma_R}+<g_N,v>_{\Gamma_N}
$$

取一个 $N$ 维的有限维空间 $V_h = \operatorname{span}\{\phi_i\}_0^{N-1}$，其基函数向量记为

$$
\bm\phi = [\phi_0, \phi_1, \cdots, \phi_{N-1}],
$$

注意这 $\bm\phi$ 是行向量函数。

用 $V_h$ 替代无限维的空间 $H^1_{D,0}(\Omega)$, 从而把问题转化为**离散的弱形式**：求 

$$
u_h = \bm\phi\boldsymbol u = \sum_{i=0}^{N-1}u_i\phi_i\in V_h
$$

其中 $\boldsymbol u$ 是 $u_h$ 在基函数 $\bm\phi$ 下的坐标**列向量**, 即 

$$
\boldsymbol u=[u_0, u_1, \ldots, u_{N-1}]^T,
$$

$u_h$ 满足：

$$
\left(\nabla u_h, (\nabla \bm\phi)^T\right)+<\kappa u_h, \bm\phi^T>_{\Gamma_R}=
(f, \bm\phi^T)+<g_R, \bm\phi^T>_{\Gamma_R}+<g_N, \bm\phi^T>_{\Gamma_N},
$$

最终转化为如下离散代数系统

$$
(\boldsymbol A + \boldsymbol R)\boldsymbol u = \boldsymbol b + \boldsymbol b_N+ \boldsymbol b_R
$$

其中

$$
\boldsymbol A = \int_\Omega (\nabla \bm\phi)^T \nabla\bm\phi\mathrm d\boldsymbol x
\quad \boldsymbol R = \int_{\Gamma_R} \bm\phi^T \bm\phi\mathrm d \boldsymbol s
$$

$$
\boldsymbol b = \int_\Omega f\bm\phi^T\mathrm d \boldsymbol x,\quad
\boldsymbol b_N =  \int_{\Gamma_N} g_N\bm\phi^T\mathrm d \boldsymbol s,\quad
\boldsymbol b_R =  \int_{\Gamma_R} g_R\bm\phi^T\mathrm d \boldsymbol s
$$


## Lagrnage 有限元方法 

```python
from fealpy.decorator import cartesian
class CosCosData:
    def __init__(self):
        pass

    def domain(self):
        return np.array([0, 1, 0, 1])

    @cartesian
    def solution(self, p):
        """ The exact solution 
        Parameters
        ---------
        p : 


        Examples
        -------
        p = np.array([0, 1], dtype=np.float64)
        p = np.array([[0, 1], [0.5, 0.5]], dtype=np.float64)
        """
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        val = np.cos(pi*x)*np.cos(pi*y)
        return val # val.shape == x.shape

    @cartesian
    def source(self, p):
        """ The right hand side of Possion equation
        INPUT:
            p: array object,  
        """
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        val = 2*pi*pi*np.cos(pi*x)*np.cos(pi*y)
        return val

    @cartesian
    def gradient(self, p):
        """ The gradient of the exact solution 
        """
        x = p[..., 0]
        y = p[..., 1]
        pi = np.pi
        val = np.zeros(p.shape, dtype=np.float64)
        val[..., 0] = -pi*np.sin(pi*x)*np.cos(pi*y)
        val[..., 1] = -pi*np.cos(pi*x)*np.sin(pi*y)
        return val # val.shape == p.shape

    @cartesian
    def dirichlet(self, p):
        return self.solution(p)

    @cartesian
    def is_dirichlet_boundary(self, p):
        y = p[..., 1]
        return ( y == 1.0) | ( y == 0.0)
```
