#!/usr/bin/python3

import matplotlib.pyplot as plt
import scipy.optimize
import jax.numpy as np
import jax

# Problem setup:
#
# Start point at 0, port at 1, submarines in the middle
# Submarines travel at unit speed, we travel at speed alpha
# x-axis is horizontal, y-axis is vertical
#
# Layout:
# 0 ----- d ----- 2d ----- ... ----- kd ----- ... ----- Nd ..... 1
#

# Number of points:
TIMESTEPS = 100

# Number of subs:
N = 10

# Derived parameters
d = 1 / (N + 1)
T = d
t = np.linspace(0, T, TIMESTEPS)
dt = t[1] - t[0]
P = np.stack([np.array(list(range(1, N + 1))) * d, np.zeros(N)], axis=-1)


def unpack(x):
    return np.reshape(x, (TIMESTEPS, 2))


def pack(x):
    return np.reshape(x, (2 * TIMESTEPS,))


# Cost: L2 on distances between sequential points
@jax.jit
def C(x):
    x = unpack(x)
    return np.sum((x[:-1] - x[1:])**2)
J = jax.jacobian(C)


# Max speed constraint
@jax.jit
def g_vel(x, alpha):
    x = unpack(x)
    return (dt * alpha)**2 - np.sum((x[:-1] - x[1:])**2, axis=1)
Jg_vel = lambda alpha: jax.jacobian(lambda x: g_vel(x, alpha))
c_vel = lambda alpha: {'type': 'ineq', 'fun': lambda x: g_vel(x, alpha), 'jac': Jg_vel(alpha)}


# Endpoint constraint (start at (0, 0), end at (1, 0))
@jax.jit
def g_endpoints(x):
    x = unpack(x)
    return np.array([np.sum(x[0]**2), np.sum((x[-1] - np.array([1, 0]))**2)])
Jg_endpoints = jax.jacobian(g_endpoints)
c_endpoints = {'type': 'eq', 'fun': g_endpoints, 'jac': Jg_endpoints}


# Non-detection constraint
@jax.jit
def g_sub(x):
    x = unpack(x)
    np.tile(x, (N, 1, 1))
    return np.reshape(np.sum((P[:, np.newaxis, :] - x)**2, axis=-1) - t**2, (N * TIMESTEPS,))
Jg_sub = jax.jacobian(g_sub)
c_sub = {'type': 'ineq', 'fun': g_sub, 'jac': Jg_sub}


def arclength(x):
    x_spline = scipy.interpolate.CubicSpline(t, x[:, 0])
    y_spline = scipy.interpolate.CubicSpline(t, x[:, 1])
    results = scipy.integrate.quad(
            lambda t: (x_spline(t, 1)**2 + y_spline(t, 1)**2)**0.5, 0, T)
    print(results)
    return results[0]


def optimize(x0):
    result = scipy.optimize.minimize(
            C,
            pack(x0),
            jac=J,
            constraints=[c_vel(alpha), c_endpoints, c_sub],
            method='SLSQP')
    print('Optimized:')
    print(result)
    x = unpack(result.x)
    return x


x0 = np.stack([np.linspace(0, 1, TIMESTEPS),
               np.ones(TIMESTEPS)], axis=-1)
alpha = N + 1.5 + 1
x = optimize(x0)
rect_arclength = np.sum(np.sum((x[1:] - x[:-1])**2, axis=1)**0.5) / T
print(rect_arclength)
print(arclength(x) / T)
plt.plot(x[:, 0], x[:, 1])
plt.show()
