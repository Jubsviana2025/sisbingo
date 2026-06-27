import streamlit as st
import random

# Configuração inicial da página
st.set_page_config(page_title="Sorteador de Bingo Profissional", page_icon="🔢", layout="centered")

# CSS customizado para as pedras grandes, design do painel e alertas
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
    .premio-box {
        background-color: #FF4B4B;
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 22px;
        margin-bottom: 20px;
    }
    @media (prefers-color-scheme: dark) {
        .pedra-ausente { background-color: #1e1e24; color: #444; border: 1px dashed #444; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔢 Sorteador de Bingo - 5x5")

# 1. Inicializa as variáveis de estado
if "historico" not in st.session_state:
    st.session_state.historico = []
if "disponiveis" not in st.session_state:
    st.session_state.disponiveis = list(range(1, 76))
if "ultima_pedra" not in st.session_state:
    st.session_state.ultima_pedra = None

# --- BARRA LATERAL (CONFIGURAÇÃO E CONFERÊNCIA) ---
st.sidebar.header("⚙️ Configuração do Sorteio")

# Permite ao operador customizar o nome dos 4 prêmios
premio1 = st.sidebar.text_input("1º Prêmio:", value="1ª Linha Horizontal")
premio2 = st.sidebar.text_input("2º Prêmio:", value="Qualquer Coluna")
premio3 = st.sidebar.text_input("3º Prêmio:", value="Cruz ou Diagonal")
premio4 = st.sidebar.text_input("4º Prêmio (Principal):", value="Cartela Cheia")

# Seletor para o operador mudar o prêmio ativo
premio_atual = st.sidebar.radio(
    "🏆 Selecione a Premiação em Jogo:",
    [premio1, premio2, premio3, premio4]
)

st.sidebar.divider()

# --- NOVO: MÓDULO DE CONFERÊNCIA DE CARTELA ---
st.sidebar.header("🔍 Validador de Ganhador")
st.sidebar.write("Digite os números que o jogador completou (separe por espaço ou vírgula):")
numeros_candidatos = st.sidebar.text_input("Números da Cartela:", placeholder="Ex: 12, 24, 45, 60")

if numeros_candidatos:
    try:
        # Processa o texto digitado transformando em uma lista de inteiros limpa
        limpar_texto = numeros_candidatos.replace(",", " ")
        lista_conferir = [int(n) for n in limpar_texto.split() if n.isdigit()]
        
        if lista_conferir:
            # Verifica quais números digitados REALMENTE já foram sorteados
            sorteados_validos = [n for n in lista_conferir if n in st.session_state.historico]
            invalidos = [n for n in lista_conferir if n not in st.session_state.historico]
            
            st.sidebar.write(f"Conferindo **{len(lista_conferir)}** números...")
            
            # Se todos os números digitados estão no histórico, BINGO!
            if len(sorteados_validos) == len(lista_conferir):
                st.sidebar.success(f"🎉 BINGO CONFIRMADO!\nTodos os {len(lista_conferir)} números digitados já saíram!")
            else:
                st.sidebar.error(f"❌ CARTELA FALSA / INCORRETA!\nOs seguintes números AINDA NÃO SAÍRAM: {invalidos}")
    except ValueError:
        st.sidebar.warning("Por favor, digite apenas números válidos separados por espaço ou vírgula.")

# --- TELA PRINCIPAL ---
# Mostra o prêmio atual em destaque na tela principal
st.markdown(f'<div class="premio-box">🏆 Valendo Agora: {premio_atual}</div>', unsafe_allow_html=True)

# Botões de controle lado a lado
col1, col2 = st.columns(2)

with col1:
    if st.button("🎰 Sortear Próxima Pedra", use_container_width=True, disabled=len(st.session_state.disponiveis) == 0):
        pedra = random.choice(st.session_state.disponiveis)
        st.session_state.ultima_pedra = pedra
        st.session_state.historico.insert(0, pedra)
        st.session_state.disponiveis.remove(pedra)

with col2:
    if st.button("🔄 Iniciar Novo Sorteio", use_container_width=True, type="primary"):
        st.session_state.historico = []
        st.session_state.disponiveis = list(range(1, 76))
        st.session_state.ultima_pedra = None
        st.rerun()

st.divider()

# 2. Função para obter a Letra Correspondente (Padrão BINGO 5x5)
def obter_letra_bingo(numero):
    if numero <= 15: return "B"
    elif numero <= 30: return "I"
    elif numero <= 45: return "N"
    elif numero <= 60: return "G"
    else: return "O"

# Exibição da Última Pedra
if st.session_state.ultima_pedra:
    letra = obter_letra_bingo(st.session_state.ultima_pedra)
    st.markdown(
        f"""
        <div style="text-align: center;">
            <p style="font-size: 22px; margin-bottom: 0; color: gray;">Última Pedra Sorteada:</p>
            <h1 style="font-size: 110px; color: #FF4B4B; margin-top: 0; font-weight: bold; line-height: 1.1;">
                <span style="color: gray; font-size: 80px;">{letra}-</span>{st.session_state.ultima_pedra}
            </h1>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    st.info("Clique em 'Sortear Próxima Pedra' para começar o sorteio!")

st.divider()

# 3. Painel Geral de Conferência
st.subheader("📋 Painel Geral de Conferência")

total_sorteadas = len(st.session_state.historico)
total_restantes = len(st.session_state.disponiveis)
st.write(f"Pedras sorteadas: **{total_sorteadas}** | Restantes: **{total_restantes}**")

# Tabuleiro estruturado do 1 ao 75
html_painel = '<div class="grid-container">'
for i in range(1, 76):
    if i in st.session_state.historico:
        html_painel += f'<div class="pedra-sorteada">{i}</div>'
    else:
        html_painel += f'<div class="pedra-ausente">{i}</div>'
html_painel += '</div>'

st.markdown(html_painel, unsafe_allow_html=True)

# 4. Histórico sequencial das últimas 10
if st.session_state.historico:
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Últimas pedras chamadas (Ordem cronológica):**")
    exibicao_historico = []
    for p in st.session_state.historico[:10]:
        exibicao_historico.append(f"**{obter_letra_bingo(p)}-{p}**")
    st.write(" ← ".join(exibicao_historico) + ("..." if len(st.session_state.historico) > 10 else ""))
