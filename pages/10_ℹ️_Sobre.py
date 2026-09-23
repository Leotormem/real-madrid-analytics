import streamlit as st


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Sobre | Real Madrid Analytics",
    page_icon="ℹ️",
    layout="wide"
)


# ==========================================================
# ESTILO
# ==========================================================

st.markdown(
    """
<style>

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.section-label {
    color: #60A5FA;
    font-size: 0.78rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.info-card {
    padding: 22px;
    border-radius: 18px;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.85),
            rgba(15,23,42,0.85)
        );

    border:
        1px solid rgba(148,163,184,0.12);

    margin-bottom: 15px;
}

</style>
""",
    unsafe_allow_html=True
)


# ==========================================================
# TÍTULO
# ==========================================================

st.title(
    "ℹ️ Sobre o Projeto"
)

st.caption(
    "Informações acadêmicas, técnicas e conceituais "
    "sobre o Real Madrid Analytics."
)


# ==========================================================
# OBJETIVO
# ==========================================================

st.markdown(
    '<div class="section-label">Projeto</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Real Madrid Analytics"
)

st.write(
    """
    O **Real Madrid Analytics** é um dashboard interativo de
    Sports Analytics desenvolvido com Python e Streamlit.

    O projeto utiliza dados reais da **StatsBomb Open Data**
    referentes aos 38 jogos do Real Madrid na La Liga
    2015/2016.

    A aplicação busca responder à seguinte pergunta:
    """
)

st.info(
    """
    **Como evoluiu o desempenho ofensivo do Real Madrid ao
    longo da La Liga 2015/2016, considerando gols, chutes,
    passes e contribuição individual dos jogadores?**
    """
)


# ==========================================================
# MOTIVAÇÃO
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Motivação</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Por que utilizar Streamlit?"
)

st.markdown(
    """
    O Streamlit foi escolhido porque permite transformar
    análises desenvolvidas em Python em aplicações web
    interativas com pouco código.

    Em projetos de Ciência de Dados e Sports Analytics,
    isso é particularmente útil porque permite integrar:

    - processamento de dados;
    - filtros interativos;
    - métricas;
    - DataFrames;
    - gráficos;
    - mapas;
    - formulários;
    - navegação entre páginas;
    - download de arquivos.

    Dessa maneira, análises que normalmente ficariam
    restritas a scripts ou notebooks podem ser exploradas
    diretamente por usuários através de uma interface web.
    """
)


# ==========================================================
# CARACTERÍSTICAS DO STREAMLIT
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Streamlit</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Principais características"
)

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        """
<div class="info-card">

### 🐍 Python

A interface pode ser construída diretamente
em Python, sem exigir desenvolvimento
tradicional em HTML e JavaScript.

</div>
""",
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
<div class="info-card">

### ⚡ Interatividade

Widgets como selectbox, radio, checkbox,
slider e formulários executam novamente
a aplicação conforme a interação do usuário.

</div>
""",
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
<div class="info-card">

### 📊 Data Science

Possui integração direta com Pandas,
Matplotlib, Seaborn, Plotly e diversas
bibliotecas do ecossistema Python.

</div>
""",
        unsafe_allow_html=True
    )


# ==========================================================
# ARQUITETURA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Arquitetura</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Como uma aplicação Streamlit funciona?"
)

st.write(
    """
    O Streamlit executa o script Python de cima para baixo.

    Quando o usuário interage com um widget, a aplicação
    pode ser executada novamente. Os valores dos componentes
    são utilizados pelo código Python para gerar a nova
    interface.

    Recursos como **Session State** ajudam a preservar
    informações entre essas execuções, enquanto o
    **cache** evita que operações pesadas sejam repetidas
    desnecessariamente.
    """
)

st.code(
    """
import streamlit as st

opcao = st.selectbox(
    "Escolha uma opção",
    ["A", "B", "C"]
)

st.write(
    f"Opção selecionada: {opcao}"
)
""",
    language="python"
)


# ==========================================================
# FLUXO DA APLICAÇÃO
# ==========================================================

st.subheader(
    "Fluxo simplificado"
)

st.markdown(
    """
    **Usuário → Widget → Python → Processamento → Interface**

    No projeto, por exemplo:

    **Usuário seleciona partida → StatsBombPy carrega eventos
    → Pandas processa os dados → Streamlit atualiza métricas
    e gráficos.**
    """
)


# ==========================================================
# COMPARAÇÃO DE FERRAMENTAS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Comparação</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Streamlit, Dash, Panel e Voilà"
)


comparacao = {
    "Ferramenta": [
        "Streamlit",
        "Dash",
        "Panel",
        "Voilà"
    ],

    "Característica": [
        "Criação rápida de aplicações usando Python",
        "Dashboards altamente customizáveis",
        "Integração com ecossistema científico Python",
        "Transforma notebooks Jupyter em aplicações"
    ],

    "Uso comum": [
        "Data Science e protótipos",
        "Dashboards corporativos",
        "Visualização científica",
        "Publicação de notebooks"
    ]
}


