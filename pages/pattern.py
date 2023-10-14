import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from itertools import combinations
import pandas as pd

st.set_page_config(page_title="Método Gráfico", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed")


@st.cache_data
def print_rangoli(size):
    letters = [chr(n) for n in range(ord("a"), ord("a")+size)]
    letters = letters[::-1]
    r = 2*(size+(size-1))-1
    x = 0
    f = True
    sr = ''
    for i in range(2*size-1):
        l2 = letters[0:x]
        s = '-'.join(letters[0:x+1]+l2[::-1])
        if x != len(letters)-1:
            s1 = ''.join(['-' for j in range((r-len(s))//2)])
            sr = sr + (s1+s+s1) + '\n'
        else:
            sr = sr + s + '\n'
        if x < len(letters)-1 and f:
            x = x + 1
        else:
            x = x - 1
            f = False
    return sr


s = st.slider("Tamaño del patrón", 0, 26, 3, 1, key="size", help="Tamaño del patrón")
if st.checkbox("Mostrar patrón en animación", key="anim"):
    import time
    #show the pattern in animation  from 0 to 26 an back in infinite loop
    it = 0
    while True:
        for i in range(0, 26):
            st.text(print_rangoli(it))
            time.sleep(0.1)
        if  it != 26 and it != 0:
            it = it + 1
        else:
            it = it - 1
st.text(print_rangoli(s))
