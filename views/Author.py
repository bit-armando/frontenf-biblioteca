import streamlit as st
import pandas as pd
import requests
import json

autores = requests.get('http://127.0.0.1:8000/libros/autor/').content.decode('utf-8')
autores = json.loads(autores)

df = pd.DataFrame(autores)

# # Función para añadir autor
def crear_autor(nombre, apellido_p, apellido_m):
    data = {
        'nombre': nombre,
        'apellido_p': apellido_p,
        'apellido_m': apellido_m,
    }
    requests.post('http://127.0.0.1:8000/libros/autor', json=data)
#
# # Función para actualizar autor
def actualizar_autor(index, nombre, apellido_p, apellido_m):
    st.session_state.autores[index] = {
        'nombre': nombre,
        'apellido_p': apellido_p,
        'apellido_m': apellido_m
    }
#
# # Función para eliminar autor
# def eliminar_autor(index):
#     del st.session_state.autores[index]

# Sección para crear/actualizar autor
st.title("Gestión de Autores")
nombre = st.text_input("Nombre:")
apellido_p = st.text_input("Apellido Paterno:")
apellido_m = st.text_input("Apellido Materno:")

# Verificar si estamos actualizando
if 'editar_index' in st.session_state:
    editar = True
    index = st.session_state.editar_index
    if st.button("Actualizar Autor"):
        actualizar_autor(index, nombre, apellido_p, apellido_m)

else:
    editar = False
    if st.button("Agregar Autor"):
        crear_autor(nombre, apellido_p, apellido_m)


# Mostrar la lista de autores con opciones para editar o eliminar
# st.subheader("Lista de Autores")
# for autor in autores:
#     st.write(f"{autor['nombre']} {autor['apellido_p']} {autor['apellido_m']}")
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("Editar", key=f"editar_{autor['id']}"):
#             pass
#
#     with col2:
#         if st.button("Eliminar", key=f"eliminar_{autor['id']}"):
#             pass
