# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 13:38:24 2022

@author: Philipp Spelten
"""

from plots import update_plot
from data import check_data, update_data, update_data_static
from printing import bmatrix, print_equations, latex_to_md
from eigenvalues_calculations import reduce_matrix, calculate_forces, calculate_stiffness_matrix, \
    calculate_node_masses_and_member_lengths, construct_mass_matrix
from sidebars import buttons_top, sidebars
from layout import titlepage, debug_options, debug_stuff

import numpy as np

import streamlit as st
from streamlit import session_state as state
from streamlit_plotly_events import plotly_events

###############################################################################
# TO-DO
###############################################################################

# 1. Calculate Energies P, D, T
# 2. Construct Stiffness Matrix K
# 3. Two results: Deformation (P+D = min) and Eigenvalues (Mx_ddot + Kx = 0)

titlepage()

debug_options()

buttons_top()

sidebars()

###############################################################################
# CALCULATIONS
###############################################################################

state.gravity = True
state.rho = 7850e-9  # kg/mm^3
state.gridsize = 100  # mm
state.d = 1  # mm
state.A = state.d * np.pi  # mm^2
state.E = 210000  # N/mm^2

calculate_node_masses_and_member_lengths()

check_data()

construct_mass_matrix()
state.M.round(state.decimals)
state.M = reduce_matrix(state.M)

calculate_stiffness_matrix()
state.M.round(state.decimals)
st.markdown('$K_{whole} = ' + bmatrix(state.K, ' 0 ', 'b') + '$')
state.K = reduce_matrix(state.K)

calculate_forces()
state.rhs = reduce_matrix(state.rhs)

st.write('node_masses: ' + str(state.node_masses))
st.write('member_lengths: ' + str(state.member_lengths))
st.write('member_angles: ' + str(state.member_angles))

st.markdown('$M = ' + bmatrix(state.M, ' 0 ', 'b') + '$')
st.markdown('$K = ' + bmatrix(state.K, ' 0 ', 'b') + '$')

st.markdown('$\\text{Forces} = ' + bmatrix(state.f_ext.round(state.decimals), ' 0 ', 'b') + '$')

state.displacements = np.zeros([2 * len(state.connected_nodes), 1])
st.markdown(
    print_equations(
        state.K, state.M, state.rhs, state.displacements,
        len(state.members), len(state.support),
        state.decimals, state.textsize, len(state.connected_nodes),
        state.onlyviz, state.showzeros, state.connected_nodes, state.rods_per_node))

state.left_side = state.K  # [2:,2:]
state.right_side = -np.dot(state.M, state.rhs)  # [2:]
state.displacements = np.linalg.solve(state.left_side, state.right_side)
st.markdown('$\\text{displacements}: ' + bmatrix(state.displacements.round(4), ' 0 ', 'b') + '\\text{mm}$')

state.m_to_minus_half = np.power(np.sqrt(state.M), -1)
state.m_to_minus_half[state.m_to_minus_half == np.inf] = 0
state.ev_problem = np.dot(np.dot(state.m_to_minus_half, state.K), state.m_to_minus_half)

state.w, state.v = np.linalg.eig(state.ev_problem)

st.markdown('$w = ' + bmatrix([state.w.round(4)], ' 0 ', 'b') + '$')
st.markdown('$v = ' + bmatrix(state.v.round(4), ' 0 ', 'b') + '$')

if 'matrix' not in state:
    update_data_static()
if 'fig' not in state:
    update_plot()

st.plotly_chart(state.fig)

content = """<p><a href='#' id='Link 1'>First link</a></p>
<p><a href='#' id='Link 2'>Second link</a></p>
<a href='#' id='Image 1'><img width='20%' src='https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=200'></a>
<a href='#' id='truss1'><img width='20%' src='https://github.com/PhiSpel/spielbeispiel-lgls/blob/master/images/truss1.png?raw=true'></a>
"""
