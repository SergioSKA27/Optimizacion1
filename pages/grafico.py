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
    <h2>Método&nbsp;Gráfico</h2>
    <h2>Método&nbsp;Gráfico</h2>
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

colsg = st.columns([.3,.7])
if ranp == None:
    with colsg[0]:
        maxg = st.number_input('Maximo de la gráfica', min_value=0, max_value=1000000, value=10, step=10)
    with colsg[1]:
        rangeplt = st.slider("Rango de la gráfica", min_value=0, max_value=maxg, value=10, step=maxg//10)
else:
    rangeplt = ranp
#.....................................Plot Restrictions.............................................
#Creamos una figura
fig = go.Figure()
x, y = sp.symbols('x y')

intersections = []


#Agregamos las restricciones a la figura y calculamos las intersecciones con los ejes
for i in range(len(restrictions)):
    if(restrictions[i]['op'] == "≤" or restrictions[i]['op'] == "≥" or restrictions[i]['op'] == "=") and len(restrictions[i]['exp'].free_symbols) == 2:
        fr = sp.solve(restrictions[i]['exp']+(-1*restrictions[i]['val']),y)
        if  fr != []:
            #st.write(fr)
            f = sp.lambdify(x, fr[0])
        else:
            f = sp.lambdify(x, restrictions[i]['exp'])

        interx = sp.solve(restrictions[i]['exp'].subs({y:0}).evalf()+(-1*restrictions[i]['val']),x)[0]
        intery = sp.solve(restrictions[i]['exp'].subs({x:0}).evalf()+(-1*restrictions[i]['val']),y)[0]
        intersections.append([float(interx),0])
        intersections.append([0,float(intery)])
        #st.write(intery)
        fig.add_trace(go.Scatter(x=np.linspace(0,rangeplt,1000), y=f(np.linspace(0,rangeplt,1000)), name="Restricción "+str(i+1), mode="lines"))
        fig.add_trace(go.Scatter(x=[float(interx)], y=[0], mode="markers",marker=dict(size=5,color="red"),name=str(i+1)+" Intersección eje x "))
        fig.add_trace(go.Scatter(x=[0], y=[float(intery)], mode="markers",marker=dict(size=5,color="red"),name=str(i+1)+" Intersección eje y "))

    elif(restrictions[i]['op'] == "≤" or restrictions[i]['op'] == "≥" or restrictions[i]['op'] == "=") and len(restrictions[i]['exp'].free_symbols) == 1:
        #The restriction is a constant
        if restrictions[i]['exp'].free_symbols == {x}:
            f = sp.lambdify(x, restrictions[i]['exp'])
            fig.add_vline(x=restrictions[i]['val'], line_width=1, name="Restricción "+str(i+1))
            fig.add_trace(go.Scatter(x=[restrictions[i]['val']], y=[0], mode="markers",marker=dict(size=5,color="red"),name=str(i+1)+" Intersección eje x "))
        elif restrictions[i]['exp'].free_symbols == {y}:
            f = sp.lambdify(y, restrictions[i]['exp'])
            fig.add_hline(y=restrictions[i]['val'], line_width=1, name="Restricción "+str(i+1))
            fig.add_trace(go.Scatter(x=[0], y=[restrictions[i]['val']], mode="markers",marker=dict(size=5,color="red"),name=str(i+1)+" Intersección eje y "))


fig.add_vline(x=0, line_width=1)
fig.add_hline(y=0, line_width=1)
fig.update_layout(title="Método Gráfico", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig, use_container_width=True)


exp = [restrictions[i]['exp']+(-1*restrictions[i]['val']) for i in range(len(restrictions)) ]


#---------------------------------Calculate the feasible region---------------------------------
def satisfy_rest(point, restr):
    flag = True
    if point[0] < 0 or point[1] < 0:
        return False
    for i in range(len(restr)):
        if restr[i]['op'] == "≤":
            if restr[i]['exp'].subs({x:point[0],y:point[1]}).evalf() > restr[i]['val']:
                flag = False
                break
        elif restr[i]['op'] == "≥":
            if restr[i]['exp'].subs({x:point[0],y:point[1]}).evalf() < restr[i]['val']:
                flag = False
                break
        elif restr[i]['op'] == "=":
            if restr[i]['exp'].subs({x:point[0],y:point[1]}).evalf() != restr[i]['val']:
                flag = False
                break
    return flag

@st.cache_data
def all_intersections(expr):
    """
    The function `all_intersections` takes in a list of expressions and returns the coordinates of all intersections between
    the curves represented by the expressions.

    :param expr: The `expr` parameter is a list of tuples, where each tuple contains two symbolic expressions. Each
    expression represents a line in the form `ax + by + c = 0`, where `a`, `b`, and `c` are coefficients.
    :return: The function `all_intersections` returns a list of intersection points between the given expressions.
    """
    x,y = sp.symbols('x y')
    inter = []

    for i in range(len(expr)):
        b = []
        if expr[i][0].free_symbols == {x}:
            f1 =  sp.Poly(expr[i][0]).coeffs()
            f1.insert(1,0)
            b.append(f1[-1]*-1)
            del(f1[-1])
        elif expr[i][0].free_symbols == {x,y}:
            f1 =  sp.Poly(expr[i][0]).coeffs()
            b.append(f1[-1]*-1)
            del(f1[-1])
        elif expr[i][0].free_symbols == {y}:
            f1 =  sp.Poly(expr[i][0]).coeffs()
            f1.insert(0,0)
            b.append(f1[-1]*-1)
            del(f1[-1])

        if expr[i][1].free_symbols == {x}:
            f2 =  sp.Poly(expr[i][1]).coeffs()
            f2.insert(1,0)
            b.append(f2[-1]*-1)
            del(f2[-1])
        elif expr[i][1].free_symbols == {x,y}:
            f2 =  sp.Poly(expr[i][1]).coeffs()
            b.append(f2[-1]*-1)
            del(f2[-1])
        elif expr[i][1].free_symbols == {y}:
            f2 =  sp.Poly(expr[i][1]).coeffs()
            f2.insert(0,0)
            b.append(f2[-1]*-1)
            del(f2[-1])

        try:
            m = sp.Matrix([f1,f2])
        except:
            continue
        if m.det() != 0:
            arrr = np.ravel((m.inv()*sp.Matrix(b)),order='F').astype(float)
            inter.append(arrr)
        else:
            continue

    return inter

def max_value(vals, func):
    """
    The function `max_value` takes a list of values and a mathematical function, and returns the maximum value of the
    function along with the corresponding input values.

    :param vals: The `vals` parameter is a list of tuples. Each tuple represents a set of values for the variables `x` and
    `y`. For example, `vals = [(1, 2), (3, 4), (5, 6)]` represents three sets of values: `
    :param func: The parameter `func` is a symbolic expression or function that represents a mathematical function. It can
    be an expression involving variables like `x` and `y`, or it can be a predefined function like `sin(x)` or `exp(x)`. The
    `subs` method is used to substitute specific
    :return: The function `max_value` returns two values: `maxx` and `vals[maxx.index(max(maxx))]`.
    """
    maxx = []

    for i in range(len(vals)):
        maxx.append(func.subs({x:vals[i][0],y:vals[i][1]}).evalf())

    return max(maxx), vals[maxx.index(max(maxx))]

def min_value(vals, func):
    """
    The function `max_value` takes a list of values and a mathematical function, and returns the maximum value of the
    function along with the corresponding input values.

    :param vals: The `vals` parameter is a list of tuples. Each tuple represents a set of values for the variables `x` and
    `y`. For example, `vals = [(1, 2), (3, 4), (5, 6)]` represents three sets of values: `
    :param func: The parameter `func` is a symbolic expression or function that represents a mathematical function. It can
    be an expression involving variables like `x` and `y`, or it can be a predefined function like `sin(x)` or `exp(x)`. The
    `subs` method is used to substitute specific
    :return: The function `max_value` returns two values: `maxx` and `vals[maxx.index(max(maxx))]`.
    """
    minn = []

    for i in range(len(vals)):
        minn.append(func.subs({x:vals[i][0],y:vals[i][1]}).evalf())

    return min(minn), vals[minn.index(min(minn))]



st.session_state['color_region'] = st.color_picker("Color de la región factible", "#73D673")
colorfact = st.session_state['color_region']

if st.button("Calcular"):
    colss = st.columns(3)
    with colss[0]:
        st.write('Intersecciones con los ejes: ',pd.DataFrame(np.array(intersections),columns=['x','y']))

    with colss[1]:
        st.write('Sistemas de ecuaciones: ' ,pd.DataFrame(np.array(list(combinations(exp,2))),columns=['Ecuación 1','Ecuación 2']))

    inters = list(all_intersections(np.array(list(combinations(exp,2)))))
    with colss[2]:
        st.write('Intersecciones entre las restricciones: ')
        st.write(pd.DataFrame(np.array(inters),columns=['x','y']))

    maxif = inters+intersections+[[0,0]]

    maxfilter = []

    for i in range(len(maxif)):
        if satisfy_rest(maxif[i],restrictions):
            maxfilter.append(list(maxif[i]))

    maxfilter = np.array(sorted(maxfilter,key=lambda x: (x[0], x[1])))
    colss2 = st.columns([.4,.6])
    with colss2[0]:
        st.write("Puntos Factibles")
        st.write(pd.DataFrame(np.array(maxfilter),columns=['x','y']))

    if obj == "Minimizar":
        valsmax = min_value(maxfilter,obf)
    else:
        valsmax = max_value(maxfilter,obf)

    with colss2[1]:
        st.subheader("Solución Optima")
        st.latex('Z \ ='+str(valsmax[0]))
        st.latex('x_1 \ ='+str(valsmax[1][0])+',\ \ \ y_1 \ ='+str(valsmax[1][1]))

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=maxfilter[:,0], y=maxfilter[:,1], mode="markers",
    marker=dict(size=5,color="blue"),name="Puntos factibles",fill='toself',fillcolor=colorfact,
    text=['Point A', 'Point B', 'Area'],textposition='top center',
    ))



    for i in range(len(restrictions)):
        if (restrictions[i]['op'] == "≤" or restrictions[i]['op'] == "≥" or restrictions[i]['op'] == "=") and len(restrictions[i]['exp'].free_symbols) == 2:
            fr = sp.solve(restrictions[i]['exp']+(-1*restrictions[i]['val']),y)
            if  fr != []:
                #st.write(fr)
                f = sp.lambdify(x, fr[0])
            else:
                f = sp.lambdify(x, restrictions[i]['exp'])
            fig2.add_trace(go.Scatter(x=np.linspace(0,rangeplt,1000), y=f(np.linspace(0,rangeplt,1000)), name="Restricción "+str(i+1), mode="lines"))
        elif (restrictions[i]['op'] == "≤" or restrictions[i]['op'] == "≥" or restrictions[i]['op'] == "=") and len(restrictions[i]['exp'].free_symbols) == 1:
            #The restriction is a constant
            if restrictions[i]['exp'].free_symbols == {x}:
                f = sp.lambdify(x, restrictions[i]['exp'])
                fig2.add_vline(x=restrictions[i]['val'], line_width=1, name="Restricción "+str(i+1))
            elif restrictions[i]['exp'].free_symbols == {y}:
                f = sp.lambdify(y, restrictions[i]['exp'])
                fig2.add_hline(y=restrictions[i]['val'], line_width=1, name="Restricción "+str(i+1))

    fig2.add_vline(x=0, line_width=1)
    fig2.add_hline(y=0, line_width=1)
    fig2.update_layout(title="Región Factible", xaxis_title="x", yaxis_title="y")
    st.plotly_chart(fig2, use_container_width=True)
