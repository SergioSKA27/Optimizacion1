import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from itertools import combinations
import pandas as pd
from streamlit.components.v1 import html
#Autor: Sergio Demis Lopez Martinez, 2023.
#set the configuration
st.set_page_config(page_title="Método Gráfico", page_icon=":snowflake:", layout="wide", initial_sidebar_state="collapsed")
#.....................................Data Input.............................................
html(r'''
<!DOCTYPE html>
<html>
<head>
<style>
    @import url("https://fonts.googleapis.com/css?family=Poppins:100,200,300,400,500,600,700,800,900");
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: "Poppins", sans-serif;
    }
    body {
        display: flex;
        background: transparent;
        min-height: 100vh;
        align-items: center;
        justify-content: center;
    }
    .content {
        width: 100%;
        justify-content: center;
    }
    .content h2 {
        color: #fff;
        font-size: 8em;
        position: absolute;
        transform: translate(-50%, -50%);
    }
    .content h2:nth-child(1) {
        color: transparent;
        -webkit-text-stroke: 2px #03a9f4;
    }
    .content h2:nth-child(2) {
      color: #03a9f4;
      animation: animate 4s ease-in-out infinite;
    }
    @keyframes animate {
      0%,
      100% {
        clip-path: polygon(
          0% 45%,
          16% 44%,
          33% 50%,
          54% 60%,
          70% 61%,
          84% 59%,
          100% 52%,
          100% 100%,
          0% 100%
        );
      }

        50% {
            clip-path: polygon(
            0% 60%,
            15% 65%,
            34% 66%,
            51% 62%,
            67% 50%,
            84% 45%,
            100% 46%,
            100% 100%,
            0% 100%
            );
        }
    }
</style>
</head>
<body>
<section>
  <div class="content">
    <h2>Método&nbsp;Simplex</h2>
    <h2>Método&nbsp;Simplex</h2>
  </div>
</section>
</body>
</html>
''',height=200)

st.divider()
ranp = None
if st.checkbox("Usar ejemplos"):
    casos = st.selectbox("Seleccione un ejemplo: ", ("Caso 1", "Caso 2", "Caso 3", "Caso 4", "Caso 5","Caso 6"))

    if casos == "Caso 1":
        ranp = 1500
        obf = sp.parse_expr('100x+90y',transformations='all')
        obj = "Maximizar"
        caso1 = [
            {'exp': sp.parse_expr('(7/10)x+y',transformations='all'), 'op': '≤', 'val': 630},
            {'exp': sp.parse_expr('(1/2)x+(5/6)y',transformations='all'), 'op': '≤', 'val': 600},
            {'exp': sp.parse_expr('x+(2/3)y',transformations='all'), 'op': '≤', 'val': 708},
            {'exp': sp.parse_expr('(1/10)x+(1/4)y',transformations='all'), 'op': '≤', 'val': 135},
        ]
        restrictions = caso1

    if casos == "Caso 2":
        obf = sp.parse_expr('3000x+2000y',transformations='all')
        obj = "Maximizar"
        ranp = 10
        caso2 = [
            {'exp': sp.parse_expr('x+2y',transformations='all'), 'op': '≤', 'val': 6},
            {'exp': sp.parse_expr('2x+y',transformations='all'), 'op': '≤', 'val': 8},
            {'exp': sp.parse_expr('-x+y',transformations='all'), 'op': '≤', 'val': 1},
            {'exp': sp.parse_expr('y',transformations='all'), 'op': '≤', 'val': 2},
        ]
        restrictions = caso2

    if casos == "Caso 3":
        obf = sp.parse_expr('5000x+4000y',transformations='all')
        obj = "Maximizar"
        ranp = 15
        caso3 = [
            {'exp': sp.parse_expr('10x+15y',transformations='all'), 'op': '≤', 'val': 150},
            {'exp': sp.parse_expr('20x+10y',transformations='all'), 'op': '≤', 'val': 160},
            {'exp': sp.parse_expr('30x+10y',transformations='all'), 'op': '≥', 'val': 135},
            {'exp': sp.parse_expr('x-3y',transformations='all'), 'op': '≤', 'val': 0},
            {'exp': sp.parse_expr('x+y',transformations='all'), 'op': '≥', 'val': 5},
        ]
        restrictions = caso3

    if casos == "Caso 4":
        obf = sp.parse_expr('18.50x+20y',transformations='all')
        obj = "Maximizar"
        ranp = 40000
        caso4 = [
            {'exp': sp.parse_expr('0.05x+0.05y',transformations='all'), 'op': '≤', 'val': 1100},
            {'exp': sp.parse_expr('0.05x+0.10y',transformations='all'), 'op': '≤', 'val': 1800},
            {'exp': sp.parse_expr('0.10x+0.05y',transformations='all'), 'op': '≤', 'val': 2000},
        ]
        restrictions = caso4

    if casos == "Caso 5":
        obf = sp.parse_expr('0.60x+0.15y',transformations='all')
        obj = "Minimizar"
        ranp = 12
        caso5 = [
            {'exp': sp.parse_expr('0.50x+0.20y',transformations='all'), 'op': '≥', 'val': 4},
            {'exp': sp.parse_expr('0.10x+0.20y',transformations='all'), 'op': '≥', 'val': 1},
        ]
        restrictions = caso5

    if casos == "Caso 6":
        obf = sp.parse_expr('18.50x+20y',transformations='all')
        obj = "Minimizar"
        ranp = 2
        caso6 = [
            {'exp': sp.parse_expr('5x+7y',transformations='all'), 'op': '≤', 'val': 6},
            {'exp': sp.parse_expr('2x+y',transformations='all'), 'op': '≤', 'val': 1.5},
            {'exp': sp.parse_expr('x+y',transformations='all'), 'op': '=', 'val': 1},
        ]
        restrictions = caso6


