# QuantLab

QuantLab est une application d’analyse quantitative développée en **Python** et **Streamlit**, organisée en modules pédagogiques pour explorer les principaux outils utilisés en finance de marché : pricing d’options, simulations, stratégies, optimisation et analyse du risque.

---

## 🚀 Fonctionnalités principales

### 📈 Black–Scholes
- Interface dédiée au pricing d’options européennes
- Paramétrage interactif (spot, strike, maturité, taux, volatilité…)
- Visualisation de l’impact des paramètres sur le prix

### 🎲 Monte Carlo
- Simulation de trajectoires de prix
- Estimation du prix d’options par simulation
- Visualisation des trajectoires et de la distribution des résultats

### 🧠 Stratégies
- Construction de stratégies simples à partir d’options (ex : call spread, put spread, straddle…)
- Visualisation des profils de payoff
- Paramétrage des strikes et quantités

### 📊 Optimisation
- Module dédié à l’optimisation de portefeuille (structure en place)
- Base pour intégrer des algorithmes d’optimisation (Markowitz, contraintes, etc.)

### ⚠️ Analyse du risque
- Structure prévue pour des indicateurs de risque (VaR, CVaR, drawdown, etc.)
- Point d’entrée pour développer des outils de risk management

### 📉 Backtest
- Module prévu pour tester des stratégies dans le temps
- Base pour intégrer des données de marché et des règles de trading

### 🧠 Architecture du projet
```text
QuantLab/
├── app.py
├── OptionLab_py/ │   ├── _01_dataloader/ │
                      ├── _02_Pricing/ │
                      ├── _03_Risk/ │
                      ├── _04_utils/ │
                      └── _05_strategies/ │
├── OptionLab_pages/ │    ├── _Home.py │
                          ├── _0_BlackScholes.py │
                          ├── _1_MonteCarlo.py │
                          ├── _2_Strategies.py │
                          ├── _3_Optimisation.py │
                          ├── _4_RiskAnalysis.py │
                          └── _5_Backtest.py │
├── README.md
├── LICENSE
└── .gitignore
```
## 🛠️ Technologies utilisées

- **Langage :** Python  
- **Interface :** Streamlit  
- **Analyse & calcul :** NumPy, Pandas, SciPy  
- **Visualisation :** Matplotlib, Plotly  
- **Données de marché :** yfinance 
---

