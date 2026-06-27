import streamlit as st
import random

# Configuração inicial da página
st.set_page_config(page_title="Sorteador de Bingo Profissional", page_icon="🔢", layout="centered")

# CSS customizado para o design do app
st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
        gap: 8px;
        margin-top: 15px;
    }
    .pedra-sorteada {
        background-color: #262730; color: #FF4B4B; border: 2px solid #FF4B4B;
        border-radius: 50%; text-align: center; font-size: 20px; font-weight: bold;
        line-height: 46px; height: 50px; width: 50px; display: inline-block;
    }
    .pedra-ausente {
        background-color: #f0f2f6; color: #d3d3d3; border: 1px dashed #d3d3d3;
        border-radius: 50%; text-align: center; font-size: 18px; line-height: 48px;
        height: 50px; width: 50px; display: inline-block;
    }
    .premio-box {
        background-color: #FF4B4B; color: white; padding: 15px; border-radius: 10px;
        text-align: center; font-weight: bold; font-size: 22px; margin-bottom: 20px;
    }
    @media (prefers-color-scheme: dark) {
        .pedra-ausente { background-color: #1e1e24; color: #444; border: 1px dashed #444; }
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔢 Bingo 5x5 - Itatiaia")

# 1. Inicializa as variáveis de estado
if "historico" not in st.session_state:
    st.session_state.historico = []
if "disponiveis" not in st.session_state:
    st.session_state.disponiveis = list(range(1, 76))
if "ultima_pedra" not in st.session_state:
    st.session_state.ultima_pedra = None

# Função auxiliar para regras de colunas do Bingo 5x5
def obter_letra_bingo(numero):
    if numero <= 15: return "B"
    elif numero <= 30: return "I"
    elif numero <= 45: return "N"
    elif numero <= 60: return "G"
    else: return "O"

# --- BARRA LATERAL (CONFIGURAÇÃO E CONFERÊNCIA AUTOMÁTICA) ---
st.sidebar.header("⚙️ Configuração do Sorteio")

# Definição dos tipos de validação matemática por formato
FORMATOS_REGRAS = {
    "Linha Horizontal (5 números)": {"qtd_min": 4, "qtd_max": 5, "msg": "Uma linha exige de 4 a 5 números marcados."},
    "Coluna Vertical (5 números do mesmo grupo)": {"qtd_min": 5, "qtd_max": 5, "msg": "Uma coluna vertical exige 5 números."},
    "Diagonal (5 números em cruz/X)": {"qtd_min": 4, "qtd_max": 5, "msg": "Uma diagonal exige de 4 a 5 números marcados."},
    "Cartela Cheia (Completa)": {"qtd_min": 24, "qtd_max": 25, "msg": "Cartela cheia exige entre 24 e 25 números válidos."}
}

# Escolha do prêmio correndo no momento
premio_atual = st.sidebar.radio(
    "🏆 Selecione a Premiação em Jogo:",
    list(FORMATOS_REGRAS.keys())
)

st.sidebar.divider()

st.sidebar.header("🔍 Validador Inteligente de Formato")
st.sidebar.write(f"Digite os números da cartela do jogador para validar o formato **{premio_atual.split(' (')[0]}**:")
numeros_candidatos = st.sidebar.text_input("Números da Cartela:", placeholder="Ex: 12, 24, 45, 60")

if numeros_candidatos:
    try:
        limpar_texto = numeros_candidatos.replace(",", " ")
        lista_conferir = list(set([int(n) for n in limpar_texto.split() if n.isdigit()])) # Remove duplicados digitados por erro
        
        regra = FORMATOS_REGRAS[premio_atual]
        total_digitados = len(lista_conferir)
        
        st.sidebar.write(f"Analisando **{total_digitados}** números fornecidos...")
        
        # PASSO 1: Validação do Formato (Quantidade de Pedras)
        if total_digitados < regra["qtd_min"] or total_digitados > regra["qtd_max"]:
            st.sidebar.error(f"❌ FORMATO INVÁLIDO para {premio_atual.split(' (')[0]}!\n{regra['msg']} Você informou {total_digitados}.")
        
        # PASSO 2: Validação de Regra Específica de Coluna
        elif "Coluna Vertical" in premio_atual:
            # Verifica se todos os números pertencem à mesma coluna/letra
            letras_dos_numeros = [obter_letra_bingo(n) for n in lista_conferir]
            todas_iguais = all(l == letras_dos_numeros[0] for l in letras_dos_numeros)
            
            if not todas_iguais:
                st.sidebar.error("❌ FORMATO INVÁLIDO!\nPara validar uma Coluna, todos os 5 números digitados precisam pertencer à mesma letra (Ex: todos da coluna B [1-15]).")
            else:
                # Se o formato passou, valida se as pedras já saíram no sorteio
                invalidos = [n for n in lista_conferir if n not in st.session_state.historico]
                if not invalidos:
                    st.sidebar.success(f"🎉 BINGO CONFIRMADO!\nColuna '{letras_dos_numeros[0]}' completa com sucesso e todas as pedras já saíram!")
                else:
                    st.sidebar.error(f"❌ CARTELA FALSA!\nO formato de coluna está correto, mas estes números AINDA NÃO SAÍRAM: {invalidos}")
                    
        # PASSO 3: Validação Geral de Sorteio (Para Linhas, Diagonais e Cartela Cheia)
        else:
            invalidos = [n for n in lista_conferir if n not in st.session_state.historico]
            if not invalidos:
                st.sidebar.success(f"🎉 BINGO CONFIRMADO!\nFormato correto para {premio_atual.split(' (')[0]} e todas as pedras são válidas!")
            else:
                st.sidebar.error(f"❌ CARTELA FALSA!\nA quantidade de números está certa para o prêmio, mas estes números AINDA NÃO SAÍRAM: {invalidos}")
                
    except ValueError:
        st.sidebar.warning("Digite apenas números válidos separados por espaço ou vírgula.")


# --- TELA PRINCIPAL (SORTEADOR) ---
st.markdown(f'<div class="premio-box">🏆 Valendo Agora: {premio_atual}</div>', unsafe_allow_html=True)

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

st.subheader("📋 Painel Geral de Conferência")
total_sorteadas = len(st.session_state.historico)
total_restantes = len(st.session_state.disponiveis)
st.write(f"Pedras sorteadas: **{total_sorteadas}** | Restantes: **{total_restantes}**")

html_painel = '<div class="grid-container">'
for i in range(1, 76):
    if i in st.session_state.historico:
        html_painel += f'<div class="pedra-sorteada">{i}</div>'
    else:
        html_painel += f'<div class="pedra-ausente">{i}</div>'
html_painel += '</div>'
st.markdown(html_painel, unsafe_allow_html=True)

if st.session_state.historico:
    st.markdown("<br>", unsafe_allow_html=True)
    st.write("**Últimas pedras chamadas (Ordem cronológica):**")
    exibicao_historico = [f"**{obter_letra_bingo(p)}-{p}**" for p in st.session_state.historico[:10]]
    st.write(" ← ".join(exibicao_historico) + ("..." if len(st.session_state.historico) > 10 else ""))
