import os
import numpy as np
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import estatistica_utils as utils

def executar_comparacao():
    print("=" * 60)
    print("ANÁLISE COMPARATIVA GLOBAL ENTRE SDKS")
    print("=" * 60)
    
    # Caminhos de arquivos
    dados_dir = r"c:\Users\evert\Documents\0-Testes_Software_Verde\Testes_Versões_JDK_17_21_25\Testes_Consumo_Energetico_QuickSort_SDKs_17_21_25\Analise_Estatistica\dados"
    f17 = os.path.join(dados_dir, "Planilha_Dados_das_Execuções_JDK_17-0-18.xlsx")
    f21 = os.path.join(dados_dir, "Planilha_Dados_das_Execuções_JDK_21-0-10.xlsx")
    f25 = os.path.join(dados_dir, "Planilha_Dados_das_Execuções_JDK_25-0-2.xlsx")
    
    # Pasta de resultados
    graficos_dir = r"c:\Users\evert\Documents\0-Testes_Software_Verde\Testes_Versões_JDK_17_21_25\Testes_Consumo_Energetico_QuickSort_SDKs_17_21_25\Analise_Estatistica\resultados\graficos"
    
    # 1. Carregar dados
    df17 = utils.carregar_dados(f17)
    df21 = utils.carregar_dados(f21)
    df25 = utils.carregar_dados(f25)
    
    e17 = df17['Energia (J)'].dropna().values
    e21 = df21['Energia (J)'].dropna().values
    e25 = df25['Energia (J)'].dropna().values
    
    dados_dict = {
        'JDK 17': df17['Energia (J)'],
        'JDK 21': df21['Energia (J)'],
        'JDK 25': df25['Energia (J)']
    }
    
    # 2. ANOVA One-Way (Análise de Variância)
    print("\n--- Teste de Hipóteses Global: ANOVA One-Way (Energia J) ---")
    print("H0: As médias de consumo de energia são iguais nos três JDKs (u_17 = u_21 = u_25)")
    print("H1: Pelo menos uma média de consumo é estatisticamente diferente")
    
    f_val, p_val_anova = stats.f_oneway(e17, e21, e25)
    print(f"Estatística F: {f_val:.4f}")
    print(f"p-value ANOVA: {p_val_anova:.4e}")
    
    rejeita_h0_anova = p_val_anova < 0.05
    if rejeita_h0_anova:
        print("DECISÃO: p-value < 0.05. REJEITA-SE H0.")
        print("Conclusão: Há diferença estatisticamente significativa no consumo de energia entre as versões do JDK.")
    else:
        print("DECISÃO: p-value >= 0.05. FALHA EM REJEITAR H0.")
        print("Conclusão: Não há diferença estatisticamente significativa no consumo de energia entre as versões do JDK.")
        
    # 3. Teste Post-Hoc: Tukey HSD
    print("\n--- Teste Post-Hoc: Tukey HSD (Energia J) ---")
    data_concat = np.concatenate([e17, e21, e25])
    groups_concat = (['JDK 17'] * len(e17)) + (['JDK 21'] * len(e21)) + (['JDK 25'] * len(e25))
    
    tukey = pairwise_tukeyhsd(endog=data_concat, groups=groups_concat, alpha=0.05)
    print(tukey)
    
    # 4. Comparação Crítica A (Java 17 vs Java 21)
    print("\n--- Comparação Crítica A: Transição LTS (Java 17 vs Java 21) ---")
    print("H0: u_17 = u_21 (Não há diferença significativa no consumo de energia)")
    print("H1: u_17 != u_21 (Há diferença significativa)")
    
    # Teste t de duas amostras (Welch - variâncias desiguais e Student - variâncias iguais)
    t_welch, p_welch = stats.ttest_ind(e17, e21, equal_var=False)
    t_student, p_student = stats.ttest_ind(e17, e21, equal_var=True)
    
    print(f"Média JDK 17: {np.mean(e17):.2f} J | Média JDK 21: {np.mean(e21):.2f} J")
    print(f"Diferença das Médias: {np.mean(e21) - np.mean(e17):.2f} J")
    print(f"Teste t de Welch (Variâncias Desiguais): t-stat = {t_welch:.4f}, p-value = {p_welch:.4f}")
    print(f"Teste t de Student (Variâncias Iguais): t-stat = {t_student:.4f}, p-value = {p_student:.4f}")
    
    if p_welch < 0.05:
        print("Decisão: Rejeita-se H0. Existe diferença estatisticamente significativa na transição LTS.")
    else:
        print("Decisão: Falha em rejeitar H0. Não há diferença estatisticamente significativa na transição LTS.")
        print("Nota Analítica: Estatisticamente, a versão 21 manteve a estabilidade de consumo e não gerou regressão energética em relação ao Java 17.")
        
    # 5. Comparação Crítica B (O Salto Moderno: Java 17 vs Java 25)
    print("\n--- Comparação Crítica B: O Salto Moderno (Java 17 vs Java 25) ---")
    print("H0: u_17 = u_25 (As médias de consumo de energia são iguais)")
    print("H1: u_17 != u_25 (As médias de consumo são diferentes)")
    
    t_welch_b, p_welch_b = stats.ttest_ind(e17, e25, equal_var=False)
    t_student_b, p_student_b = stats.ttest_ind(e17, e25, equal_var=True)
    
    print(f"Média JDK 17: {np.mean(e17):.2f} J | Média JDK 25: {np.mean(e25):.2f} J")
    print(f"Diferença das Médias: {np.mean(e25) - np.mean(e17):.2f} J")
    print(f"Teste t de Welch (Variâncias Desiguais): t-stat = {t_welch_b:.4f}, p-value = {p_welch_b:.4f}")
    print(f"Teste t de Student (Variâncias Iguais): t-stat = {t_student_b:.4f}, p-value = {p_student_b:.4f}")
    
    if p_welch_b < 0.05:
        print("Decisão: Rejeita-se H0. Existe diferença estatisticamente significativa no salto moderno.")
        if np.mean(e25) > np.mean(e17):
            print("Nota Analítica: Como a média do Java 25 foi maior que a do Java 17, conclui-se estatisticamente que a evolução para o Java 25 resultou em maior consumo (menor eficiência) sob estresse contínuo.")
        else:
            print("Nota Analítica: O Java 25 apresentou menor consumo médio em relação ao Java 17.")
    else:
        print("Decisão: Falha em rejeitar H0. Não há diferença estatisticamente significativa no salto moderno.")

    # 6. Geração dos Gráficos Comparativos
    print("\n--- Gerando Visualizações Conjuntas ---")
    
    boxplot_path = os.path.join(graficos_dir, "comparacao_consumo_boxplot.png")
    utils.salvar_boxplot_comparativo(dados_dict, "Energia (J)", boxplot_path)
    print(f"Boxplot comparativo salvo em: {boxplot_path}")
    
    barras_path = os.path.join(graficos_dir, "comparacao_consumo_barras_ci.png")
    utils.salvar_grafico_barras_ci(dados_dict, "Energia (J)", barras_path)
    print(f"Gráfico de barras com CI salvo em: {barras_path}")
    
    histogramas_path = os.path.join(graficos_dir, "comparacao_distribuicao_hist_kde.png")
    utils.salvar_histogramas_lado_a_lado(dados_dict, "Energia (J)", histogramas_path)
    print(f"Histogramas lado a lado salvos em: {histogramas_path}")
    
    print("=" * 60 + "\n")
    
    # Retornar resultados dos testes para o relatório final
    return {
        'anova': {'f_val': f_val, 'p_val': p_val_anova, 'rejeita': rejeita_h0_anova},
        'comp_a': {'t_val': t_welch, 'p_val': p_welch, 'rejeita': p_welch < 0.05},
        'comp_b': {'t_val': t_welch_b, 'p_val': p_welch_b, 'rejeita': p_welch_b < 0.05}
    }

if __name__ == '__main__':
    executar_comparacao()
