import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import zipfile

st.set_page_config(
    page_title="Dashboard Ventas",
    page_icon="📊",
    layout="wide"
)
# Titulo de la aplicacion
st.title("Dashboard de ventas (Usando muestra)")
tab1, tab2, tab3, tab4 = st.tabs(["Visión Global", "Por tienda", "Por estado", "Sorpresa"])
columnas_necesarias = ['date', 'store_nbr', 'family', 'sales', 'onpromotion','holiday_type', 'state', 'transactions', 'year', 'month','week', 'day_of_week']

archivo1_zip = "parte_1.zip"
archivo2_zip = "parte_2.zip"
# Descomprimir
with zipfile.ZipFile(archivo1_zip, "r") as zip_ref:
    zip_ref.extractall()

with zipfile.ZipFile(archivo2_zip, "r") as zip_ref:
    zip_ref.extractall()

@st.cache_data 
def cargar_datos():
    # Carga de datos costosa    
    parte1 = pd.read_csv("parte_1.csv",parse_dates=["date"], index_col=0)    
    parte2 = pd.read_csv("parte_2.csv",parse_dates=["date"], index_col=0)
    return parte1, parte2
parte1, parte2 = cargar_datos()
df = df_combined = pd.concat([parte1, parte2], ignore_index=True)  # Junto para tener un unico df



with tab1:  
    st.header("Visión global")

    st.subheader("Conteo general")
    numero_tiendas = df["store_nbr"].nunique()
    st.write("● **Número total de tiendas:**", numero_tiendas)
    total_productos_venden = df["family"].nunique()  # Se entiende como los productos que se venden siendo los tipos de producto
    st.write("● **Número de tipos de productos que se venden:**", total_productos_venden)
    st.write("Número total de productos que se venden se interpreta como número total de tipos de productos, ya que no hay un indicador de producto.")
    total_ventas = df["family"].count()  
    st.write("● **Número de ventas:**", total_ventas)
    total_volumen_ventas = df["sales"].sum()  
    st.write("● **Total volumen de ventas:**", total_volumen_ventas)
    total_estados = df["state"].nunique()
    st.write("● **Número de estados en los que está la empresa:**", total_estados)
    total_meses = df[["year", "month"]].drop_duplicates().shape[0]
    st.write("● **Número de meses de los que se tienen datos:**", total_meses)

    st.divider()
    st.subheader("Análisis en términos medios")
    top_ventas = df.groupby("family")["sales"].sum().sort_values(ascending=False).head(10)
    ventas_por_tienda = df.groupby("store_nbr")["sales"].sum()
    top_tiendas_promo = df[df["onpromotion"] > 0].groupby("store_nbr")["sales"].sum().sort_values(ascending=False).head(10)
    st.write("● **Top 10 productos por ventas**")
    st.bar_chart(top_ventas,x_label="Tipo producto", y_label="Volumen de ventas", color="#59A14F", sort=False)
    st.write("● **Distribucion de las ventas por tienda**")
    st.bar_chart(ventas_por_tienda,x_label="Número de tienda",  y_label="Volumen de ventas",color="#F28E2B", sort=False)
    st.write("● **Top 10 tiendas con ventas en promoción**")
    st.bar_chart(top_tiendas_promo, x_label="Número de tienda",  y_label="Volumen de ventas en promoción",color="#76B7B2", sort = False)

    st.divider()
    st.subheader("Análisis de la estacionalidad")
    ventas_dow = df.groupby("day_of_week")["sales"].mean()
    ventas_week = df.groupby("week")["sales"].mean()
    ventas_month = df.groupby("month")["sales"].mean()

    col1, col2= st.columns(2)
    with col1:
        st.write("● **Venta en funcion de dia semana**")
        st.bar_chart(ventas_dow, x_label="Día de la semana",  y_label="Volumen medio de ventas")
    with col2:
        st.write("● **Venta en funcion de semana**")
        st.bar_chart(ventas_week, x_label="Semana del año",  y_label="Volumen medio de ventas")
    
    st.write("● **Venta en funcion de mes**")
    st.line_chart(ventas_month, x_label= "Mes del año", y_label="Volumen medio de ventas ")


with tab2:
    st.header("Por tienda")
    tiendas = sorted(df["store_nbr"].unique())
    tienda_sel = st.selectbox("Selecciona tienda:", tiendas)
    df_tienda = df[df["store_nbr"] == tienda_sel] 
    
    ventas_year = df_tienda.groupby("year")["sales"].sum().sort_index()
    total_prod_vendidos = df_tienda["family"].count()
    total_en_promo = df_tienda[df_tienda["onpromotion"] > 0]["family"].count()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Volumen de ventas totales por año")
        st.line_chart(ventas_year, x_label="Año", y_label="Volumen de ventas", color="#4E79A7")
    with col2:
        st.subheader("Resumen tienda")
        st.metric("Productos vendidos", total_prod_vendidos)
        st.metric("Productos en promoción vendidos", total_en_promo)


with tab3:
    st.header("Por estado")
    states = sorted(df["state"].unique())
    state_sel = st.selectbox("Selecciona estado:", states)
    df_state = df[df["state"] == state_sel]

    st.subheader("Transacciones por año") 
    transacciones_year = df_state.groupby("year")["transactions"].sum().sort_index()
    st.line_chart(transacciones_year, x_label="Año", y_label="Transacciones", color="#4E79A7")

    st.subheader("Ranking de tiendas con más ventas")
    ranking_tiendas = df_state.groupby("store_nbr")["sales"].sum().sort_values(ascending=False)
    st.bar_chart(ranking_tiendas.head(10), x_label="Número de tienda", y_label="Volumen ventas", color="#59A14F",sort=False)
    
    productos_vendido = df_state.groupby("family")["sales"].sum().sort_values(ascending=False)
    st.subheader(f"Producto más vendido en estado {state_sel}: {productos_vendido.index[0]}")


with tab4:
    st.header("Sorpresa: impacto de festivos")
    df_festivos = df[df["holiday_type"].notna()]
    festivos = df_festivos["holiday_type"].unique()

    st.subheader("Volumen de ventas medias por tipo de festivo")
    ventas_festivo = df_festivos.groupby("holiday_type")["sales"].mean()
    st.bar_chart(ventas_festivo, x_label="Tipo de festivo", y_label="Volumen de ventas medio", color="#59A14F", sort="-sales")

    st.divider()
    festivo_sel = st.selectbox("Selecciona tipo de festivo:", festivos)
    df_festivo_sel = df[df["holiday_type"] == festivo_sel]
    st.subheader(f"Ranking de tiendas con más ventas por el tipo de festivo {festivo_sel}")
    ranking_tiendas = df_festivo_sel.groupby("store_nbr")["sales"].sum().sort_values(ascending=False)
    st.bar_chart(ranking_tiendas.head(10), x_label="Número de tienda", y_label="Volumen ventas", color="#4A90E2",sort=False)

    producto_festivo = df_festivo_sel.groupby("family")["sales"].sum().sort_values(ascending=False)
    st.subheader(f"Producto más vendido durante el tipo de festivo {festivo_sel}: {producto_festivo.index[0]}")

st.caption("© 2025 - MTeresa Sangil Terrés - 202407108")

    



    







