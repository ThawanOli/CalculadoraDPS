import streamlit as st
import re
import json

# Configuração da página Web
st.set_page_config(page_title="Anime Astral DPS Calculator", page_icon="https://imgs.search.brave.com/uURRODNhU2oVGHe49vCUi5vMvkCx73E2-_i2enyC7-I/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9pbWcu/ZnJlZXBpay5jb20v/cHNkLXByZW1pdW0v/bmVvbi1waXNjYW5k/by1lbS11bS1lbWJs/ZW1hLWhleGFnb25h/bC1jb20tdW1hLXNp/bGh1ZXRhLWRlLWRy/YWdhby1lLWVzdHJ1/dHVyYS1jcnV6YWRh/LWRlbnRyby1kZS1j/YXJhY3RlcmlzdGlj/YXNfMTE0MjI4My00/NjE3NTkuanBnP3Nl/bXQ9YWlzX2h5YnJp/ZCZ3PTc0MA", layout="centered")

# 1. MAPEAMENTO DO SISTEMA DE NÚMEROS GIGANTES
SUFFIXES = {
    'M': 1e6, 'B': 1e9, 'T': 1e12, 'Qa': 1e15, 'Qi': 1e18,
    'Sx': 1e21, 'Sp': 1e24, 'Oc': 1e27, 'No': 1e30, 'De': 1e33,
    'βA': 1e36, 'βB': 1e39, 'βC': 1e42, 'βD': 1e45, 'βE': 1e48,
    'βF': 1e51, 'βG': 1e54, 'βH': 1e57, 'βI': 1e60, 'βJ': 1e63,
    'βK': 1e66, 'βL': 1e69, 'βM': 1e72, 'βN': 1e75, 'βO': 1e78,
    'βP': 1e81
}
SUFFIX_LIST = ["Nenhum"] + list(SUFFIXES.keys())

def format_number(num):
    if num is None: return "N/A"
    if num < 1e6: return f"{num:.2f}"
    for suffix, value in sorted(SUFFIXES.items(), key=lambda x: x[1], reverse=True):
        if num >= value:
            return f"{num / value:.2f} {suffix}"
    return f"{num:.2f}"

def parse_requirement(val_str):
    if not val_str or any(x in val_str.lower() for x in ['not possible', 'dont have data', 'possible', 'n temos']):
        return None
    val_str = val_str.strip().replace(',', '')
    match = re.match(r"^([0-9.]+)\s*([a-zA-Zβ\d]+)?$", val_str)
    if not match: return None
    num_part = float(match.group(1))
    suffix_part = match.group(2)
    if suffix_part and suffix_part in SUFFIXES:
        return num_part * SUFFIXES[suffix_part]
    return num_part