st.table(
    comparacao
)


st.write(
    """
    Para este projeto, o **Streamlit** foi escolhido pela
    facilidade de integração com Pandas, StatsBombPy,
    mplsoccer, Matplotlib, Seaborn e Plotly, além da rapidez
    para criar interfaces interativas.
    """
)


# ==========================================================
# MARKDOWN
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Elementos do Streamlit</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Markdown"
)

st.markdown(
    """
    O Streamlit permite utilizar **Markdown** diretamente
    dentro da aplicação.

    Podemos utilizar:

    - **negrito**
    - *itálico*
    - listas
    - títulos
    - links
    - blocos de código
    """
)


# ==========================================================
# LATEX
# ==========================================================

st.subheader(
    "LaTeX"
)

st.write(
    "Um exemplo utilizado nas análises é a taxa de conversão:"
)

st.latex(
    r"""
    \text{Taxa de Conversão}
    =
    \frac{\text{Gols}}
    {\text{Chutes}}
    \times 100
    """
)


# ==========================================================
# CÓDIGO FORMATADO
# ==========================================================

st.subheader(
    "Código formatado"
)

st.code(
    """
from statsbombpy import sb

eventos = sb.events(
    match_id=3825700
)

chutes = eventos[
    eventos["type"] == "Shot"
]
""",
    language="python"
)


# ==========================================================
# MAGIC
# ==========================================================

st.subheader(
    "Comandos Magic"
)

st.write(
    """
    O Streamlit também permite exibir valores sem utilizar
    explicitamente uma função como `st.write()`.
    """
)

st.code(
    """
nome = "Real Madrid"

nome
""",
    language="python"
)

st.caption(
    "Ao escrever apenas o nome da variável em uma aplicação "
    "Streamlit, seu conteúdo pode ser apresentado automaticamente."
)


# ==========================================================
# TECNOLOGIAS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Tecnologias</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Stack do projeto"
)

t1, t2, t3, t4 = st.columns(4)


with t1:

    st.metric(
        "Frontend",
        "Streamlit"
    )


with t2:

    st.metric(
        "Dados",
        "StatsBombPy"
    )


with t3:

    st.metric(
        "Campo",
        "mplsoccer"
    )


with t4:

    st.metric(
        "Processamento",
        "Pandas"
    )


st.markdown(
    """
    Outras bibliotecas utilizadas:

    - **NumPy**
    - **Matplotlib**
    - **Seaborn**
    - **Plotly**
    - **streamlit-extras**
    """
)


# ==========================================================
# ESTRUTURA
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Arquitetura do projeto</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Organização dos arquivos"
)

st.code(
    """
sports_analytics_at/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── pages/
│   ├── 1_🏠_Inicio.py
│   ├── 2_⚽_Temporada.py
│   ├── 3_📈_Evolucao.py
│   ├── 4_🎯_Finalizacoes.py
│   ├── 5_🔄_Passes.py
│   ├── 6_👤_Jogadores.py
│   ├── 7_⚽_Partida.py
│   ├── 8_📋_Eventos.py
│   ├── 9_🔬_Analises.py
│   └── 10_ℹ️_Sobre.py
│
└── utils/
    ├── dados.py
    ├── graficos.py
    └── funcoes.py
""",
    language="text"
)


# ==========================================================
# COMPONENTES UTILIZADOS
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Recursos implementados</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Recursos do Streamlit utilizados"
)

recursos = [
    "st.title()",
    "st.header()",
    "st.subheader()",
    "st.caption()",
    "st.write()",
    "st.markdown()",
    "st.code()",
    "st.latex()",
    "st.metric()",
    "st.dataframe()",
    "st.table()",
    "st.json()",
    "st.selectbox()",
    "st.multiselect()",
    "st.radio()",
    "st.checkbox()",
    "st.slider()",
    "st.form()",
    "st.download_button()",
    "st.spinner()",
    "st.progress()",
    "st.columns()",
    "st.expander()",
    "st.sidebar",
    "st.cache_data",
    "Session State",
    "Múltiplas páginas"
]


for recurso in recursos:

    st.write(
        f"✅ {recurso}"
    )


# ==========================================================
# FONTES
# ==========================================================

st.divider()

st.markdown(
    '<div class="section-label">Dados</div>',
    unsafe_allow_html=True
)

st.subheader(
    "Fonte dos dados"
)

st.info(
    """
    **StatsBomb Open Data**

    Competição: La Liga

    Temporada: 2015/2016

    Equipe analisada: Real Madrid

    Partidas analisadas: 38
    """
)


# ==========================================================
# CRÉDITOS
# ==========================================================

st.divider()

st.markdown(
    """
    ### Assessment

    **Disciplina:** Desenvolvimento Front-End com Python e Streamlit

    **Aluno:** Leonardo Luiz Tormem

    **Professor:** Tiago Cariolano de Souza Xavier
    """
)

st.caption(
    "Projeto acadêmico de Sports Analytics desenvolvido "
    "com Python e Streamlit."
)