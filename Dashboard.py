#region IMPORTS
from classes.ui.header import HeaderMenu
from classes.ui.footer import Footer
from classes.ui.pages import Pages
from classes.ui.textelement import TextElement
from classes.ui.metrics import DisplayMetrics
from classes.data.fetchdata import DataConnection
from classes.ui.data import PlotData
from streamlit import switch_page
import streamlit as st
import pandas as pd
#endregion

#region PAGE CONFIGURATION
Pages(name="Compras Center", icon=":material/bar_chart:", page_layout="wide")
HeaderMenu.hide_menu()
#endregion

#region DATA LOADING
df = DataConnection.get_purchase_data()

# Limpeza Preço Unitário
if "Preço_Unitário" in df.columns:
    df["Preço_Unitário"] = (
        df["Preço_Unitário"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )
#endregion

#region TABS
tab1, tab2= st.tabs(["ANÁLISE", "DASHBOARD"])
#endregion

#region ANALYSIS TAB
with tab1:
    #region HEADER
    TextElement.set_title(":material/bar_chart: Análise da planilha de compras")
    TextElement.set_caption("**EMPRESA:** MATERIAL DE CONSTRUÇÃO LTDA")
    TextElement.write_text("---")
    #endregion    

    #region FILTERS
    col1, col2, col3 = st.columns(3)
    with col1:
        datas = ["Todos"] + sorted(df['Data_Solicitação'].dropna().unique())
        sel_data = st.selectbox("Data de Solicitação", datas)
    with col2:
        produtos = ["Todos"] + sorted(df['Produto'].dropna().unique())
        sel_prod = st.selectbox("Produto", produtos)
    with col3:
        fornecedores = ["Todos"] + sorted(df['Fornecedor'].dropna().unique())
        sel_fornecedor = st.selectbox("Fornecedor", fornecedores)
    #endregion

    #region APPLY FILTERS
    filtered = df.copy()
    if sel_data != "Todos":
        filtered = filtered[filtered["Data_Solicitação"] == sel_data]
    if sel_prod != "Todos":
        filtered = filtered[filtered["Produto"] == sel_prod]
    if sel_fornecedor != "Todos":
        filtered = filtered[filtered["Fornecedor"] == sel_fornecedor]
    #endregion

    st.dataframe(filtered)
    Footer.footer()
#endregion

#region DASHBOARD TAB
with tab2:
    #region HEADER
    TextElement.set_title(":material/bar_chart: Dashboard de Compras")
    TextElement.set_caption("**EMPRESA:** MATERIAL DE CONSTRUÇÃO LTDA")
    TextElement.write_text("---")
    #endregion

    #region METRICS
    col1, col2, col3, col4 = st.columns(4)

    total_gasto = filtered["Preço_Unitário"].sum()
    produto_caro = filtered.loc[filtered["Preço_Unitário"].idxmax()] if not filtered.empty else None
    fornecedor_rapido = filtered.groupby("Fornecedor")["Prazo_Entrega_dias"].mean().sort_values().head(1)
    total_quantidade = filtered["Quantidade"].sum()

    with col1:
        # Antes de exibir
        def format_brl(valor):
            try:
                # Garantindo que é float
                valor = float(valor)
                # Formata no padrão brasileiro
                return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
            except:
                # Caso dê algum problema, retorna 0
                return "R$ 0,00"


        with col1:
            DisplayMetrics(
                ":material/payment: GASTO TOTAL",
                format_brl(total_gasto)
            )

    with col2:
        if produto_caro is not None:
            DisplayMetrics(":material/shopping_cart: PRODUTO MAIS CARO (unitário)", f"{produto_caro['Produto']}")
        else:
            DisplayMetrics(":material/shopping_cart: PRODUTO MAIS CARO (unitário)", "-")

    with col3:
        if not fornecedor_rapido.empty:
            nome = fornecedor_rapido.index[0]
            DisplayMetrics(":material/store: FORNECEDOR MAIS RÁPIDO", f"{nome}")
        else:
            DisplayMetrics(":material/store: FORNECEDOR MAIS RÁPIDO", "-")

    with col4:
        DisplayMetrics(":material/local_shipping: QUANTIDADE TOTAL COMPRADA", f"{total_quantidade} unidades")
    #endregion

    #region GRÁFICOS SIMPLES COM CONTAINERS
    col1, col2 = st.columns(2)

    # Pizza: gasto por fornecedor
    with col1:
        with st.container(border=True):
            PlotData.pie_plot(filtered, names="Fornecedor", values="Valor_Total", title="Gastos por fornecedor", show=True)

    # Barras: gasto por produto
    with col2:
        with st.container(border=True):
            df_prod = filtered.groupby("Produto", as_index=False)["Preço_Unitário"].sum()
            PlotData.bar_plot(df_prod, x="Produto", y="Preço_Unitário", title="Gasto total por produto", color="lightblue", show=True)

    # Barras horizontais: prazo médio por fornecedor
    with st.container(border=True):
        df_prazo = filtered.groupby("Fornecedor", as_index=False)["Prazo_Entrega_dias"].mean()
        PlotData.bar_plot(df_prazo, x="Prazo_Entrega_dias", y="Fornecedor", title="Prazo médio por fornecedor", color="lightblue", show=True)

    # Linha: evolução do gasto no tempo
    with st.container(border=True):
        df_tempo = filtered.groupby("Data_Solicitação", as_index=False)["Preço_Unitário"].sum()
        PlotData.bar_plot(df_tempo, x="Data_Solicitação", y="Preço_Unitário", title="Evolução do gasto ao longo do tempo", show=True)
    #endregion
    Footer.footer()
#endregion
