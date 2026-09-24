import streamlit as st
import pandas as pd

# --- Fase 1: Estrutura Básica ---
st.title('Dashboard de Vendas')

@st.cache_data
def carregar_dados():
    df = pd.read_csv('vendas.csv', sep=';')
    if 'data_hora' in df.columns:
        df['mes'] = df['data_hora'].str[:7]
    return df

df = carregar_dados()

# --- Fase 2: Layout e Filtros Laterais ---
st.sidebar.title('Filtros')

if 'categoria' in df.columns:
    lista_de_categorias = df['categoria'].unique().tolist()
    categorias_selecionadas = st.sidebar.multiselect('Selecione as Categorias', options=lista_de_categorias)
    
    if categorias_selecionadas:
        df_filtrado = df[df['categoria'].isin(categorias_selecionadas)]
    else:
        df_filtrado = df
else:
    df_filtrado = df

# --- Fase 3: Métricas em Destaque e Visualização de Dados ---
# Passo 1: Criação das colunas
col1, col2 = st.columns([1, 1])

# Passo 2: Indicadores numéricos nas colunas
if 'valor' in df_filtrado.columns:
    receita_calculada = df_filtrado['valor'].sum()
else:
    receita_calculada = 0.0

total_pedidos = len(df_filtrado)

with col1:
    st.metric(label='Receita Total', value=f"R$ {receita_calculada:,.2f}")

with col2:
    st.metric(label='Total de Pedidos', value=total_pedidos)

# Passo 3: Área de navegação por abas
aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

# Passo 4: Gráfico de área na aba1
with aba1:
    st.subheader("Evolução Mensal de Receita")
    if 'mes' in df_filtrado.columns and 'valor' in df_filtrado.columns:
        dados_agrupados = df_filtrado.groupby('mes')['valor'].sum()
        st.area_chart(dados_agrupados)
    else:
        st.warning("As colunas 'mes' ou 'valor' não foram encontradas.")

# Passo 5: Tabela de dados interativa e exportação
with aba2:
    st.subheader("Dados Detalhados")
    # Exibindo o DataFrame filtrado como tabela interativa
    st.dataframe(df_filtrado)
    
    # Preparando o arquivo CSV para download
    csv = df_filtrado.to_csv(index=False, sep=';').encode('utf-8')
    
    # Botão de exportação
    st.download_button(
        label="Download dos dados filtrados (CSV)",
        data=csv,
        file_name='vendas_filtradas.csv',
        mime='text/csv'
    )