else:
    #Lee la función objetivo
    objfunc = st.text_input("Ingrese la función objetivo: ",'2x + 3y')
    #La transforma a una expresión simbólica
    obf = sp.parse_expr(objfunc.strip(),transformations='all')
    with st.expander('Ayuda'):
    #Muestra la ayuda para ingresar la función objetivo
        st.info("Ejemplo: 2*x + 3*y")
    #Se selecciona el tipo de problema
    obj = st.selectbox("Seleccione el tipo de problema: ", ("Maximizar", "Minimizar"))

    #Lee el número de restricciones
    numres = st.number_input("Ingrese el número de restricciones: ", min_value=1, max_value=10, value=1, step=1)

    with st.expander('Ayuda'):
    #Muestra la ayuda para ingresar las restricciones
        st.info("Ejemplo: 2*x + 3*y <= 10")
        st.info("Ejemplo: 2*x + 3*y >= 10")
        st.info("Ejemplo: 2*x + 3*y = 10")

    st.divider()
    restrictions = []
    # Lee las restricciones y las almacena en una lista de diccionarios
    # Cada diccionario contiene la expresión(exp), el operador(op) y el valor de la restricción(val)
    for i in range(numres):
        st.subheader("Restricción " + str(i+1))
        cols = st.columns([.4,.1,.4])
        with cols[0]:
            restexp = st.text_input("", key='sr'+str(i))
        with cols[1]:
            rest = st.selectbox("", ("≤", "≥", "="), key='br'+str(i))

        with cols[2]:
            restval = st.number_input("", key='vr'+str(i))
            if  len(restexp) > 0:
                restrictions.append({'exp': sp.parse_expr(restexp.strip(),transformations='all'), 'op': rest, 'val': restval})


#define una función para imprimir las restricciones usando latex
def print_restricciones(restricciones):

    for i in range(len(restricciones)):
        st.latex(sp.latex(restricciones[i]['exp']) + restricciones[i]['op'] + str(restricciones[i]['val']))

st.divider()
#Imprime la función objetivo en latex
if obj == "Maximizar":
    st.subheader("$$ Max\ Z = " + sp.latex(obf)+'$$')
else:
    st.subheader("$$ Min Z = " + sp.latex(obf)+'$$')

#Imprime las restricciones en latex
st.write('Sujeto a: ')
if len(restrictions) and len(restrictions[0]) > 0  :
    print_restricciones(restrictions)

st.latex(str(obf.free_symbols)+ ' ≥ 0')

def add_slackvars(restricciones,obf,probtype):
    slckvar = []
    #Agrega las variables de holgura
    if probtype == "Maximizar":
        for i in range(len(restricciones)):
            z = sp.Symbol('s'+str(i+1))
            if restricciones[i]['op'] == '≤':
            #Añadimos la variable de holgura
                restricciones[i]['exp'] = z+ restricciones[i]['exp']
                obf = z+obf
                slckvar.append(z)
            if restricciones[i]['op'] == '≥':
            #Añadimos la variable de exceso
                restricciones[i]['exp'] = restricciones[i]['exp'] - z
                obf = obf + z
                slckvar.append(z)

    else:
        for i in range(len(restricciones)):
            z = sp.Symbol('s'+str(i+1))
            if restricciones[i]['op'] == '≤':
            #Añadimos la variable de holgura
                restricciones[i]['exp'] = restricciones[i]['exp'] + z
                obf = obf + z
                slckvar.append(z)
            if restricciones[i]['op'] == '≥':
            #Añadimos la variable de exceso
                restricciones[i]['exp'] = restricciones[i]['exp'] - z
                obf = obf + z
                slckvar.append(z)


    return restricciones, obf, slckvar