# BANCO DE DADOS
GAME_MODES = {
    "Ninja Raid": [
        ("Wave 5", "242.67 M"), ("Wave 10", "38 B"), ("Wave 15", "6 T"), ("Wave 20", "944 T"),
        ("Wave 25", "148.33 Qa"), ("Wave 30", "23.33 Qi"), ("Wave 35", "3.67 Sx"), ("Wave 40", "577.67 Sx"),
        ("Wave 45", "91 Sp"), ("Wave 50", "14.33 Oc"), ("Wave 55", "2.25 No"), ("Wave 60", "353.33 No"),
        ("Wave 65", "55.67 De"), ("Wave 70", "8.67 βA"), ("Wave 75", "1.37 βB"), ("Wave 80", "216.33 βB"),
        ("Wave 85", "34 βC"), ("Wave 90", "5.33 βD"), ("Wave 95", "841.33 βD"), ("Wave 100", "132.33 βE")
    ],

    "Time Trial Easy": [
        ("Room 5", "18.08 M"), ("Room 10", "72.17 B"), ("Room 15", "287.75 T"), ("Room 20", "1.17 Qi"),
        ("Room 25", "4.58 Sx"), ("Room 30", "3.5 Sp"), ("Room 35", "72.83 Oc"), ("Room 40", "290.42 No"),
        ("Room 45", "1.17 βA"), ("Room 50", "4.58 βB")
    ],

    "Time Trial Medium": [
        ("Room 5", "174.67 βC"), ("Room 10", "3.5 βE"), ("Room 15", "70.08 βF"), ("Room 20", "1.42 βH"), 
        ("Room 25", "28.08 βI"), ("Room 30 (Predicted)", "560.67 βJ"), ("Room 35 (Predicted)", "11.21 βL"), 
        ("Room 40 (Predicted)", "224.27 βM"), ("Room 45 (Predicted)", "4.49 βO"), ("Room 50 (Predicted)", "89.71 βP")
    ],

    "Titan Defense": [
        ("Wave 5", "530 Qa"), ("Wave 10", "83.33 Qi"), ("Wave 15", "13.12 Sx"), ("Wave 20", "2.06 Sp"),
        ("Wave 25", "323.33 Sp"), ("Wave 30", "53.33 Oc"), ("Wave 35", "8.03 No"), ("Wave 40", "1.26 De"),
        ("Wave 45", "200 De"), ("Wave 50", "31.29 βA"), ("Wave 55", "4.91 βB"), ("Wave 60", "773.33 βB"),
        ("Wave 65", "120 βC"), ("Wave 70", "19.11 βD"), ("Wave 75", "3 βE"), ("Wave 80", "473.33 βE"),
        ("Wave 85", "73.33 βF"), ("Wave 90", "11.69 βG"), ("Wave 95", "1.84 βH"), ("Wave 100", "288.88 βH (Predicted)")
    ],

    "Timeless Raid": [
        ("Wave 5", "184.67 No"), ("Wave 10", "137 Oc"), ("Wave 15", "101.67 No"), ("Wave 20", "75.33 De"),
        ("Wave 25", "55.67 βA"), ("Wave 30", "41.33 βB"), ("Wave 35", "30.67 βC"), ("Wave 40", "22.67 βD"),
        ("Wave 45", "17 βE"), ("Wave 50", "12.67 βF")
    ],

    "Infinity Castle": [
        ("Wave 10", "377 De"), ("Wave 20", "724.67 βB"), ("Wave 30", "1.39 βE")
    ],

    "Gate E Rank": [
        ("Wave 10", "582.67 Sx"), ("Wave 20", "1.64 Oc"), ("Wave 30", "5.33 No"), ("Wave 40", "18 De"), ("Wave 50", "60.33 βA")
    ],

    "Gate D Rank": [
        ("Wave 10", "2.96 No"), ("Wave 20", "9.67 De"), ("Wave 30", "32.67 βA"), ("Wave 40", "108.67 βB"), ("Wave 50", "361.33 βC")
    ],

    "Gate C Rank": [
        ("Wave 10 (Boss/Arise)", "16.67 βA"), ("Wave 20 (Boss/Arise)", "55.67 βB"), 
        ("Wave 30", "12.33 βC"), ("Wave 30 (Boss/Arise)", "463 βC"), 
        ("Wave 35", "712 βC"), 
        ("Wave 40", "41 βD"), ("Wave 40 (Boss/Arise)", "616 βD"), 
        ("Wave 45", "2.37 βE"), 
        ("Wave 50", "136.67 βE"), ("Wave 50 (Boss/Arise)", "3.67 βF")    
    ],

    "Gate B Rank": [
        ("Wave 5", "57 βB"), ("Wave 10", "3.28 βC"), ("Wave 10 (Boss)", "49.33 βC"), 
        ("Wave 15", "189.33 βC"), ("Wave 20", "11 βD"), ("Wave 20 (Boss)", "163.67 βD"), 
        ("Wave 25", "629.67 βD"), ("Wave 30", "36.33 βE"), ("Wave 30 (Boss)", "544.67 βE"), 
        ("Wave 35", "2.09 βF"), ("Wave 40", "120.67 βF"), ("Wave 40 (Boss)", "1.81 βG"), 
        ("Wave 45", "7 βG"), ("Wave 50", "401.67 βG"), ("Wave 50 (Boss)", "6 βH")    
    ],
    "Clover Raid": [
        ("Wave 5", "2.77 βB"), ("Wave 10", "2.02 βC"), ("Wave 10 (Boss)", "73.33 βD"), 
        ("Wave 15", "3.29 βD"), ("Wave 20", "3.67 βE"), ("Wave 20 (Boss)", "87 βE"), 
        ("Wave 25", "4 βF"), ("Wave 30", "4.33 βG"), ("Wave 30 (Boss)", "103.33 βG"), 
        ("Wave 35", "4.66 βH"), ("Wave 40", "5 βI"), ("Wave 40 (Boss)", "122.67 βI"), 
        ("Wave 45", "5.65 βJ (Predicted)"), ("Wave 50", "6.21 βK (Predicted)"), ("Wave 50 (Boss)", "Not Possible")
    ],
}

