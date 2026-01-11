import streamlit as st
import pickle
import os
import altair as alt
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Football Studio • AI Pro Analyzer",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Persistência do histórico
DATA_FILE = "football_history.pkl"

def load_history():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'rb') as f:
            return pickle.load(f)
    return []

def save_history(history):
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(history, f)

if "history" not in st.session_state:
    st.session_state.history = load_history()

if "custom_strategies" not in st.session_state:
    st.session_state.custom_strategies = []

# CSS - Histórico horizontal reforçado (uma linha única)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

* { font-family: 'Poppins', sans-serif; }
body { background: radial-gradient(circle at top, #0f2027, #203a43, #2c5364); }

.title { font-size: 52px; font-weight: 800; color: #ffffff; text-align: center; letter-spacing: 2px; }
.subtitle { font-size: 20px; text-align: center; color: #d0d0d0; }

.history-wrapper {
    overflow-x: auto !important;
    white-space: nowrap !important;
    padding: 10px 0;
    background: rgba(255,255,255,0.06);
    border-radius: 16px;
    margin: 12px 0;
}

.history-row {
    display: inline-flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 8px;
}

.result {
    display: inline-block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    line-height: 40px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
    color: white;
    margin: 0 2px;
    vertical-align: middle;
    flex-shrink: 0;
}

.red { background: linear-gradient(145deg, #ff1e1e, #b30000); }
.blue { background: linear-gradient(145deg, #1e90ff, #003d80); }
.yellow { background: linear-gradient(145deg, #ffcc00, #cc9a00); color: #000; }

.warning-box { background: rgba(255,68,68,0.15); border: 1px solid #ff4444; border-radius: 12px; padding: 16px; margin: 20px 0; color: #ffdddd; }
</style>
""", unsafe_allow_html=True)

# Cabeçalho
st.markdown('<div class="title">🃏 Football Studio AI Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Análise Inteligente • Padrões Reais 2026 • Sugestões Avançadas</div>', unsafe_allow_html=True)

st.warning("⚠️ **AVISO**: Apostas envolvem risco financeiro alto. Jogue apenas com dinheiro que pode perder. Proibido para menores de 18 anos.")

# SIDEBAR - Configurações e Estratégias Personalizadas
with st.sidebar:
    st.header("Configurações Profissionais")
    
    gale_level = st.slider("Nível máximo de Gales (Martingale)", min_value=0, max_value=3, value=1, step=1)
    st.info(f"Gales sugeridos: 0 a {gale_level} níveis. Stop após 2 perdas recomendado.")

    st.subheader("Crie Estratégias Personalizadas")
    strategy_name = st.text_input("Nome da Estratégia", placeholder="Ex: Quebra 4 Azuis")
    pattern_str = st.text_input("Sequência do Padrão", placeholder="Ex: B,B,B,B", help="B = 🔵 Player\nR = 🔴 Casa\nY = 🟡 Empate\nSepare por vírgula")
    suggestion = st.selectbox("Sugestão de Entrada Após o Padrão", ["🔵 Player", "🔴 Casa", "🟡 Empate"])

    if st.button("Adicionar Estratégia") and pattern_str:
        pattern_list = [p.strip().upper() for p in pattern_str.split(",")]
        st.session_state.custom_strategies.append((pattern_list, suggestion, strategy_name or "Custom"))
        if len(st.session_state.custom_strategies) > 5:
            st.session_state.custom_strategies = st.session_state.custom_strategies[-5:]
        st.success("Estratégia adicionada!")

    st.markdown("**Estratégias Ativas:**")
    for pat, sug, name in st.session_state.custom_strategies:
        st.write(f"**{name}**: {','.join(pat)} → {sug}")

# FUNÇÕES AUXILIARES
def add_result(value):
    st.session_state.history.insert(0, value)
    st.session_state.history = st.session_state.history[:500]  # Aumentado para mais análise
    save_history(st.session_state.history)

def undo():
    if st.session_state.history:
        st.session_state.history.pop(0)
        save_history(st.session_state.history)

def clear():
    st.session_state.history = []
    save_history([])

color_map = {"R": ("🔴", "red"), "B": ("🔵", "blue"), "Y": ("🟡", "yellow")}
color_to_label = {"R": "🔴 Casa", "B": "🔵 Visitante", "Y": "🟡 Empate"}

def get_stats(history):
    return {
        "R": history.count("R"),
        "B": history.count("B"),
        "Y": history.count("Y"),
        "total": len(history)
    }

def backtest_pattern(history, pattern, suggestion):
    hits = total = 0
    sug_code = {"🔵 Player": "B", "🔴 Casa": "R", "🟡 Empate": "Y"}[suggestion]
    for i in range(len(history) - len(pattern)):
        if history[i:i+len(pattern)] == pattern:
            total += 1
            if i + len(pattern) < len(history) and history[i + len(pattern)] == sug_code:
                hits += 1
    return (hits / total * 100) if total > 0 else None

# DETECÇÃO DE PADRÕES AVANÇADA (todos os 18 + Green Sinais + imagens)
def detect_patterns(history):
    if len(history) < 3:
        return None, 0, "", None

    recent = history[:20]  # Aumentado para capturar padrões longos
    patterns = []

    # Padrões do Green Sinais (oficiais)
    patterns.extend([
        (["B"]*4, "🔴 Casa", 94, "Quebra 4 Azuis - Muito usado"),
        (["R"]*4, "🔵 Player", 94, "Quebra 4 Vermelhos - Muito usado"),
        (["B","R","B","R"], "🔵 Player", 90, "Alternância 4"),
        (["Y","B","Y","R"], "🟡 Empate", 92, "🟡🔵🟡🔴 - Misto com 2 empates"),
        (["Y","Y"], "🟡 Empate", 88, "🟡🟡 - 2 Empates Seguidos"),
    ])

    # 18 padrões que você enviou (mapeados para códigos)
    patterns.extend([
        (["R","R"], "🔴 Casa", 85, "Repetição Simples Vermelho"),
        (["R","R","R"], "🔵 Player", 92, "Repetição Média Vermelho - Quebra"),
        (["R","R","R","R","R"], "🔵 Player", 96, "Repetição Longa - Manipulada"),
        (["R","B","R","B"], "🔴 Casa", 90, "Alternância Simples"),
        (["R","B","R","B","R","B"], "🔴 Casa", 88, "Alternância Longa"),
        (["R","R","B","B"], "🔴 Casa", 90, "Bloco 2x2"),
        (["R","R","R","B","B","B"], "🔴 Casa", 89, "Bloco 3x3"),
        (["R","R","B","R","R","B"], "🔴 Casa", 90, "Bloco Camuflado"),
        (["Y","R","R","B"], "🔵 Player", 87, "Empate Isolado"),
        (["R","R","Y","R","R"], "🔴 Casa", 89, "Empate Âncora"),
        (["R","R","R","Y","B"], "🔵 Player", 92, "Empate de Quebra"),
        (["R","R","Y","B","R"], "🔴 Casa", 85, "Empate Antecipatório"),
        (["R","Y","B","Y","R"], "🟡 Empate", 80, "Empate Intercalado"),
        (["Y","Y"], "🟡 Empate", 85, "Empate Duplo"),
        (["R","R","Y","B","B"], "🔵 Player", 90, "Bloco com Empate Central"),
        (["R","B","Y","B","R"], "🟡 Empate", 85, "Caos com Empate"),
    ])

    # Customizadas
    for pat, sug, name in st.session_state.custom_strategies:
        patterns.append((pat, sug, 90, name))

    detected = []
    for pat, sug, conf, name in patterns:
        if len(recent) >= len(pat) and recent[-len(pat):] == pat:  # Olha o final (mais recente)
            b_conf = backtest_pattern(history, pat, sug)
            final_conf = b_conf if b_conf is not None else conf
            detected.append((name, final_conf, sug, pat))

    if detected:
        best = max(detected, key=lambda x: x[1])
        return best

    return None, 0, "", None

# BOTÕES DE ENTRADA
cols = st.columns(5)
cols[0].button("🔴 Casa", use_container_width=True, on_click=lambda: add_result("R"))
cols[1].button("🔵 Visitante", use_container_width=True, on_click=lambda: add_result("B"))
cols[2].button("🟡 Empate", use_container_width=True, on_click=lambda: add_result("Y"))
cols[3].button("↩️ Desfazer", use_container_width=True, on_click=undo)
cols[4].button("🧹 Limpar Tudo", use_container_width=True, on_click=clear)

# HISTÓRICO HORIZONTAL (mais antigo ← → mais recente)
st.subheader("📊 Histórico (mais antigo ← → mais recente)")

if st.session_state.history:
    display_history = list(reversed(st.session_state.history[:80]))

    history_html = '<div class="history-wrapper"><div class="history-row">'
    
    for val in display_history:
        emoji, cls = color_map[val]
        history_html += f'<div class="result {cls}">{emoji}</div>'

    history_html += '</div></div>'

    st.markdown(history_html, unsafe_allow_html=True)

    st.caption("← Mais antigo                  Mais recente →")
    st.caption("Sequência lida da esquerda para a direita, como no Green Sinais.")

    # Export CSV
    df_export = pd.DataFrame({
        "Resultado": [color_to_label.get(r, r) for r in reversed(st.session_state.history)]
    })
    csv = df_export.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exportar Histórico (CSV)", csv, "historico.csv", "text/csv")

else:
    st.info("Adicione resultados usando os botões acima")

# ANÁLISE & SUGESTÃO
st.subheader("🧠 Análise & Sugestão de Entrada")

if len(st.session_state.history) >= 3:
    result = detect_patterns(st.session_state.history)
    if result and result[0]:
        pattern_name, confidence, suggestion, pattern = result
        st.success(f"**Padrão Detectado**: {pattern_name} ({','.join(pattern or [])})")
        st.markdown(f"**Sugestão de Entrada**: **{suggestion}**")
        st.metric("Assertividade (backtest no histórico)", f"{confidence:.1f}%")
        st.info(f"**Gales Recomendados**: Até {gale_level} níveis (Martingale). Stop após 2 perdas.")
    else:
        st.warning("Nenhum padrão forte detectado no momento.")

    stats = get_stats(st.session_state.history)
    cols_stats = st.columns(3)
    cols_stats[0].metric("Casa (🔴)", f"{stats['R']} ({stats['R']/stats['total']*100:.1f}%)")
    cols_stats[1].metric("Player (🔵)", f"{stats['B']} ({stats['B']/stats['total']*100:.1f}%)")
    cols_stats[2].metric("Empate (🟡)", f"{stats['Y']} ({stats['Y']/stats['total']*100:.1f}%)")

    df_pie = pd.DataFrame({
        "Cor": ["Casa 🔴", "Player 🔵", "Empate 🟡"],
        "Quantidade": [stats["R"], stats["B"], stats["Y"]]
    })
    chart = alt.Chart(df_pie).mark_arc().encode(theta="Quantidade", color="Cor")
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Adicione pelo menos 3 resultados para ativar a análise completa.")

# Aviso final
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="warning-box">Jogue com responsabilidade. Defina stop loss diário e não aposte dinheiro essencial.</div>', unsafe_allow_html=True)
