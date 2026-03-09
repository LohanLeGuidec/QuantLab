import streamlit as st
import importlib

st.set_page_config(
    page_title="QuantLab",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("📊 Navigation")

menu = {
    "🧮 OptionLab": {
        "Dashboard": "OptionLab_pages._Home",
        "Black-Scholes": "OptionLab_pages._0_BlackScholes",
        "Monte Carlo": "OptionLab_pages._1_MonteCarlo",
        "Strategies": "OptionLab_pages._2_Strategies",
        "Optimisation": "OptionLab_pages._3_Optimisation",
        "Risk Analysis": "OptionLab_pages._4_RiskAnalysis",
        "Backtesting": "OptionLab_pages._5_Backtest",
    },

}

# --- MENU PRINCIPAL ---
section = st.sidebar.selectbox("Module :", list(menu.keys()))

# --- SOUS-MENU ---
page = st.sidebar.radio("Pages :", list(menu[section].keys()))

# --- IMPORT DYNAMIQUE ---
module_path = menu[section][page]
module = importlib.import_module(module_path)

# --- EXECUTION DE LA PAGE ---
module.run()