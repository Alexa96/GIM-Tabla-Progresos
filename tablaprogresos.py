import streamlit as st
import pandas as pd
import os

# Nombre del archivo CSV para guardar los datos
CSV_FILE = "tareasprogresos.csv"

# Función para cargar los datos desde el archivo CSV
def cargar_datos():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            "Cliente", "Tarea", "Responsable", "Progreso (%)", "Comentarios", "Prioridad", 
            "Dependencia", "Fecha de inicio", "Fecha de entrega"
        ])

# Función para guardar los datos en el archivo CSV
def guardar_datos(data):
    data.to_csv(CSV_FILE, index=False)

# Cargar los datos al iniciar
if "data" not in st.session_state:
    st.session_state.data = cargar_datos()


# Título de la aplicación
st.title("Gestión de Progresos de Tareas")


# Enlace directo al logo en Google Drive
logo_url = "https://irp.cdn-website.com/edbbae6c/dms3rep/multi/logo-412999722.png"
# Mostrar el logo en la barra lateral
st.sidebar.image(logo_url, use_container_width=True)

# Formulario para agregar tareas
st.sidebar.header("Agregar una nueva tarea")

with st.sidebar.form("Formulario de Tarea"):
    cliente = st.text_input("Cliente")
    tarea = st.text_input("Nombre de la tarea/pieza")
    responsable = st.text_input("Responsable")
    progreso = st.slider("Progreso (%)", 0, 100, 0)
    comentarios = st.text_area("Comentarios u Observaciones")
    prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"])
    dependencia = st.text_input("Depende de (otra tarea o pieza)")
    fecha_inicio = st.date_input("Fecha de inicio")
    fecha_entrega = st.date_input("Fecha de entrega estimada")
    
    # Botón para enviar
    submit = st.form_submit_button("Agregar tarea")



# Agregar la tarea a la tabla
if submit:
    # Validación simple
    if cliente and tarea and responsable:
        nueva_fila = {
            "Cliente": cliente,
            "Tarea": tarea,
            "Responsable": responsable,
            "Progreso (%)": progreso,
            "Comentarios": comentarios,
            "Prioridad": prioridad,
            "Dependencia": dependencia,
            "Fecha de inicio": fecha_inicio,
            "Fecha de entrega": fecha_entrega,
        }
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([nueva_fila])], ignore_index=True)
        guardar_datos(st.session_state.data)  # Guardar los datos en CSV
        st.success("Tarea agregada exitosamente.")
    else:
        st.error("Por favor, completa los campos obligatorios.")
    
# Aplicar estilos CSS personalizados para ajustar comentarios en el editor
st.markdown(
    """
    <style>
    .streamlit-table-wrapper td:nth-child(5) {
        max-width: 200px; /* Ajusta la columna de Comentarios */
        word-wrap: break-word;
        white-space: normal;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Mostrar la tabla de tareas con capacidad de edición
st.subheader("Lista de Tareas")
edited_data = st.data_editor(
    st.session_state.data,
    num_rows="dynamic",
    key="editable_table"
)

# Actualizar los datos en tiempo real
if not edited_data.equals(st.session_state.data):
    st.session_state.data = edited_data
    guardar_datos(st.session_state.data)  # Guardar los datos actualizados
    st.success("Los datos se actualizaron correctamente.")

# Visualización del progreso
st.subheader("Progreso de Tareas")
for index, row in st.session_state.data.iterrows():
    progreso = row["Progreso (%)"]
    # Validar que el progreso no sea None o NaN
    if pd.isna(progreso) or progreso is None:
        progreso = 0  # Valor predeterminado en caso de que esté vacío
    st.write(f"**{row['Tarea']}** - Responsable: {row['Responsable']}")
    if progreso <= 33:
        st.write("🔴 Bajo progreso")
    elif progreso <= 66:
        st.write("🟡 Progreso medio")
    else:
        st.write("🟢 Alto progreso")
    st.progress(progreso / 100)
