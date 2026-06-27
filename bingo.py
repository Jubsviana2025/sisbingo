import streamlit as st
import random

# Configuração inicial da página (ajusta o layout para mobile e PC)
st.set_page_config(page_title="Sorteador de Bingo", page_icon="🔢", layout="centered")

# CSS customizado para criar as pedras grandes e redondas no painel de conferência
st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
        gap: 8px;
        margin-top: 15px;
    }
    .pedra-sorteada {
        background-color: #262730;
        color: #FF4B4B;
        border: 2px solid #FF4B4B;
        border-radius: 50%;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        line-height: 46px;
        height: 50px;
        width: 50px;
        display: inline-block;
    }
    .pedra-ausente {
        background-color: #f0f2f6;
        color: #d3d3d3;
        border: 1px dashed #d3d3d3;
        border-radius: 50%;
        text-align: center;
        font-size: 18px;
        line-height: 48px;
        height: 50px;
        width: 50px;
        display: inline-block;
    }
    /* Estilo para o modo escuro do Streamlit se necessário */
    @media (prefers-color-scheme: dark) {
        .pedra-ausente {
            background-color: #1e1e24;
            color: #444;
            border: 1px dashed #444;
        }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔢 Bingo Virtual Itatiaia")
st.write("Números de 1 a 75 sem repetição!")

# 1. Inicializa as variáveis de estado (se não existirem)
if "historico" not in st.session_state:
    st.session_state.historico = []

if "disponiveis" not in st.session_state:
    st.session_state.disponiveis = list(range(1, 76))

if "ultima_pedra" not in st.session_state:
    st.session_state.ultima_pedra = None

# Botões de controle lado a lado
col1, col2 = st.columns(2)

with col1:
    # Botão para sortear a próxima pedra
    if st.button("🎰 Sortear Próxima Pedra", use_container_width=True, disabled=len(st.session_state.disponiveis) == 0):
        pedra = random.choice(st.session_state.disponiveis)
        st.session_state.ultima_pedra = pedra
        st.session_state.historico.insert(0, pedra) # Mais recente primeiro no histórico interno
        st.session_state.disponiveis.remove(pedra)

with col2:
    # Botão para reiniciar o sorteio
    if st.button("🔄 Iniciar Novo Sorteio", use_container_width=True, type="primary"):
        st.session_state.historico = []
        st.session_state.disponiveis = list(range(1, 76))
        st.session_state.ultima_pedra = None
        st.rerun()

st.divider()

# 2. Exibição da Última Pedra (Destaque Principal)
if st.session_state.ultima_pedra:
    st.markdown(
        f"""
        <div style="text-align: center;">
            <p style="font-size: 24px; margin-bottom: 0; color: gray;">Última Pedra Sorteada:</p>
            <h1 style="font-size: 110px; color: #FF4B4B; margin-top: 0; font-weight: bold; line-height: 1.1;">{st.session_state.ultima_pedra}</h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.info("Clique em 'Sortear Próxima Pedra' para começar!")

st.divider()

# 3. Painel Geral de Conferência (Estilo Tabuleiro de Bingo)
st.subheader("📋 Painel Geral de Conferência")

total_sorteadas = len(st.session_state.historico)
total_restantes = len(st.session_state.disponiveis)

st.write(f"Pedras sorteadas: **{total_sorteadas}**  |  Pedras restantes: **{total_restantes}**")

# Montando o tabuleiro do 1 ao 75 em HTML para ficar grande e fixo
html_painel = '<div class="grid-container">'
for i in range(1, 76):
    if i in st.session_state.historico:
        # Se já foi sorteada, ganha a classe de destaque (Grande e Vermelha)
        html_painel += f'<div class="pedra-sorteada">{i}</div>'
    else:
        # Se não foi sorteada, fica apagada (Cinza de fundo)
        html_painel += f'<div class="pedra-ausente">{i}</div>'
html_painel += '</div>'

st.markdown(html_painel, unsafe_allow_html=True)

# 4. Histórico Sequencial rápido (para saber a ordem exata das últimas)
if st.session_state.historico:
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Ordem de saída (Mais recentes primeiro):**")
    st.write(" → ".join(f"**{p}**" for p in st.session_state.historico[:10]) + ("..." if len(st.session_state.historico) > 10 else ""))