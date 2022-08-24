from data import update_data
from state_stuff import setup_session_states
import streamlit as st
from streamlit import session_state as state
import numpy as np
from plots import update_plot


def titlepage():
    st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

    setup_session_states()

    st.title("Internal forces of a rod structure")

    with st.expander('Explanation'):
        st.write(
            "Here, you can see a rod system with supports and forces. Below, you see the linear system of equations that is solved to calculate the iternal forces of the rods.  \n "
            + "  \n "
            + "Select 'Interactive mode' to be able to change the rod structure.  \n "
            + "Delete rods via the orange 'x' markers. Add rods by klicking both nodes after each other (you may need to hide the rod-markers by klicking on 'x members for deselection' in the legend). Below the plot, you get information about which node(s) you chose.  \n "
            + "Add or delete supports or forces in the sidebar.  \n "
            + "You can input all forces, supports and members in bulk by choosing 'Use vectors as input' in the sidebar.  \n "
            + "  \n "
            + "To display your changes, klick 'Update plot and matrix'.  \n "
            + "To update your calculations, click 'Update calculations' and deselect 'Interactive mode'.  \n "
            + "  \n "
            + "Keep in mind that your rod structure must consist of triangles to yield sensible results!  \n "
        )


###############################################################################
# DEBUG OPTIONS
###############################################################################

def debug_options():
    state.debug = False  # st.sidebar.checkbox(label="show development stuff")

    if state.debug:
        st.sidebar.number_input(label="precision of print",
                                min_value=0,
                                max_value=5,
                                value=2,
                                key='decimals')
        # textsize = st.sidebar.selectbox(label="font size of formula", options=[r'\normalsize',r'\small',r'\footnotesize',r'\scriptsize',r'\tiny'],index=3)
    else:
        state.decimals = 2
        # textsize = r'\scriptsize'

    if not state.debug:
        if 'support' not in state:
            state.support = np.array([
                [0, 0], [0, 90], [20, 90]
            ])
        if 'f_ext' not in state:
            state.f_ext = np.array([
                [5, -90, 10], [12, 180, 10], [15, -90, 15]
            ])


def debug_stuff():
    if 'matrix' not in state: update_data()
    if 'fig' not in state: update_plot()

    if state.onlyviz:
        if state.onlyviz: update_plot()
        if state.apply_changes: update_plot()
    elif state.calculate:
        if state.issquare:
            update_data()
            update_plot()
        else:
            st.warning(
                "I am having issues solving your system. Return to interactive mode to check whether your system is solvable. If you need to reset, press 'Reste data'.")
            state.onlyviz = True
            update_plot()
