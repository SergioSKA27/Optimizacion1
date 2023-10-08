import streamlit as st
import sympy as sp
import numpy as np
import plotly.graph_objects as go
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

restrictions = []
for i in range(numres):
    st.subheader("Restricción " + str(i+1))
    cols = st.columns(3)
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
    st.subheader("Función Objetivo:$$ Max\ Z = " + sp.latex(obf)+'$$')
else:
    st.subheader("Función Objetivo:$$ Min Z = " + sp.latex(obf)+'$$')

st.write('Sujeto a: ')
if len(restrictions[0]) > 0:
    print_restricciones(restrictions)



rangeplt = st.slider("Rango de la gráfica", min_value=-10, max_value=10000, value=(-10,10), step=10)

fig = go.Figure()
x, y = sp.symbols('x y')




for i in range(len(restrictions)):
    fr = sp.solve(restrictions[i]['exp']+(-1*restrictions[i]['val']),y)
    if  fr != []:
        #st.write(fr)
        f = sp.lambdify(x, fr[0])
    else:
        f = sp.lambdify(x, restrictions[i]['exp'])
    interx = sp.solve(restrictions[i]['exp'].subs({y:0}).evalf()+(-1*restrictions[i]['val']),x)[0]
    intery = sp.solve(restrictions[i]['exp'].subs({x:0}).evalf()+(-1*restrictions[i]['val']),y)[0]
    st.write(intery)
    fig.add_trace(go.Scatter(x=np.linspace(rangeplt[0],rangeplt[1],100), y=f(np.linspace(rangeplt[0],rangeplt[1],100)), name="Restricción "+str(i+1), mode="lines"))
    fig.add_trace(go.Scatter(x=[float(interx)], y=[0], mode="markers",marker=dict(size=5,color="black"),name=str(i+1)+" Intersección eje x "))
    fig.add_trace(go.Scatter(x=[0], y=[float(intery)], mode="markers",marker=dict(size=5,color="black"),name=str(i+1)+" Intersección eje y "))

fig.add_vline(x=0, line_width=1)
fig.add_hline(y=0, line_width=1)
st.plotly_chart(fig, use_container_width=True)
