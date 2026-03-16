import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="Simulador PRO - Vendas", layout="wide")

st.title("📊 Simulador Estratégico de Vendas")

# --- 1. PARÂMETROS COMPACTOS (Menu Superior) ---
with st.expander("⚙️ Parâmetros do Plano (Clique para expandir/ocultar)", expanded=True):
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: valor_carta = st.number_input("Carta (R$)", min_value=10000.0, value=300000.0, step=5000.0)
    with c2: prazo = st.number_input("Prazo (Meses)", min_value=12, value=220, step=12)
    with c3: taxa_adm = st.number_input("Taxa Adm (%)", min_value=0.0, value=24.2, step=0.5)
    with c4: fundo_res = st.number_input("Fundo Res. (%)", min_value=0.0, value=2.0, step=0.5)
    with c5: incc_anual = st.number_input("INCC/INPC Anual (%)", min_value=0.0, value=5.0, step=0.5)
    
    c6, c7, c8, c9, c10 = st.columns(5)
    with c6: plano_reduzido = st.selectbox("Parcela Inicial", ["Integral (100%)", "Reduzida (70%)", "Meia (50%)"])
    with c7: mes_contemplacao = st.number_input("Mês Contemplação", min_value=1, value=24, step=1)
    with c8: lance_proprio = st.number_input("Lance Próprio (R$)", min_value=0.0, value=15000.0, step=1000.0)
    with c9: percentual_embutido = st.number_input("Embutido (%)", min_value=0.0, max_value=50.0, value=20.0, step=1.0)
    with c10: opcao_amortizacao = st.selectbox("Amortização", ["Abater na Parcela", "Abater no Prazo"])

# --- CÁLCULOS GERAIS PARA AS DUAS PÁGINAS ---
fator_reducao = 1.0
if "70%" in plano_reduzido: fator_reducao = 0.70
elif "50%" in plano_reduzido: fator_reducao = 0.50

taxa_total_perc = taxa_adm + fundo_res
custo_total_cons_base = valor_carta * (1 + (taxa_total_perc / 100))
parcela_inicial_cons = (custo_total_cons_base / prazo) * fator_reducao

# Cálculos do Financiamento IMOBILIÁRIO (30% entrada, 14% a.a, 420 meses)
entrada_fin_imob = valor_carta * 0.20
valor_financiado_imob = valor_carta - entrada_fin_imob
juros_mes_imob = 0.14 / 12
meses_fin_imob = 420
parcela_inicial_fin_imob = valor_financiado_imob * (juros_mes_imob * (1 + juros_mes_imob)**meses_fin_imob) / ((1 + juros_mes_imob)**meses_fin_imob - 1)
total_fin_imob = (parcela_inicial_fin_imob * meses_fin_imob) + entrada_fin_imob

# Cálculos do Financiamento de VEÍCULOS (30% entrada, 30% a.a, 60 meses)
entrada_fin_veiculo = valor_carta * 0.20
valor_financiado_veiculo = valor_carta - entrada_fin_veiculo
juros_mes_veiculo = 0.30 / 12
meses_fin_veiculo = 60
parcela_inicial_fin_veiculo = valor_financiado_veiculo * (juros_mes_veiculo * (1 + juros_mes_veiculo)**meses_fin_veiculo) / ((1 + juros_mes_veiculo)**meses_fin_veiculo - 1)
total_fin_veiculo = (parcela_inicial_fin_veiculo * meses_fin_veiculo) + entrada_fin_veiculo

# --- CRIANDO AS PÁGINAS (ABAS) ---
tab1, tab2 = st.tabs(["⚖️ Comparativo (Financiamento x Consórcio)", "📈 Detalhes da Contemplação e Reajuste"])

