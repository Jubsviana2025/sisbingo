import streamlit as st
import random
import time

# Configuração inicial da página
st.set_page_config(page_title="Bingo Animado Profissional", page_icon="🔢", layout="centered")

# CSS customizado para o design do app e balão de fala do narrador
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
    .balao-narrador {
        background-color: #f1f3f4; color: #333; padding: 15px; 
        border-radius: 15px; border-left: 5px solid #FF4B4B;
        font-style: italic; font-size: 18px; margin-bottom: 20px;
        text-align: center; font-weight: 500;
    }
    @media (prefers-color-scheme: dark) {
        .pedra-ausente { background-color: #1e1e24; color: #444; border: 1px dashed #444; }
        .balao-narrador { background-color: #262730; color: #fff; }
    }
    </style>
""", unsafe_allow_html=True)

# --- BANCO DE FRASES ENGRAÇADAS POR TEMA ---
DICIONARIO_PIADAS = {
    "🎉 Clássico / Geral": [
        "Olha o olho do lobo... Número 5!",
        "Dois patinhos na lagoa... 22!",
        "Idade de Cristo... 33!",
        "Se o seu número não saiu, reclama com o Papa!",
        "Quem tá por uma pedra aí já pode começar a rezar!",
        "Grita bingo baixo pra não assustar o azar!",
        "Atenção: conferindo as cartelas com carinho, mas sem suborno!"
    ],
    "🌽 Festa Junina": [
        "Olha a cobra! É mentira... mas o número é de verdade!",
        "Mais quente que fogueira de São João, só o coração de quem tá por uma pedra!",
        "Se ganhar, vai ter que pagar uma rodada de quentão pra mesa toda!",
        "Pula a fogueira, iaiá! Cuidado para não queimar a cartela!",
        "Tá mais disputado que o último pedaço de bolo de fubá!",
        "Anarriê! Quem não marcar esse número vai dançar a quadrilha sozinho!"
    ],
    "👩‍👧 Dia das Mães": [
        "Esse número é que nem conselho de mãe: se você não ouvir, vai se dar mal!",
        "Vou levar um casaco pro globo, porque tá esfriando esse sorteio!",
        "Tá achando que eu sou o quê? Sua mãe pra te dar o número que você quer?",
        "Quem ganhar hoje, já sabe: metade do prêmio vai pra quem te deu a vida!",
        "Se sumir com essa cartela, eu vou aí e acho em dois segundos!",
        "Coração de mãe sempre cabe mais um número na cartela!"
    ],
    "👨‍👦 Dia dos Pais": [
        "Esse sorteio tá mais demorado que o seu pai indo comprar cigarro e voltando 20 anos depois!",
        "Pergunta pro seu pai se ele aprova esse número que saiu!",
        "Quem ganhar vai ter que pagar o churrasco do domingão!",
        "Não adianta chorar, o universo não é seu pai pra te fazer todas as vontades!",
        "Tá com a mão coçando? É o dinheiro do prêmio chegando ou o boleto vencendo!",
        "Abaixa esse som do bingo que o seu pai tá tentando assistir o futebol!"
    ]
}

st.title("🔢 Sorteador de Bingo Animado")

# 1. Inicializa as variáveis de estado
if "historico" not in st.session_state:
    st.session_state.historico = []
if "disponiveis" not in st.session_state:
    st.session_state.disponiveis = list(range(1, 76))
if "ultima_pedra" not in st.session_state:
    st.session_state.ultima_pedra = None
if "frase_atual" not in st.session_state:
    st.session_state.frase_atual = "Bem-vindos ao Bingo! Preparem suas cartelas!"

# Função auxiliar para colunas do Bingo
def obter_letra_bingo(numero):
    if numero <= 15: return "B"
    elif numero <= 30: return "I"
    elif numero <= 45: return "N"
    elif numero <= 60: return "G"
    else: return "O"

# --- BARRA LATERAL ---
st.sidebar.header("⚙️ Configuração do Sorteio")

FORMATOS_REGRAS = {
    "Linha Horizontal (5 números)": {"qtd_min": 4, "qtd_max": 5, "msg": "Uma linha exige de 4 a 5 números."},
    "Coluna Vertical (5 números do mesmo grupo)": {"qtd_min": 5, "qtd_max": 5, "msg": "Uma coluna exige 5 números."},
    "Diagonal (5 números em cruz/X)": {"qtd_min": 4, "qtd_max": 5, "msg": "Uma diagonal exige de 4 a 5 números."},
    "Cartela Cheia (Completa)": {"qtd_min": 24, "qtd_max": 25, "msg": "Cartela cheia exige de 24 a 25 números."}
}

premio_atual = st.sidebar.radio("🏆 Premiação em Jogo:", list(FORMATOS_REGRAS.keys()))

st.sidebar.divider()

# NOVO: SELETOR DE TEMAS
st.sidebar.header("🎭 Tema do Narrador")
tema_selecionado = st.sidebar.selectbox("Escolha o clima do jogo:", list(DICIONARIO_PIADAS.keys()))

st.sidebar.divider()

# VALIDADOR DE GANHADOR
st.sidebar.header("🔍 Validador de Ganhador")
numeros_candidatos = st.sidebar.text_input("Números da Cartela:", placeholder="Ex: 12, 24, 45")

if numeros_candidatos:
    try:
        limpar_texto = numeros_candidatos.replace(",", " ")
        lista_conferir = list(set([int(n) for n in limpar_texto.split() if n.isdigit()]))
        regra = FORMATOS_REGRAS[premio_atual]
        total_digitados = len(lista_conferir)
        
        if total_digitados < regra["qtd_min"] or total_digitados > regra["qtd_max"]:
            st.sidebar.error(f"❌ FORMATO INVÁLIDO!\n{regra['msg']}")
        elif "Coluna Vertical" in premio_atual:
            letras_dos_numeros = [obter_letra_bingo(n) for n in lista_conferir]
            if not all(l == letras_dos_numeros[0] for l in letras_dos_numeros):
                st.sidebar.error("❌ FORMATO INVÁLIDO!\nOs números não são da mesma coluna.")
            else:
                invalidos = [n for n in lista_conferir if n not in st.session_state.historico]
                if not invalidos: st.sidebar.success("🎉 BINGO CONFIRMADO!")
                else: st.sidebar.error(f"❌ CARTELA FALSA! Faltam: {invalidos}")
        else:
            invalidos = [n for n in lista_conferir if n not in st.session_state.historico]
            if not invalidos: st.sidebar.success("🎉 BINGO CONFIRMADO!")
            else: st.sidebar.error(f"❌ CARTELA FALSA! Faltam: {invalidos}")
    except ValueError:
        st.sidebar.warning("Digite apenas números válidos.")


# --- TELA PRINCIPAL ---
st.markdown(f'<div class="premio-box">🏆 Valendo Agora: {premio_atual}</div>', unsafe_allow_html=True)

# NOVO: BALÃO DO NARRADOR QUE ATUALIZA SOZINHO (A cada 15 segundos solta uma piada aleatória do tema)
@st.fragment(run_every=15)
def renderizar_narrador():
    # Se o botão de sortear foi clicado no frame principal, ele muda a piada. 
    # Caso contrário, o tempo passa e ele escolhe outra do tema atual de forma aleatória.
    frase = random.choice(DICIONARIO_PIADAS[tema_selecionado])
    st.markdown(f'<div class="balao-narrador">🎙️ **Narrador diz:** "{frase}"</div>', unsafe_allow_html=True)

renderizar_narrador()

# Botões de controle lado a lado
col1, col2 = st.columns(2)

with col1:
    if st.button("🎰 Sortear Próxima Pedra", use_container_width=True, disabled=len(st.session_state.disponiveis) == 0):
        pedra = random.choice(st.session_state.disponiveis)
        st.session_state.ultima_pedra = pedra
        st.session_state.historico.insert(0, pedra)
        st.session_state.disponiveis.remove(pedra)
        # Força mudar a frase do narrador imediatamente após o clique do sorteio também
        st.rerun()

with col2:
    if st.button("🔄 Iniciar Novo Sorteio", use_container_width=True, type="primary"):
        st.session_state.historico = []
        st.session_state.disponiveis = list(range(1, 76))
        st.session_state.ultima_pedra = None
        st.session_state.frase_atual = "Novo jogo iniciado! Boa sorte!"
        st.rerun()

st.divider()

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

# Painel Geral de Conferência
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
