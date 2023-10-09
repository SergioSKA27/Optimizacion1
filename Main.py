import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
from itertools import combinations
#Autor: Sergio Demis Lopez Martinez, 2023.
#set the configuration
st.set_page_config(page_title="Método Gráfico", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="expanded")

st.title("Metodo Gráfico")

objfunc = st.text_input("Ingrese la función objetivo: ",'2x + 3y')
obf = sp.parse_expr(objfunc.strip(),transformations='all')
with st.expander('Ayuda'):
    st.info("Ejemplo: 2*x + 3*y")
obj = st.selectbox("Seleccione el tipo de problema: ", ("Maximizar", "Minimizar"))

numres = st.number_input("Ingrese el número de restricciones: ", min_value=1, max_value=10, value=1, step=1)

with st.expander('Ayuda'):
    st.info("Ejemplo: 2*x + 3*y <= 10")
    st.info("Ejemplo: 2*x + 3*y >= 10")
    st.info("Ejemplo: 2*x + 3*y = 10")

st.divider()
restrictions = []
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
if obj == "Maximizar":
    st.subheader("$$ Max\ Z = " + sp.latex(obf)+'$$')
else:
    st.subheader("$$ Min Z = " + sp.latex(obf)+'$$')

st.write('Sujeto a: ')
if len(restrictions) and len(restrictions[0]) > 0  :
    print_restricciones(restrictions)

st.latex(str(obf.free_symbols)+ ' ≥ 0')

rangeplt = st.slider("Rango de la gráfica", min_value=-10, max_value=10000, value=10, step=10)

fig = go.Figure()
x, y = sp.symbols('x y')

intersections = []



for i in range(len(restrictions)):
    if restrictions[i]['op'] == "≤" or restrictions[i]['op'] == "≥":
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
        fig.add_trace(go.Scatter(x=np.linspace(-10,rangeplt,100), y=f(np.linspace(-10,rangeplt,100)), name="Restricción "+str(i+1), mode="lines"))
        fig.add_trace(go.Scatter(x=[float(interx)], y=[0], mode="markers",marker=dict(size=5,color="red"),name=str(i+1)+" Intersección eje x "))
        fig.add_trace(go.Scatter(x=[0], y=[float(intery)], mode="markers",marker=dict(size=5,color="red"),name=str(i+1)+" Intersección eje y "))

fig.add_vline(x=0, line_width=1)
fig.add_hline(y=0, line_width=1)
fig.update_layout(title="Método Gráfico", xaxis_title="x", yaxis_title="y")
st.plotly_chart(fig, use_container_width=True)


exp = [restrictions[i]['exp']+(-1*restrictions[i]['val']) for i in range(len(restrictions))]

st.write(np.array(list(combinations(exp,2))))


@st.cache_data
def factible_region(expr,rangeplt):
    ys = []
    xs = []
    x,y = sp.symbols('x y')
    for i in range(len(expr)):
        x_range = np.linspace(-10,rangeplt,100)
        if expr[i][0].free_symbols == {x}:
            f1 =  sp.lambdify(x, expr[i][0])
        elif expr[i][0].free_symbols == {x,y}:
            f1 =  sp.lambdify([x,y], expr[i][0])
        if expr[i][1].free_symbols == {x}:
            f2 =  sp.lambdify(x, expr[i][1])
        elif expr[i][1].free_symbols == {x,y}:
            f2 =  sp.lambdify([x,y], expr[i][1])

        y_range = np.linspace(-10,max(max(sp.lambdify(x,sp.solve(expr[i][0],y)[0])(x_range)),max(sp.lambdify(x,sp.solve(expr[i][1],y)[0])(x_range))),100)
        x_grid, y_grid = np.meshgrid(x_range, y_range)
        if expr[i][0].free_symbols == {x,y}:
            z1 = f1(x_grid,y_grid)
        elif expr[i][0].free_symbols == {x}:
            z1 = f1(x_grid)
        if expr[i][1].free_symbols == {x,y}:
            z2 = f2(x_grid,y_grid)
        elif expr[i][1].free_symbols == {x}:
            z2 = f2(x_grid)
        ys.append(z1)
        ys.append(z2)
    return ys,x_grid




region = factible_region(np.array(list(combinations(exp,2))),rangeplt)
st.write(region[0], len(region[1]))


st.write(sp.Poly(restrictions[0]['exp']+(-1*restrictions[0]['val'])).coeffs())


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
        if expr[i][1].free_symbols == {x}:
            f2 =  sp.Poly(expr[i][1]).coeffs()
            f2.insert(1,0)
            b.append(f2[-1]*-1)
            del(f2[-1])
        elif expr[i][1].free_symbols == {x,y}:
            f2 =  sp.Poly(expr[i][1]).coeffs()
            b.append(f2[-1]*-1)
            del(f2[-1])
        m = sp.Matrix([f1,f2])

        if m.det() != 0:
            inter.append(np.round(np.ravel((m.inv()*sp.Matrix(b)),order='F').astype(float)))

    return inter

maxif = list(all_intersections(np.array(list(combinations(exp,2)))))+intersections+[[0,0]]


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

    return maxx, vals[maxx.index(max(maxx))]

st.write(max_value(maxif,obf)[0])