# ==========================================
# PÁGINA 1: O CHOQUE DE REALIDADE
# ==========================================
with tab1:
    st.markdown("### Análise Financeira: Como o mercado cobra pelo crédito")
    st.markdown("Comparativo direto para aquisição de um bem no valor de **R$ {:,.2f}**".format(valor_carta).replace(",", "X").replace(".", ",").replace("X", "."))
    
    # Cálculo do CET Anual do Consórcio
    anos_plano = prazo / 12
    cet_anual_consorcio = taxa_total_perc / anos_plano
    cet_formatado = f"{cet_anual_consorcio:.2f}".replace(".", ",")
    
    # --- TABELA 1: IMÓVEIS ---
    st.markdown("#### 🏡 Cenário 1: Aquisição de Imóvel")
    st.markdown(f"""
    <table style="width:100%; text-align:left; font-size:16px; border-collapse: collapse; margin-bottom: 20px;">
        <tr style="background-color: #f0f2f6; border-bottom: 2px solid #ccc;">
            <th style="padding: 12px; width: 25%;">Parâmetro</th>
            <th style="padding: 12px; color: #d9534f; width: 37%;">🏦 Financiamento (CET 14% a.a)</th>
            <th style="padding: 12px; color: #5cb85c; width: 38%;">🚀 Consórcio (CET {cet_formatado}% a.a)</th>
        </tr>
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px;"><b>Valor de Entrada</b></td>
            <td style="padding: 12px;">R$ {entrada_fin_imob:,.2f}</td>
            <td style="padding: 12px; font-weight: bold; color: #5cb85c;">R$ 0,00</td>
        </tr>
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px;"><b>Parcela Inicial</b></td>
            <td style="padding: 12px;">R$ {parcela_inicial_fin_imob:,.2f}</td>
            <td style="padding: 12px;">R$ {parcela_inicial_cons:,.2f}</td>
        </tr>
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px;"><b>Custo Total</b></td>
            <td style="padding: 12px; color: #d9534f; font-weight: bold;">R$ {total_fin_imob:,.2f}</td>
            <td style="padding: 12px; font-weight: bold;">R$ {custo_total_cons_base:,.2f}</td>
        </tr>
        <tr>
            <td style="padding: 12px;"><b>Prazo</b></td>
            <td style="padding: 12px;">{meses_fin_imob} meses</td>
            <td style="padding: 12px;">{prazo} meses</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    # --- TABELA 2: VEÍCULOS ---
    st.markdown("#### 🚗 Cenário 2: Aquisição de Veículo (Pesados ou Leves)")
    st.markdown(f"""
    <table style="width:100%; text-align:left; font-size:16px; border-collapse: collapse;">
        <tr style="background-color: #f0f2f6; border-bottom: 2px solid #ccc;">
            <th style="padding: 12px; width: 25%;">Parâmetro</th>
            <th style="padding: 12px; color: #d9534f; width: 37%;">🏦 Financiamento (CET 30% a.a)</th>
            <th style="padding: 12px; color: #5cb85c; width: 38%;">🚀 Consórcio (CET {cet_formatado}% a.a)</th>
        </tr>
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px;"><b>Valor de Entrada</b></td>
            <td style="padding: 12px;">R$ {entrada_fin_veiculo:,.2f}</td>
            <td style="padding: 12px; font-weight: bold; color: #5cb85c;">R$ 0,00</td>
        </tr>
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px;"><b>Parcela Inicial</b></td>
            <td style="padding: 12px;">R$ {parcela_inicial_fin_veiculo:,.2f}</td>
            <td style="padding: 12px;">R$ {parcela_inicial_cons:,.2f}</td>
        </tr>
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 12px;"><b>Custo Total</b></td>
            <td style="padding: 12px; color: #d9534f; font-weight: bold;">R$ {total_fin_veiculo:,.2f}</td>
            <td style="padding: 12px; font-weight: bold;">R$ {custo_total_cons_base:,.2f}</td>
        </tr>
        <tr>
            <td style="padding: 12px;"><b>Prazo</b></td>
            <td style="padding: 12px;">{meses_fin_veiculo} meses</td>
            <td style="padding: 12px;">{prazo} meses</td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
    
    st.caption("*Nota: O custo total do consórcio representa o crédito somado às taxas administrativas. O prazo do consórcio é o mesmo para ambos os comparativos, baseado nos parâmetros preenchidos.*")

# ==========================================
# PÁGINA 2: DETALHES, INCC E AMORTIZAÇÃO
# ==========================================
with tab2:
    st.subheader("💡 A Mágica da Correção: Projeção de Patrimônio (3 Primeiros Anos)")
    st.markdown("Veja como a valorização da sua carta supera o reajuste pago nas parcelas.")
    
    c_ano1 = valor_carta
    p_ano1 = parcela_inicial_cons
    
    c_ano2 = c_ano1 * (1 + (incc_anual / 100))
    p_ano2 = p_ano1 * (1 + (incc_anual / 100))
    aumento_pago_ano2 = (p_ano2 - p_ano1) * 12
    ganho_carta_ano2 = c_ano2 - c_ano1
    lucro_ano2 = ganho_carta_ano2 - aumento_pago_ano2
    
    c_ano3 = c_ano2 * (1 + (incc_anual / 100))
    p_ano3 = p_ano2 * (1 + (incc_anual / 100))
    aumento_pago_ano3 = (p_ano3 - p_ano2) * 12
    ganho_carta_ano3 = c_ano3 - c_ano2
    lucro_ano3 = ganho_carta_ano3 - aumento_pago_ano3
    
    dados_projecao = [
        {"Período": "Ano 1", "Parcela Mensal": p_ano1, "Pago a Mais (12m)": 0.0, "Novo Valor da Carta": c_ano1, "Lucro na Valorização": 0.0},
        {"Período": "Ano 2", "Parcela Mensal": p_ano2, "Pago a Mais (12m)": aumento_pago_ano2, "Novo Valor da Carta": c_ano2, "Lucro na Valorização": lucro_ano2},
        {"Período": "Ano 3", "Parcela Mensal": p_ano3, "Pago a Mais (12m)": aumento_pago_ano3, "Novo Valor da Carta": c_ano3, "Lucro na Valorização": lucro_ano3}
    ]
    
    df_projecao = pd.DataFrame(dados_projecao)
    df_projecao_fmt = df_projecao.style.format({
        "Parcela Mensal": "R$ {:,.2f}", 
        "Pago a Mais (12m)": "R$ {:,.2f}", 
        "Novo Valor da Carta": "R$ {:,.2f}", 
        "Lucro na Valorização": "R$ {:,.2f}"
    }).map(lambda x: 'color: #5cb85c; font-weight: bold;' if x > 0 else '', subset=['Lucro na Valorização'])
    
    st.dataframe(df_projecao_fmt, use_container_width=True, hide_index=True)

    # --- SIMULAÇÃO DA AMORTIZAÇÃO (Background Math) ---
    carta_atual = valor_carta
    saldo_devedor = carta_atual * (1 + (taxa_total_perc / 100))
    parcela_base_cheia = saldo_devedor / prazo
    parcela_atual = parcela_base_cheia * fator_reducao
    meses_restantes = prazo
    tabela_dados = []
    
    carta_na_contemplacao = 0
    lance_embutido_reais = 0
    credito_liquido = 0
    lance_total = 0

    for mes in range(1, prazo + 1):
        if meses_restantes <= 0 or saldo_devedor <= 0.01:
            break

        lance_pago_mes = 0.0
        
        if mes > 1 and (mes - 1) % 12 == 0:
            fator_incc = 1 + (incc_anual / 100)
            carta_atual *= fator_incc
            saldo_devedor *= fator_incc 
            
            if mes <= mes_contemplacao:
                parcela_atual = (saldo_devedor / meses_restantes) * fator_reducao
            else:
                parcela_atual = saldo_devedor / meses_restantes

        if mes == mes_contemplacao:
            carta_na_contemplacao = carta_atual
            fator_reducao = 1.00
            
            lance_embutido_reais = carta_atual * (percentual_embutido / 100)
            lance_total = lance_proprio + lance_embutido_reais
            credito_liquido = carta_atual - lance_embutido_reais
            
            if lance_total > 0:
                lance_pago_mes = lance_total
                saldo_devedor -= lance_pago_mes
                
                if opcao_amortizacao == "Abater na Parcela":
                    parcela_atual = saldo_devedor / meses_restantes
                elif opcao_amortizacao == "Abater no Prazo":
                    parcela_atual = saldo_devedor / meses_restantes if plano_reduzido != "Integral (100%)" else parcela_atual
                    meses_restantes = math.ceil(saldo_devedor / parcela_atual)
            else:
                 parcela_atual = saldo_devedor / meses_restantes
                 
        if parcela_atual > saldo_devedor:
            parcela_atual = saldo_devedor
            
        saldo_devedor -= parcela_atual
        meses_restantes -= 1
        
        tabela_dados.append({
            "Mês": mes, "Valor da Carta": carta_atual, "Parcela": parcela_atual,
            "Lance Total Pago": lance_pago_mes, "Saldo Devedor": max(0, saldo_devedor)
        })

    # --- RESUMO DA CONTEMPLAÇÃO ---
    st.divider()
    st.header(f"🎯 Resumo da Contemplação (Mês {mes_contemplacao})")
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("Crédito Bruto (Atualizado)", f"R$ {carta_na_contemplacao:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col_res2:
        st.metric("Lance Total Ofertado", f"R$ {lance_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    with col_res3:
        st.metric("Crédito Líquido Liberado", f"R$ {credito_liquido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    # --- TABELA DE AMORTIZAÇÃO ---
    st.subheader("🗓️ Tabela de Amortização Projetada")
    df_tabela = pd.DataFrame(tabela_dados)
    df_tabela_fmt = df_tabela.style.format({
        "Valor da Carta": "R$ {:,.2f}", "Parcela": "R$ {:,.2f}",
        "Lance Total Pago": "R$ {:,.2f}", "Saldo Devedor": "R$ {:,.2f}"
    }).map(lambda x: 'background-color: #d4edda; color: black' if x > 0 else '', subset=['Lance Total Pago'])
    
    st.dataframe(df_tabela_fmt, use_container_width=True, height=400)

    # --- RESULTADO OCULTO ---
    valor_total_pago = df_tabela["Parcela"].sum() + df_tabela["Lance Total Pago"].sum()
    with st.expander("👁️‍🗨️ Área Exclusiva do Consultor"):
        st.markdown(f"**Total Pago (Parcelas + Lance Próprio + Embutido):** R$ {valor_total_pago:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
