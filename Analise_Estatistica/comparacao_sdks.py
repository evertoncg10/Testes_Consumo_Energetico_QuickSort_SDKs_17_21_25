import os
import numpy as np
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.multitest import multipletests
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
    
    # 2. Testes de Premissas (Shapiro-Wilk e Levene)
    print("\n--- Testes de Premissas (Energia J) ---")
    shapiro_17 = stats.shapiro(e17)
    shapiro_21 = stats.shapiro(e21)
    shapiro_25 = stats.shapiro(e25)
    print(f"Shapiro-Wilk JDK 17: stat={shapiro_17.statistic:.4f}, p-value={shapiro_17.pvalue:.4f}")
    print(f"Shapiro-Wilk JDK 21: stat={shapiro_21.statistic:.4f}, p-value={shapiro_21.pvalue:.4f}")
    print(f"Shapiro-Wilk JDK 25: stat={shapiro_25.statistic:.4f}, p-value={shapiro_25.pvalue:.4f}")
    
    levene_test = stats.levene(e17, e21, e25)
    print(f"Levene (homocedasticidade): stat={levene_test.statistic:.4f}, p-value={levene_test.pvalue:.4f}")
    
    global_normal = (shapiro_17.pvalue >= 0.05) and (shapiro_21.pvalue >= 0.05) and (shapiro_25.pvalue >= 0.05)
    global_homogeneo = (levene_test.pvalue >= 0.05)
    
    # 3. Teste Global (ANOVA ou Kruskal-Wallis)
    print("\n--- Teste de Hipóteses Global (Energia J) ---")
    if global_normal and global_homogeneo:
        print("Premissas atendidas. Executando ANOVA One-Way...")
        print("H0: u_17 = u_21 = u_25 (Não há diferença estatisticamente significativa no consumo)")
        print("H1: Pelo menos uma média é estatisticamente diferente")
        
        f_val, p_val_global = stats.f_oneway(e17, e21, e25)
        print(f"Estatística F: {f_val:.4f}")
        print(f"p-value ANOVA: {p_val_global:.4e}")
        rejeita_h0_global = p_val_global < 0.05
        
        # Teste Post-Hoc: Tukey HSD
        print("\n--- Teste Post-Hoc: Tukey HSD (Energia J) ---")
        data_concat = np.concatenate([e17, e21, e25])
        groups_concat = (['JDK 17'] * len(e17)) + (['JDK 21'] * len(e21)) + (['JDK 25'] * len(e25))
        tukey = pairwise_tukeyhsd(endog=data_concat, groups=groups_concat, alpha=0.05)
        print(tukey)
        
        tukey_results = tukey
        dunn_mw_results = None
        global_stat = f_val
    else:
        print("Premissas violadas. Executando Teste de Kruskal-Wallis...")
        print("H0: As distribuições de consumo de energia são idênticas (medianas iguais)")
        print("H1: Pelo menos uma distribuição (mediana) é diferente")
        
        kw_stat, p_val_global = stats.kruskal(e17, e21, e25)
        print(f"Estatística H (Kruskal-Wallis): {kw_stat:.4f}")
        print(f"p-value Kruskal-Wallis: {p_val_global:.4e}")
        rejeita_h0_global = p_val_global < 0.05
        
        # Teste Post-Hoc: Mann-Whitney U pareados com correção Holm-Bonferroni
        print("\n--- Teste Post-Hoc: Mann-Whitney U Pareados (Holm-Bonferroni) ---")
        p_17_21 = stats.mannwhitneyu(e17, e21, alternative='two-sided').pvalue
        p_17_25 = stats.mannwhitneyu(e17, e25, alternative='two-sided').pvalue
        p_21_25 = stats.mannwhitneyu(e21, e25, alternative='two-sided').pvalue
        
        p_vals_raw = [p_17_21, p_17_25, p_21_25]
        reject_corrected, p_vals_corrected, _, _ = multipletests(p_vals_raw, alpha=0.05, method='holm')
        
        pairs = ["JDK 17 vs JDK 21", "JDK 17 vs JDK 25", "JDK 21 vs JDK 25"]
        print(f"{'Comparação':<20} | {'p-val Bruto':<12} | {'p-val Corrigido':<15} | {'Rejeita H0':<10}")
        print("-" * 65)
        for i, pair in enumerate(pairs):
            print(f"{pair:<20} | {p_vals_raw[i]:<12.4f} | {p_vals_corrected[i]:<15.4f} | {str(reject_corrected[i]):<10}")
            
        tukey_results = None
        dunn_mw_results = []
        for i, pair in enumerate(pairs):
            dunn_mw_results.append({
                'pair': pair,
                'p_raw': p_vals_raw[i],
                'p_adj': p_vals_corrected[i],
                'reject': bool(reject_corrected[i])
            })
        global_stat = kw_stat
        
    if rejeita_h0_global:
        print("DECISÃO: p-value < 0.05. REJEITA-SE H0.")
    else:
        print("DECISÃO: p-value >= 0.05. FALHA EM REJEITAR H0.")
        
    # 4. Comparação Crítica A (Java 17 vs Java 21)
    print("\n--- Comparação Crítica A: Transição LTS (Java 17 vs Java 21) ---")
    comp_a_normal = (shapiro_17.pvalue >= 0.05) and (shapiro_21.pvalue >= 0.05)
    
    if comp_a_normal:
        levene_a = stats.levene(e17, e21)
        eq_var_a = levene_a.pvalue >= 0.05
        if eq_var_a:
            comp_a_teste = "Teste t (Student, Variâncias Iguais)"
            t_stat, p_comp_a = stats.ttest_ind(e17, e21, equal_var=True)
        else:
            comp_a_teste = "Teste t (Welch, Variâncias Desiguais)"
            t_stat, p_comp_a = stats.ttest_ind(e17, e21, equal_var=False)
        comp_a_stat = t_stat
    else:
        comp_a_teste = "Mann-Whitney U"
        mw_stat, p_comp_a = stats.mannwhitneyu(e17, e21, alternative='two-sided')
        comp_a_stat = mw_stat
        
    print(f"Teste Utilizado: {comp_a_teste}")
    print(f"Média JDK 17: {np.mean(e17):.2f} J | Média JDK 21: {np.mean(e21):.2f} J")
    print(f"Diferença das Médias: {np.mean(e21) - np.mean(e17):.2f} J")
    print(f"Estatística: {comp_a_stat:.4f}, p-value = {p_comp_a:.4f}")
    
    if p_comp_a < 0.05:
        print("Decisão: Rejeita-se H0. Existe diferença estatisticamente significativa na transição LTS.")
    else:
        print("Decisão: Falha em rejeitar H0. Não há diferença estatisticamente significativa na transição LTS.")
        print("Nota Analítica: Estatisticamente, a versão 21 manteve a estabilidade de consumo e não gerou regressão energética em relação ao Java 17.")
        
    # 5. Comparação Crítica B (O Salto Moderno: Java 17 vs Java 25)
    print("\n--- Comparação Crítica B: O Salto Moderno (Java 17 vs Java 25) ---")
    comp_b_normal = (shapiro_17.pvalue >= 0.05) and (shapiro_25.pvalue >= 0.05)
    
    if comp_b_normal:
        levene_b = stats.levene(e17, e25)
        eq_var_b = levene_b.pvalue >= 0.05
        if eq_var_b:
            comp_b_teste = "Teste t (Student, Variâncias Iguais)"
            t_stat, p_comp_b = stats.ttest_ind(e17, e25, equal_var=True)
        else:
            comp_b_teste = "Teste t (Welch, Variâncias Desiguais)"
            t_stat, p_comp_b = stats.ttest_ind(e17, e25, equal_var=False)
        comp_b_stat = t_stat
    else:
        comp_b_teste = "Mann-Whitney U"
        mw_stat, p_comp_b = stats.mannwhitneyu(e17, e25, alternative='two-sided')
        comp_b_stat = mw_stat
        
    print(f"Teste Utilizado: {comp_b_teste}")
    print(f"Média JDK 17: {np.mean(e17):.2f} J | Média JDK 25: {np.mean(e25):.2f} J")
    print(f"Diferença das Médias: {np.mean(e25) - np.mean(e17):.2f} J")
    print(f"Estatística: {comp_b_stat:.4f}, p-value = {p_comp_b:.4f}")
    
    if p_comp_b < 0.05:
        print("Decisão: Rejeita-se H0. Existe diferença estatisticamente significativa no salto moderno.")
        if np.mean(e25) > np.mean(e17):
            print("Nota Analítica: Como a média do Java 25 foi maior que a do Java 17, conclui-se estatisticamente que a evolução para o Java 25 resultou em maior consumo (menor eficiência) sob estresse contínuo.")
        else:
            print("Nota Analítica: O Java 25 apresentou menor consumo médio em relação ao Java 17.")
    else:
        print("Decisão: Falha em rejeitar H0. Não há diferença estatisticamente significativa no salto moderno.")
        
    # 6. Avaliação de Ganho de Eficiência no Warm-up (Apenas Primeiras 10 Execuções: Java 17 vs Java 25)
    print("\n--- Teste de Hipótese: Warm-up (Primeiras 10 Execuções, Java 17 vs Java 25) ---")
    print("H0: u_Java25 >= u_Java17 (O Java 25 consome o mesmo ou mais que o Java 17 no início)")
    print("H1: u_Java25 < u_Java17 (O Java 25 consome significativamente menos energia no início)")
    
    e17_warm = e17[:10]
    e25_warm = e25[:10]
    
    shapiro_17_w = stats.shapiro(e17_warm)
    shapiro_25_w = stats.shapiro(e25_warm)
    print(f"Shapiro-Wilk Warm-up JDK 17: p-value = {shapiro_17_w.pvalue:.4f}")
    print(f"Shapiro-Wilk Warm-up JDK 25: p-value = {shapiro_25_w.pvalue:.4f}")
    
    warmup_normal = (shapiro_17_w.pvalue >= 0.05) and (shapiro_25_w.pvalue >= 0.05)
    
    if warmup_normal:
        levene_w = stats.levene(e17_warm, e25_warm)
        eq_var_w = levene_w.pvalue >= 0.05
        if eq_var_w:
            warmup_teste = "Teste t (Student, Unilateral, Variâncias Iguais)"
            t_stat_w, warmup_pval = stats.ttest_ind(e25_warm, e17_warm, equal_var=True, alternative='less')
        else:
            warmup_teste = "Teste t (Welch, Unilateral, Variâncias Desiguais)"
            t_stat_w, warmup_pval = stats.ttest_ind(e25_warm, e17_warm, equal_var=False, alternative='less')
        warmup_stat = t_stat_w
    else:
        warmup_teste = "Mann-Whitney U (Unilateral)"
        mw_stat_w, warmup_pval = stats.mannwhitneyu(e25_warm, e17_warm, alternative='less')
        warmup_stat = mw_stat_w
        
    print(f"Teste Utilizado: {warmup_teste}")
    print(f"Média Warm-up JDK 17 (n=10): {np.mean(e17_warm):.2f} J")
    print(f"Média Warm-up JDK 25 (n=10): {np.mean(e25_warm):.2f} J")
    print(f"Diferença das Médias: {np.mean(e25_warm) - np.mean(e17_warm):.2f} J")
    print(f"Estatística: {warmup_stat:.4f}, p-value = {warmup_pval:.4e}")
    
    if warmup_pval < 0.05:
        print("Decisão: Rejeita-se H0. Existe ganho de eficiência estatisticamente comprovado de Java 25 em relação ao Java 17 no Warm-up.")
    else:
        print("Decisão: Falha em rejeitar H0. Não há ganho de eficiência estatisticamente comprovado no Warm-up.")

    # 7. Geração dos Gráficos Comparativos
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
        'premissas': {
            'shapiro': {
                'JDK 17': {'stat': shapiro_17.statistic, 'p_val': shapiro_17.pvalue, 'normal': bool(shapiro_17.pvalue >= 0.05)},
                'JDK 21': {'stat': shapiro_21.statistic, 'p_val': shapiro_21.pvalue, 'normal': bool(shapiro_21.pvalue >= 0.05)},
                'JDK 25': {'stat': shapiro_25.statistic, 'p_val': shapiro_25.pvalue, 'normal': bool(shapiro_25.pvalue >= 0.05)}
            },
            'levene': {'stat': levene_test.statistic, 'p_val': levene_test.pvalue, 'homogeneo': bool(levene_test.pvalue >= 0.05)}
        },
        'global': {
            'teste_usado': 'ANOVA' if global_normal and global_homogeneo else 'Kruskal-Wallis',
            'stat': global_stat,
            'p_val': p_val_global,
            'rejeita': bool(rejeita_h0_global),
            'tukey': tukey_results,
            'dunn_mw': dunn_mw_results
        },
        'comp_a': {
            'teste_usado': comp_a_teste,
            'stat': comp_a_stat,
            'p_val': p_comp_a,
            'rejeita': bool(p_comp_a < 0.05),
            'media_17': np.mean(e17),
            'media_21': np.mean(e21)
        },
        'comp_b': {
            'teste_usado': comp_b_teste,
            'stat': comp_b_stat,
            'p_val': p_comp_b,
            'rejeita': bool(p_comp_b < 0.05),
            'media_17': np.mean(e17),
            'media_25': np.mean(e25)
        },
        'warmup': {
            'teste_usado': warmup_teste,
            'stat': warmup_stat,
            'p_val': warmup_pval,
            'rejeita': bool(warmup_pval < 0.05),
            'media_17': np.mean(e17_warm),
            'media_25': np.mean(e25_warm),
            'shapiro_17_p': shapiro_17_w.pvalue,
            'shapiro_25_p': shapiro_25_w.pvalue
        }
    }

if __name__ == '__main__':
    executar_comparacao()
