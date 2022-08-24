# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:56:07 2022

@author: phili
"""

###############################################################################
# SIDEBARS
###############################################################################

import streamlit as st
from streamlit import session_state as state
from state_stuff import reset_data, new_array, new_force_input, new_support_input, new_force_delete, new_support_delete, update_all


def latex_to_md(textsize):
    string = r'''<font size="'''
    if textsize == r'\tiny':
        string += '1'
    elif textsize == r'\scriptsize':
        string += '2'
    elif (textsize == r'\footnotesize') | (textsize == r'\small'):
        string += '3'
    elif textsize == r'\normalsize':
        string += '4'
    string += r'''"> '''
    return string


def sidebars():
    onlyviz, apply_changes = state.onlyviz, state.apply_changes
    # if onlyviz:
    #     st.write('Mind the admonitions below the plot about requirements to the rod system.')

    st.sidebar.selectbox(label="font size of formula",
                         options=[r'\normalsize', r'\small', r'\footnotesize', r'\scriptsize', r'\tiny'],
                         index=3,
                         key='textsize')

    state.textsize_md = latex_to_md(state.textsize)

    st.sidebar.selectbox(label="show zeros as...",
                         options=[' 0 ', ' '],
                         key='showzeros')

    if onlyviz:
        st.sidebar.checkbox(
            "Use vectors as input. (klick 'Update plot' once to initialize)",
            key='vectorinput')
        if state.vectorinput:
            st.sidebar.text_input(label="members",
                                  help="[node,angle]",
                                  value='''[0,6],[0,5],[6,5],[5,10],[6,10],[6,12],[12,10],[10,15],[10,16],[16,15],[12,16],[15,20],[16,20]''',
                                  key='members_str',
                                  on_change=new_array('members'))

            st.sidebar.text_input(label="support",
                                  help="[node,angle]",
                                  value='[0, 0],[0, 90],[20, 90]',
                                  key='support_str',
                                  on_change=new_array('support'))

            st.sidebar.text_input(label="external forces",
                                  help="[node,angle,force]",
                                  value='[5,-90,10],[12,180,10],[15,-90,15]',
                                  key='f_ext_str',
                                  on_change=new_array('f_ext'))

        else:
            st.sidebar.text_input(label="add external forces",
                                  help="node angle force",
                                  placeholder="e.g. '6 90 10'",
                                  on_change=new_force_input(),
                                  key='new_f_ext_str')

            st.sidebar.text_input(label="add supports",
                                  help="node angle",
                                  placeholder="e.g. '10 90'",
                                  on_change=new_support_input(),
                                  key='new_support_str')

            f_ext_text = ''
            for i in range(len(state.f_ext)):
                f_ext_text += str(i) + ': ' + str(state.f_ext[i])
                if i < len(state.f_ext) - 1:
                    f_ext_text += ', '
            support_text = ''
            for i in range(len(state.support)):
                support_text += str(i) + ': ' + str(state.support[i])
                if i < len(state.support) - 1:
                    support_text += ', '

            st.sidebar.markdown(state.textsize_md + 'Currently, you have these forces: '
                                + f_ext_text + '. Would you like to delete one? '
                                + r''' </font>''', unsafe_allow_html=True)
            st.sidebar.text_input(label='remove external forces',
                                  placeholder="IDs start at 0!",
                                  on_change=new_force_delete(),
                                  key='force_delete_str')

            st.sidebar.markdown(state.textsize_md + 'Currently, you have these supports: '
                                + support_text + '. Would you like to delete one? '
                                + r''' </font>''', unsafe_allow_html=True)
            st.sidebar.text_input(label='remove supports',
                                  placeholder="IDs start at 0!",
                                  on_change=new_support_delete(),
                                  key='support_delete_str')

            if apply_changes:
                update_all(state.removed_members, state.new_members, state.removed_forces, state.removed_supports,
                           state.new_f_ext, state.new_supports)
                state.selected_nodes = []


###############################################################################
# BUTTONS
###############################################################################

def buttons_top():
    col1, col2, col3, col4 = st.columns(4)  # ([1,1,1,1,0])
    with col1:
        reset = st.button('Reset data')
    if reset:
        reset_data()
    with col2:
        st.checkbox("Interactive mode", key='onlyviz')
    with col3:
        st.button(
            'Update plot and matrix',
            key='apply_changes')  # ,on_click=update_members(state.removed_members,state.new_members))
    with col4:
        st.button('Update calculations', key='calculate')
        if state.calculate:
            state.onlyviz = False
