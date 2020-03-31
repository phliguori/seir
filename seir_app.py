import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import streamlit as st


def seir(y, t, k_transmission, k_recovery, k_infectious, k_incubation):
    S_t = y[0]       # Susceptable
    E_t = y[1]       # Exposed
    I_t = y[2]       # Infected
    R_t = y[3]       # Recovered

    dsdt = - (k_transmission * k_infectious) * I_t * S_t
    dedt = (k_transmission * k_infectious) * I_t * S_t - (1 / k_incubation) * E_t
    didt = (1 / k_incubation) * E_t - (1 / (k_recovery + k_infectious)) * I_t
    drdt = (1 / (k_recovery + k_infectious)) * I_t

    return [dsdt, dedt, didt, drdt]


# initial disease parameters
transmission = st.slider('Transmission rate (hab/day)', min_value=0., max_value=1., value=0.75)
recovery = st.slider('Recovery period (days)', min_value=0., max_value=8.0, value=3.0)
infection = st.slider('Infectious period (days)', min_value=0., max_value=8., value=2.9)
incubation = st.slider('Incubation period (day)', min_value=0., max_value=8., value=5.2)


# initial conditions
N = st.sidebar.slider('Population (k hab)', min_value=int(500), max_value=int(300e3), value=int(210e3), step=int(500))

# S_0 = st.sidebar.slider('Initial susceptible pop. (%)', min_value=0., max_value=4., value=1.25)                        # Initial susceptable population
E_0 = st.sidebar.slider('Initially exposed population(%)', min_value=0., max_value=2., value=0.05, step=0.05) / 100       # Initial exposed population
I_0 = st.sidebar.slider('Initially infected population (%)',  min_value=0., max_value=1., value=0.0, step=0.05) / 100    # Initial infected population
R_0 = st.sidebar.slider('Initially recovered population (%)',  min_value=0., max_value=100., value=0.0, step=0.5) / 100    # Initial recovered population
S_0 = 1 - (E_0 + I_0 + R_0) 

y_0 = [S_0, E_0, I_0, R_0]     # initial condition vector

t = np.linspace(0, 60, 180)     # time grid

# solve the DEs
soln = odeint(seir, y_0, t, args=(transmission, recovery, infection, incubation))
S = N * soln[:, 0]
E = N * soln[:, 1]
I = N * soln[:, 2]
R = N * soln[:, 3]

# # plot results
plt.rcParams['figure.figsize'] = 10, 8
plt.figure()
plt.plot(t, S, label='Susceptable')
plt.plot(t, E, label='Exposed')
plt.plot(t, I, label='Infected')
plt.plot(t, R, label='Recovered')
plt.xlabel('Days from outbreak')
plt.ylabel('Population')
plt.title('SEIR Model: COVID-19')
plt.legend(loc=0)

# plt.show()
st.pyplot()
