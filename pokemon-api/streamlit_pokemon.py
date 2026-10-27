import random

import pandas as pd
import requests
import streamlit as st

# ----------------------------------------------------------------------------
# Configuração da página
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pokédex Interativa",
    page_icon="🔴",
    layout="wide",
)

API_BASE = "https://pokeapi.co/api/v2"

CORES_TIPOS = {
    "normal": "#A8A77A", "fire": "#EE8130", "water": "#6390F0",
    "electric": "#F7D02C", "grass": "#7AC74C", "ice": "#96D9D6",
    "fighting": "#C22E28", "poison": "#A33EA1", "ground": "#E2BF65",
    "flying": "#A98FF3", "psychic": "#F95587", "bug": "#A6B91A",
    "rock": "#B6A136", "ghost": "#735797", "dragon": "#6F35FC",
    "dark": "#705746", "steel": "#B7B7CE", "fairy": "#D685AD",
}

TRADUCAO_TIPOS = {
    "normal": "Normal", "fire": "Fogo", "water": "Água",
    "electric": "Elétrico", "grass": "Planta", "ice": "Gelo",
    "fighting": "Lutador", "poison": "Veneno", "ground": "Terra",
    "flying": "Voador", "psychic": "Psíquico", "bug": "Inseto",
    "rock": "Pedra", "ghost": "Fantasma", "dragon": "Dragão",
    "dark": "Sombrio", "steel": "Aço", "fairy": "Fada",
}

NOMES_STATS = {
    "hp": "HP", "attack": "Ataque", "defense": "Defesa",
    "special-attack": "Ataque Esp.", "special-defense": "Defesa Esp.",
    "speed": "Velocidade",
}

POPULARES = [
    "pikachu", "charizard", "bulbasaur", "squirtle", "eevee",
    "mewtwo", "gengar", "snorlax", "lucario", "gyarados",
]

