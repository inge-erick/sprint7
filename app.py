import pandas as pd
import plotly.express as px
import streamlit as st

# Encabezado
st.header("Panel de Análisis de Vehículos Usados")

# Cargar dataset
car_data = pd.read_csv("vehicles_us.csv")

st.write("Explora datos de anuncios de vehículos en EE.UU. con visualizaciones interactivas.")

# ----------------------
# Visualizador de datos filtrado por tipo
# ----------------------
st.subheader("Visualizador de Datos")
tipos = ["Todos"] + sorted(car_data["type"].dropna().unique())
tipo_sel = st.selectbox("Selecciona un tipo de vehículo:", tipos)

if tipo_sel != "Todos":
    data_filtrada = car_data[car_data["type"] == tipo_sel]
else:
    data_filtrada = car_data

st.write(f"Mostrando {len(data_filtrada)} registros")
st.dataframe(data_filtrada)

# ----------------------
# Histograma interactivo
# ----------------------
if st.checkbox("Mostrar histograma de odómetro"):
    st.write("Distribución de kilometraje según los datos filtrados.")
    fig_hist = px.histogram(
        data_filtrada,
        x="odometer",
        nbins=30,
        title="Distribución del Odómetro",
        labels={"odometer": "Kilometraje (millas)"},
        opacity=0.75
    )
    fig_hist.update_layout(bargap=0.1)
    st.plotly_chart(fig_hist, use_container_width=True)

# ----------------------
# Gráfico de dispersión interactivo
# ----------------------
if st.checkbox("Mostrar gráfico de dispersión de precio vs año"):
    st.write("Relación entre año del vehículo y precio.")
    fig_scatter = px.scatter(
        data_filtrada,
        x="model_year",
        y="price",
        color="condition",
        hover_data=["model", "odometer", "fuel", "transmission", "type"],
        title="Precio vs Año del Vehículo",
        labels={"model_year": "Año", "price": "Precio (USD)"},
        opacity=0.6
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ----------------------
# Comparador de distribución de precios por tipo
# ----------------------
if st.checkbox("Comparar distribución de precios por tipo de vehículo"):
    top_tipos = car_data["type"].value_counts().head(10).index
    df_top = car_data[car_data["type"].isin(top_tipos)]
    
    fig_box = px.box(
        df_top,
        x="type",
        y="price",
        title="Distribución de Precios por Tipo de Vehículo (Top 10)",
        labels={"type": "Tipo de vehículo", "price": "Precio (USD)"},
        points="outliers"
    )
    st.plotly_chart(fig_box, use_container_width=True)

st.write("Selecciona las opciones para ver las visualizaciones. Puedes filtrar por tipo de vehículo para un análisis más detallado.")
