import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.title("Rodeo Personal")

ARCHIVO = "../inventario_rodeo.csv"

# Cargar o crear CSV
if not os.path.exists(ARCHIVO):
    pd.DataFrame(columns=["Caravana","Categoría","Sexo","Raza","Peso_actual_kg",
                          "Fecha_nacimiento","Fecha_compra","Madre_caravana","Observaciones"]
                ).to_csv(ARCHIVO, index=False)

df = pd.read_csv(ARCHIVO)
df["Fecha_nacimiento"] = pd.to_datetime(df["Fecha_nacimiento"], errors="coerce")
df["Fecha_compra"] = pd.to_datetime(df["Fecha_compra"], errors="coerce")

categorias = ["Parido","Escotero","Terneros de ordeño","Terneras destetadas","Terneros destetados"]

# === BORRAR SI HAY QUE BORRAR ===
if st.session_state.get("borrar_rodeo"):
    car = st.session_state.pop("borrar_rodeo")
    df = df[df["Caravana"] != car]
    df.to_csv(ARCHIVO, index=False)
    st.success(f"Animal {car} eliminado")
    st.rerun()

# === CARGAR NUEVO ANIMAL ===
with st.sidebar.form("cargar", clear_on_submit=True):
    caravana = st.text_input("Caravana*")
    cat = st.selectbox("Categoría", categorias)
    sexo = st.radio("Sexo", ["Macho","Hembra"], horizontal=True)
    raza = st.text_input("Raza", "Angus")
    peso = st.number_input("Peso (kg)", 30, 1000, 200)
    c1, c2 = st.columns(2)
    with c1: fnac = st.date_input("Nacimiento", value=None)
    with c2: fcompra = st.date_input("Compra (opcional)", value=None)
    madre = st.text_input("Madre (opcional)")
    obs = st.text_area("Observaciones")
    if st.form_submit_button("Guardar"):
        if not caravana:
            st.error("Falta caravana")
        elif caravana in df["Caravana"].values:
            st.error("Ya existe")
        else:
            nuevo = pd.DataFrame([{"Caravana":caravana,"Categoría":cat,"Sexo":sexo,"Raza":raza,
                                   "Peso_actual_kg":peso,"Fecha_nacimiento":fnac,"Fecha_compra":fcompra,
                                   "Madre_caravana":madre,"Observaciones":obs}])
            df = pd.concat([df, nuevo], ignore_index=True)
            df.to_csv(ARCHIVO, index=False)
            st.success("Guardado")
            st.rerun()

# === GRÁFICO ===
conteo = df["Categoría"].value_counts().reindex(categorias, fill_value=0)
col1, col2 = st.columns([1, 3])
with col1:
    st.metric("Total animales", len(df))
    st.dataframe(pd.DataFrame({"Categoría":conteo.index, "Cabezas":conteo.values}), hide_index=True)
with col2:
    if len(df) > 0:
        fig = px.pie(conteo, values=conteo.values, names=conteo.index, hole=0.4,
                     color_discrete_sequence=px.colors.sequential.Greens)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

# === LISTADO + BORRAR CON UN CLICK ===
filtro = st.selectbox("Filtrar categoría", ["Todas"] + categorias)
dfv = df if filtro == "Todas" else df[df["Categoría"] == filtro]

for _, animal in dfv.iterrows():
    car = str(animal["Caravana"])
    with st.expander(f"{car} – {animal['Sexo']} {animal['Raza']} – {animal['Peso_actual_kg']} kg"):
        c1, c2, c3 = st.columns([3, 3, 1])
        with c1:
            st.write("**Categoría**", animal["Categoría"])
            st.write("**Raza**", animal["Raza"])
        with c2:
            nac = animal["Fecha_nacimiento"].strftime("%d/%m/%Y") if pd.notna(animal["Fecha_nacimiento"]) else "–"
            compra = animal["Fecha_compra"].strftime("%d/%m/%Y") if pd.notna(animal["Fecha_compra"]) else "–"
            st.write("**Nacimiento**", nac)
            st.write("**Compra**", compra)
        with c3:
            if st.button("Borrar", key=f"del_{car}"):
                st.session_state["borrar_rodeo"] = car
                st.rerun()
        if animal["Observaciones"]:
            st.info(animal["Observaciones"])