# ----------------------------------------------------------------------------
# Estilo (CSS)
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .titulo-app {
        font-size: 2.4rem; font-weight: 800; margin-bottom: 0;
        background: linear-gradient(90deg, #EE1515, #F7D02C);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .badge-tipo {
        display: inline-block; padding: 4px 16px; border-radius: 20px;
        color: white; font-weight: 700; margin-right: 8px; font-size: 0.95rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    .cartao-pokemon {
        border-radius: 20px; padding: 24px; color: white;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }
    .nome-pokemon { font-size: 2.4rem; font-weight: 800; text-transform: capitalize; }
    .numero-pokemon { font-size: 1.3rem; opacity: 0.85; font-weight: 600; }
    .stat-linha { display: flex; align-items: center; margin: 8px 0; }
    .stat-nome { width: 130px; font-weight: 600; }
    .stat-valor { width: 45px; text-align: right; font-weight: 700; margin-right: 12px; }
    .stat-trilho {
        flex: 1; background: rgba(128,128,128,0.25);
        border-radius: 10px; height: 14px; overflow: hidden;
    }
    .stat-barra { height: 100%; border-radius: 10px; }
    .chip-habilidade {
        display: inline-block; padding: 6px 14px; margin: 4px 6px 4px 0;
        border-radius: 12px; background: rgba(128,128,128,0.18);
        font-weight: 600; text-transform: capitalize;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# Funções de acesso à API
# ----------------------------------------------------------------------------
def normalizar_nome(nome: str) -> str:
    return nome.strip().lower().replace(" ", "-")


@st.cache_data(show_spinner=False, ttl=3600)
def buscar_pokemon(nome: str):
    """Retorna (dados, erro). Mantém a lógica original: status 200 = sucesso."""
    try:
        resposta = requests.get(f"{API_BASE}/pokemon/{nome}", timeout=10)
    except requests.RequestException:
        return None, "Falha de conexão com a PokéAPI."
    if resposta.status_code == 200:
        return resposta.json(), None
    return None, "Não foi possível consultar o Pokémon."


@st.cache_data(show_spinner=False, ttl=3600)
def buscar_especie(pokemon_id: int):
    try:
        resposta = requests.get(f"{API_BASE}/pokemon-species/{pokemon_id}", timeout=10)
        if resposta.status_code == 200:
            return resposta.json()
    except requests.RequestException:
        pass
    return None


def descricao_da_especie(especie):
    if not especie:
        return None
    for idioma in ("pt-br", "pt", "en"):
        for entrada in especie.get("flavor_text_entries", []):
            if entrada["language"]["name"] == idioma:
                return entrada["flavor_text"].replace("\n", " ").replace("\f", " ")
    return None


def cor_do_stat(valor: int) -> str:
    if valor < 50:
        return "#E74C3C"
    if valor < 80:
        return "#F39C12"
    if valor < 110:
        return "#2ECC71"
    return "#3498DB"


def escolher_nome(nome: str):
    st.session_state["pokemon_atual"] = nome


# ----------------------------------------------------------------------------
# Estado e barra lateral
# ----------------------------------------------------------------------------
if "pokemon_atual" not in st.session_state:
    st.session_state["pokemon_atual"] = "pikachu"

with st.sidebar:
    st.header("🔎 Buscar Pokémon")

    with st.form("form_busca", clear_on_submit=False):
        entrada = st.text_input(
            "Digite o nome do Pokémon",
            placeholder="Ex.: charizard",
        )
        enviar = st.form_submit_button("Pesquisar", use_container_width=True)

    if enviar and entrada.strip():
        escolher_nome(normalizar_nome(entrada))

    if st.button("🎲 Pokémon aleatório", use_container_width=True):
        escolher_nome(str(random.randint(1, 1025)))

    st.divider()
    st.subheader("⭐ Populares")
    colunas_pop = st.columns(2)
    for i, nome_pop in enumerate(POPULARES):
        colunas_pop[i % 2].button(
            nome_pop.capitalize(),
            key=f"pop_{nome_pop}",
            on_click=escolher_nome,
            args=(nome_pop,),
            use_container_width=True,
        )

    st.divider()
    mostrar_shiny = st.toggle("✨ Versão shiny", value=False)

# ----------------------------------------------------------------------------
# Corpo principal
# ----------------------------------------------------------------------------
st.markdown('<p class="titulo-app">Pokédex Interativa</p>', unsafe_allow_html=True)
st.caption("Dados fornecidos pela PokéAPI (pokeapi.co)")

with st.spinner("Consultando a PokéAPI..."):
    dados, erro = buscar_pokemon(st.session_state["pokemon_atual"])

if erro:
    st.error(f"❌ {erro}")
    st.info("Verifique a grafia do nome ou utilize o botão de Pokémon aleatório.")
    st.stop()

# Informações básicas
tipos = [t["type"]["name"] for t in dados["types"]]
cor_principal = CORES_TIPOS.get(tipos[0], "#777777")
cor_secundaria = CORES_TIPOS.get(tipos[-1], cor_principal)

artwork = dados["sprites"]["other"]["official-artwork"]
imagem = (
    artwork.get("front_shiny") if mostrar_shiny else artwork.get("front_default")
) or dados["sprites"].get("front_default")

altura_m = dados["height"] / 10
peso_kg = dados["weight"] / 10

# Cartão de destaque
col_img, col_info = st.columns([1, 1.3], gap="large")

with col_img:
    if imagem:
        st.image(imagem, use_container_width=True)
    audio = (dados.get("cries") or {}).get("latest")
    if audio:
        st.caption("🔊 Grito do Pokémon")
        st.audio(audio)

with col_info:
    badges = "".join(
        f'<span class="badge-tipo" style="background:{CORES_TIPOS.get(t, "#777")}">'
        f'{TRADUCAO_TIPOS.get(t, t.capitalize())}</span>'
        for t in tipos
    )
    st.markdown(
        f"""
        <div class="cartao-pokemon"
             style="background: linear-gradient(135deg, {cor_principal}, {cor_secundaria});">
            <div class="numero-pokemon">#{dados['id']:04d}</div>
            <div class="nome-pokemon">{dados['name'].replace('-', ' ')}</div>
            <div style="margin-top:10px">{badges}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    m1, m2, m3 = st.columns(3)
    m1.metric("Altura", f"{altura_m:.1f} m")
    m2.metric("Peso", f"{peso_kg:.1f} kg")
    m3.metric("Exp. base", dados.get("base_experience") or "—")

    especie = buscar_especie(dados["id"])
    texto = descricao_da_especie(especie)
    if texto:
        st.info(f"📖 {texto}")

# ----------------------------------------------------------------------------
# Abas
# ----------------------------------------------------------------------------
aba_stats, aba_hab, aba_golpes, aba_sprites = st.tabs(
    ["📊 Estatísticas", "🧠 Habilidades", "⚔️ Golpes", "🖼️ Sprites"]
)

with aba_stats:
    total = 0
    for item in dados["stats"]:
        valor = item["base_stat"]
        total += valor
        nome_stat = NOMES_STATS.get(item["stat"]["name"], item["stat"]["name"])
        largura = min(valor / 255 * 100, 100)
        st.markdown(
            f"""
            <div class="stat-linha">
                <div class="stat-nome">{nome_stat}</div>
                <div class="stat-valor">{valor}</div>
                <div class="stat-trilho">
                    <div class="stat-barra"
                         style="width:{largura}%; background:{cor_do_stat(valor)};"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown(f"**Total:** {total}")

    df_stats = pd.DataFrame(
        {
            "Atributo": [NOMES_STATS.get(s["stat"]["name"], s["stat"]["name"]) for s in dados["stats"]],
            "Valor": [s["base_stat"] for s in dados["stats"]],
        }
    ).set_index("Atributo")
    with st.expander("Ver gráfico de barras"):
        st.bar_chart(df_stats, color=cor_principal)

with aba_hab:
    st.subheader("Habilidades")
    chips = ""
    for h in dados["abilities"]:
        oculta = " (oculta)" if h["is_hidden"] else ""
        chips += f'<span class="chip-habilidade">{h["ability"]["name"].replace("-", " ")}{oculta}</span>'
    st.markdown(chips, unsafe_allow_html=True)

with aba_golpes:
    st.subheader(f"Golpes ({len(dados['moves'])})")
    nomes_golpes = sorted(m["move"]["name"].replace("-", " ").title() for m in dados["moves"])
    filtro = st.text_input("Filtrar golpes", placeholder="Ex.: thunder")
    if filtro:
        nomes_golpes = [g for g in nomes_golpes if filtro.lower() in g.lower()]
    st.caption(f"{len(nomes_golpes)} golpe(s) exibido(s)")
    st.dataframe(
        pd.DataFrame({"Golpe": nomes_golpes}),
        use_container_width=True,
        hide_index=True,
        height=350,
    )

with aba_sprites:
    st.subheader("Galeria de sprites")
    rotulos = {
        "front_default": "Frente",
        "back_default": "Costas",
        "front_shiny": "Frente (shiny)",
        "back_shiny": "Costas (shiny)",
    }
    disponiveis = [(r, dados["sprites"].get(k)) for k, r in rotulos.items() if dados["sprites"].get(k)]
    if disponiveis:
        colunas = st.columns(len(disponiveis))
        for coluna, (rotulo, url) in zip(colunas, disponiveis):
            coluna.image(url, caption=rotulo, width=140)
    else:
        st.write("Nenhum sprite disponível para este Pokémon.")