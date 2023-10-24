import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from itertools import combinations
import pandas as pd
from streamlit.components.v1 import html
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, add_page_title
#Autor: Sergio Demis Lopez Martinez, 2023.


# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("Main.py", "Inicio", ":comet:"),
        Page("pages/Home.py", "Home", "🏠"),
        Page("pages/grafico.py", "Metodo Grafico", ":chart_with_upwards_trend:"),
        Page("pages/simplexmatrix.py","Simplex Matricial", ":diamond_shape_with_a_dot_inside:"),
        Page("pages/tableusimplex.py","Tableau Simplex", ":abacus:"),
    ]
)
#set the configuration
st.set_page_config(page_title="Método Gráfico", page_icon=":snowflake:", layout="wide", initial_sidebar_state="collapsed")
#.....................................Data Input.............................................

st.markdown(
r'''
<style>
body{
background-color: #e5e5f7;
opacity: 0.8;
background-image:  linear-gradient(30deg, #444cf7 12%, transparent 12.5%, transparent 87%, #444cf7 87.5%, #444cf7), linear-gradient(150deg, #444cf7 12%, transparent 12.5%, transparent 87%, #444cf7 87.5%, #444cf7), linear-gradient(30deg, #444cf7 12%, transparent 12.5%, transparent 87%, #444cf7 87.5%, #444cf7), linear-gradient(150deg, #444cf7 12%, transparent 12.5%, transparent 87%, #444cf7 87.5%, #444cf7), linear-gradient(60deg, #444cf777 25%, transparent 25.5%, transparent 75%, #444cf777 75%, #444cf777), linear-gradient(60deg, #444cf777 25%, transparent 25.5%, transparent 75%, #444cf777 75%, #444cf777);
background-size: 20px 35px;
background-position: 0 0, 0 0, 10px 18px, 10px 18px, 0 0, 10px 18px;
}
[data-testid="collapsedControl"] {
        display: none
    }
.css-wwfog0 {
  position: fixed;
  top: 0px;
  left: 0px;
  right: 0px;
  height: 2.875rem;
  background: rgb(216, 255, 152);
  outline: none;
  z-index: 999990;
  display: none;
}
</style>
''', unsafe_allow_html=True)





html(r'''
<!DOCTYPE html>
<html>
<head>
    <style>
        *,
        *::before,
        *::after {
  box-sizing: border-box;
        }

        :root {
          --color-primary: #f6aca2;
          --color-secondary: #f49b90;
          --color-tertiary: #f28b7d;
          --color-quaternary: #f07a6a;
          --color-quinary: #ee6352;
          /*
          --color-primary: #5192ED;
          --color-secondary: #69A1F0;
          --color-tertiary: #7EAEF2;
          --color-quaternary: #90BAF5;
          --color-quinary: #A2C4F5;
          */
        }

        body {
          min-height: 100vh;
          font-family: canada-type-gibson, sans-serif;
          font-weight: 300;
          font-size: 1.25rem;
          display: flex;
          flex-direction: column;
          justify-content: center;
          overflow: hidden;
          background-color: transparent;
        }

        .content {
          display: fixed;
          align-content: center;
          justify-content: center;
        }

        .text_shadows {
          text-shadow: 3px 3px 0 var(--color-secondary), 6px 6px 0 var(--color-tertiary),
            9px 9px var(--color-quaternary), 12px 12px 0 var(--color-quinary);
          font-family: bungee, sans-serif;
          font-weight: 400;
          text-transform: uppercase;
          font-size: calc(2rem + 5vw);
          text-align: center;
          margin: 0;
          color: var(--color-primary);
          //color: transparent;
          //background-color: white;
          //background-clip: text;
          animation: shadows 1.2s ease-in infinite, move 1.2s ease-in infinite;
          letter-spacing: 0.4rem;
        }

        @keyframes shadows {
          0% {
            text-shadow: none;
          }
          10% {
            text-shadow: 3px 3px 0 var(--color-secondary);
          }
          20% {
            text-shadow: 3px 3px 0 var(--color-secondary),
              6px 6px 0 var(--color-tertiary);
          }
          30% {
            text-shadow: 3px 3px 0 var(--color-secondary),
              6px 6px 0 var(--color-tertiary), 9px 9px var(--color-quaternary);
          }
          40% {
            text-shadow: 3px 3px 0 var(--color-secondary),
              6px 6px 0 var(--color-tertiary), 9px 9px var(--color-quaternary),
              12px 12px 0 var(--color-quinary);
          }
          50% {
            text-shadow: 3px 3px 0 var(--color-secondary),
              6px 6px 0 var(--color-tertiary), 9px 9px var(--color-quaternary),
              12px 12px 0 var(--color-quinary);
          }
          60% {
            text-shadow: 3px 3px 0 var(--color-secondary),
              6px 6px 0 var(--color-tertiary), 9px 9px var(--color-quaternary),
              12px 12px 0 var(--color-quinary);
          }
          70% {
            text-shadow: 3px 3px 0 var(--color-secondary),
              6px 6px 0 var(--color-tertiary), 9px 9px var(--color-quaternary);
          }
          80% {
            text-shadow: 3px 3px 0 var(--color-secondary),
              6px 6px 0 var(--color-tertiary);
          }
          90% {
            text-shadow: 3px 3px 0 var(--color-secondary);
          }
          100% {
            text-shadow: none;
          }
        }

        @keyframes move {
          0% {
            transform: translate(0px, 0px);
          }
          40% {
            transform: translate(-12px, -12px);
          }
          50% {
            transform: translate(-12px, -12px);
          }
          60% {
            transform: translate(-12px, -12px);
          }
          100% {
            transform: translate(0px, 0px);
          }
        }
    </style>
</head>
<body>
    <div class="content">
        <h2 class="text_shadows">Optimización 1</h2>
    </div>
</body>
</html>
''',height=200)


st.markdown(r'''
<style>
button[kind="primary"] {
  display: block;
  margin: 0 auto;
  padding-bottom: 10px;
  background: #7986cb;
  font-size: 20px;
  color: white;
  border-radius: 7px;
  box-shadow: 0 7px 0px #3f51b5;
  transition: all .2s;
  padding: 20px 25px;
  top: 0;
  cursor: pointer;
}
button[kind="primary"]:active {
  top: 3px;
  box-shadow: 0 2px 0px #3f51b5;
  transition: all .2s;

}
</style>
''', unsafe_allow_html=True)

if st.button("Inicio",type='primary'):
  switch_page('Home')