# INTERFACE WEB (STREAMLIT)
st.title("Anime Astral DPS Calculator")
st.subheader("Painel Tático de DPS & Progresso")

# Abas de navegação de forma nativa e limpa
tab1, tab2 = st.tabs(["Calculadora de Status", "Wiki & Alvos Reversos"])

with tab1:
    st.header("Seus Atributos")
    
    # Grid de inputs
    col1, col2 = st.columns([2, 1])
    with col1:
        power_num = st.number_input("Current Power:", min_value=0.0, value=10.0, step=1.0)
    with col2:
        selected_suffix = st.selectbox("Sufixo:", SUFFIX_LIST, index=12) # Padrão βB
        
    multi_input = st.text_input("Damage Multiplier:", value="5000000")
    fast_click = st.checkbox("Possuo Fast Click Gamepass (3.66x)", value=True)
    
    # Processa os multiplicadores textuais se o usuário digitar M ou B
    try:
        multi_clean = multi_input.upper().replace('M', '000000').replace('B', '000000000')
        damage_multi = float(multi_clean) if multi_clean else 1.0
    except ValueError:
        st.error("Por favor, digite um Damage Multiplier válido.")
        damage_multi = 0.0

    current_power = power_num * SUFFIXES[selected_suffix] if selected_suffix in SUFFIXES else power_num
    multiplier = 3.66 if fast_click else 2.66
    user_dps = multiplier * current_power * damage_multi

    # Exibe o DPS Calculado em destaque
    st.metric(label="SEU DPS CALCULADO", value=format_number(user_dps))
    
    st.markdown("---")
    st.header("Progresso Estimado")

    # Varre os modos de jogo e monta os relatórios e barras
    for mode_name, stages in GAME_MODES.items():
        if mode_name == "Gate B Rank": continue # Pula o que está totalmente sem dados
        
        total_stages = len(stages)
        passed_count = 0
        highest_passed = "Nenhuma"
        next_stage, next_req_raw = None, None
        
        for stage_name, req_str in stages:
            req_val = parse_requirement(req_str)
            if "not possible" in req_str.lower(): total_stages -= 1; continue
            if "dont have data" in req_str.lower() or "n temos" in req_str.lower() or req_str == "N/A":
                next_stage = f"{stage_name} (Dados ausentes)"
                break
            if req_val is not None:
                if user_dps >= req_val:
                    highest_passed = stage_name
                    passed_count += 1
                else:
                    next_stage = stage_name
                    next_req_raw = req_val
                    break
                    
        # Exibe progresso visual
        pct = (passed_count / total_stages) if total_stages > 0 else 0.0
        st.write(f"**{mode_name}** — Passa até: `{highest_passed}`")
        st.progress(pct)
        
        if next_stage:
            if next_req_raw:
                st.caption(f"**Próximo objetivo:** {next_stage} (Falta **{format_number(next_req_raw - user_dps)}** de DPS)")
            else:
                st.caption(f"**Próximo objetivo:** {next_stage}")
        else:
            st.caption(" **Modo totalmente dominado com o status atual!**")
        st.write("")

with tab2:
    st.header("Calculadora Reversa de Metas")
    st.write("Selecione um local e descubra se o seu DPS atual é suficiente ou quanto falta.")
    
    wiki_mode = st.selectbox("Escolha o Modo de Jogo:", list(GAME_MODES.keys()))
    
    waves_disponiveis = [stage[0] for stage in GAME_MODES[wiki_mode]]
    wiki_wave = st.selectbox("Escolha a Wave/Room Alvo:", waves_disponiveis)
    
    if wiki_mode and wiki_wave:
        req_str = next((stage[1] for stage in GAME_MODES[wiki_mode] if stage[0] == wiki_wave), None)
        req_val = parse_requirement(req_str)
        
        st.markdown(f"**Requisito desta Fase:** `{req_str}`")
        
        if req_str in ["N/A", "Not Possible", "Possible, Dont have Data"]:
            st.warning("Não há dados numéricos válidos ou a fase é impossível.")
        else:
            if user_dps >= req_val:
                st.success(f"✓ **Você já passa!** Seu DPS supera o requisito por um excesso de {format_number(user_dps - req_val)}.")
            else:
                st.error(f"✗ **Você não passa ainda.** Falta exatamente **{format_number(req_val - user_dps)}** de DPS para vencer essa onda.")