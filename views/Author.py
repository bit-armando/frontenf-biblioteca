import streamlit as st
import pandas as pd
import requests
import json


# Obtener la lista de autores desde la API
def obtener_autores():
    autores = requests.get('http://127.0.0.1:8000/libros/autor/').content.decode('utf-8')
    return json.loads(autores)


# Función para añadir autor
def crear_autor(nombre, apellido_p, apellido_m):
    data = {
        'nombre':     nombre,
        'apellido_p': apellido_p,
        'apellido_m': apellido_m,
    }
    requests.post('http://127.0.0.1:8000/libros/autor', json=data)


# Función para actualizar autor
def actualizar_autor(id, nombre, apellido_p, apellido_m):
    data = {
        'nombre':     nombre,
        'apellido_p': apellido_p,
        'apellido_m': apellido_m,
    }
    requests.put(f'http://127.0.0.1:8000/libros/autor/{id}', json=data)


# Función para eliminar autor
def eliminar_autor(id):
    requests.delete(f'http://127.0.0.1:8000/libros/autor/{id}')


autores = obtener_autores()
st.title("Gestión de Autores")

# Variables para controlar la edición
autor_seleccionado = None

# Sección para crear/actualizar autor
entrada, vista = st.columns(2)

with entrada:
    st.subheader("Agregar / Editar Autor")

    # Si hay un autor seleccionado para editar, usamos sus datos como valores iniciales
    if 'autor_id' not in st.session_state:
        st.session_state['autor_id'] = None

    if st.session_state['autor_id'] is not None:
        autor_seleccionado = next((autor for autor in autores if autor['id'] == st.session_state['autor_id']), None)
        nombre_valor = autor_seleccionado['nombre']
        apellido_p_valor = autor_seleccionado['apellido_p']
        apellido_m_valor = autor_seleccionado['apellido_m']
    else:
        nombre_valor = ""
        apellido_p_valor = ""
        apellido_m_valor = ""

    # Campos de texto con valores iniciales
    nombre = st.text_input("Nombre:", value=nombre_valor)
    apellido_p = st.text_input("Apellido Paterno:", value=apellido_p_valor)
    apellido_m = st.text_input("Apellido Materno:", value=apellido_m_valor)

    # Botón para agregar o actualizar según el estado
    if st.session_state['autor_id'] is None:
        if st.button("Agregar Autor"):
            crear_autor(nombre, apellido_p, apellido_m)
            st.rerun()
    else:
        if st.button("Actualizar Autor"):
            actualizar_autor(st.session_state['autor_id'], nombre, apellido_p, apellido_m)
            st.session_state['autor_id'] = None  # Limpiar el estado después de actualizar
            st.rerun()

with vista:
    # Mostrar la lista de autores con opciones para editar o eliminar
    st.subheader("Lista de Autores")
    for autor in autores:
        st.write(f"{autor['nombre']} {autor['apellido_p']} {autor['apellido_m']}")

        col1, col2 = st.columns(2)
        with col1:
            # Editar autor y guardar su ID en session_state
            if st.button("Editar", key=f"editar_{autor['id']}"):
                st.session_state['autor_id'] = autor['id']
                st.rerun()

        with col2:
            if st.button("Eliminar", key=f"eliminar_{autor['id']}", type='primary'):
                eliminar_autor(autor['id'])
                st.rerun()