def add_artificialvar(restricciones,obf,probtype):
    art = []
    m = sp.Symbol('M')
    if probtype == "Maximizar":
        for i in range(len(restricciones)):
            z = sp.Symbol('R'+str(i+1))
            if restricciones[i]['op'] == '=':
            #Añadimos la variable de holgura
                restricciones[i]['exp'] = restricciones[i]['exp'] + z
                obf = obf-m*z
                art.append(z)
            if restricciones[i]['op'] == '≥':
            #Añadimos la variable de exceso
                restricciones[i]['exp'] = restricciones[i]['exp'] + z
                obf = obf - m*z
                art.append(z)
    else:
        for i in range(len(restricciones)):
            z = sp.Symbol('R'+str(i+1))
            if restricciones[i]['op'] == '=':
            #Añadimos la variable de holgura
                restricciones[i]['exp'] = restricciones[i]['exp'] + z
                obf = obf + m*z
                art.append(z)
            if restricciones[i]['op'] == '≥':
            #Añadimos la variable de exceso
                restricciones[i]['exp'] = restricciones[i]['exp'] - z
                obf = obf + m*z
                art.append(z)


    return restricciones, obf, art

def to_matrix(restricciones, obf,slck,art,obj):
    nb = [sp.Poly(restricciones[i]['exp']).coeffs() for i in range(len(restricciones))]
    n = [[nb[i][j] for j in range(len(obf.free_symbols))] for i in range(len(restricciones))]
    a = []
    obff = sp.Poly(obf).coeffs()
    obff += [0]*(len(slck))
    if obj == "Maximizar":
        obff += [sp.Symbol('M')*-1]*(len(art))
    else:
        obff += [sp.Symbol('M')]*(len(art))

    for i in range(len(restricciones)):
        temp = [0]*(len(slck))
        if restricciones[i]['op'] == '≤':
            temp[i] = 1
        if restricciones[i]['op'] == '≥':
            temp[i] = -1
        if restricciones[i]['op'] == '=':
            continue
        n[i] += temp

    for i in range(len(n)):
        if restricciones[i]['op'] == '=' or restricciones[i]['op'] == '≥':
            for j in range(len(n)):
                if i == j:
                    n[j].append(1)
                else:
                    n[j].append(0)
        else:
            continue









    return n, obff



_restrictions, _obf,slck = add_slackvars(list(restrictions), obf, obj)

st.write("Después de agregar las variables de holgura y exceso: ")
#st.write(_restrictions, _obf, slck)
#Imprime la función objetivo en latex
if obj == "Maximizar":
    st.subheader("$$ Max\ Z = " + sp.latex(obf)+'$$')
else:
    st.subheader("$$ Min Z = " + sp.latex(obf)+'$$')

#Imprime las restricciones en latex
st.write('Sujeto a: ')
if len(restrictions) and len(restrictions[0]) > 0  :
    print_restricciones(_restrictions)

st.latex(str(_obf.free_symbols)+ ' ≥ 0')


_restrictionss, _obff,art = add_artificialvar(_restrictions[:], _obf, obj)

#st.write(_restrictionss, _obff, art)
if len(art) > 0:
    #Imprime la función objetivo en latex
    st.write("Después de agregar las variables artificiales: ")
    if obj == "Maximizar":
        st.subheader("$$ Max\ Z = " + sp.latex(obf)+'$$')
    else:
        st.subheader("$$ Min Z = " + sp.latex(obf)+'$$')

    #Imprime las restricciones en latex
    st.write('Sujeto a: ')
    if len(restrictions) and len(restrictions[0]) > 0  :
        print_restricciones(_restrictions)

    st.latex(str(_obf.free_symbols)+ ' ≥ 0')



st.write("Convertimos las restricciones a forma estándar: ")

a, b = to_matrix(restrictions, obf,slck,art,obj)

if obj == "Maximizar":
        st.subheader("$$ Max\ Z = " + sp.latex(sp.Matrix(b).T)+'$$')
else:
    st.subheader("$$ Min Z = " + sp.latex(sp.Matrix(b).T)+'$$')

st.write('Sujeto a: ')
#st.write(a)
st.latex(sp.latex(sp.Matrix(a))+sp.latex(sp.Matrix(list(obf.free_symbols)+slck+art))+ '=' +sp.latex(sp.Matrix([restrictions[i]['val'] for i in range(len(restrictions))])))

