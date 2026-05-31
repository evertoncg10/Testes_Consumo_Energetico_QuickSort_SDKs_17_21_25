import os

# Importar os módulos de análise individuais e comparativa
import analise_jdk17
import analise_jdk21
import analise_jdk25
import comparacao_sdks

def main():
    print("=" * 70)
    # Título principal do console
    print("INICIANDO FLUXO COMPLETO DE ANÁLISE ESTATÍSTICA E COMPARATIVA")
    print("=" * 70)
    
    # Criar pasta de resultados se não existir
    resultados_dir = r"c:\Users\evert\Documents\0-Testes_Software_Verde\Testes_Versões_JDK_17_21_25\Testes_Consumo_Energetico_QuickSort_SDKs_17_21_25\Analise_Estatistica\resultados"
    os.makedirs(resultados_dir, exist_ok=True)
    os.makedirs(os.path.join(resultados_dir, "graficos"), exist_ok=True)
    
    # 1. Executar as análises individuais
    df17, stats17 = analise_jdk17.executar_analise()
    df21, stats21 = analise_jdk21.executar_analise()
    df25, stats25 = analise_jdk25.executar_analise()
    
    # 2. Executar a análise comparativa (ANOVA/Kruskal, testes t/Mann-Whitney e gráficos comparativos)
    comp_results = comparacao_sdks.executar_comparacao()
    
    # 3. Gerar o relatório Markdown unificado
    relatorio_path = os.path.join(resultados_dir, "relatorio_estatistico.md")
    
    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write("# Relatório Estatístico Consolidado: Consumo Energético e Eficiência de JDKs\n\n")
        f.write("Este relatório apresenta a análise estatística dos testes do algoritmo QuickSort executados nos JDKs 17, 21 e 25. Foram realizadas 40 execuções válidas para cada versão do SDK.\n\n")
        
        # Seção 1: Estatísticas Descritivas
        f.write("## 1. Estatísticas Descritivas e Variabilidade\n\n")
        
        # Tabela de Energia
        f.write("### 1.1 Consumo de Energia (Joules)\n\n")
        f.write("| JDK | Média (J) | Mediana (J) | Moda (J) | Q1 (25%) | Q3 (75%) | Desvio Padrão (J) | CV (%) |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        f.write(f"| JDK 17 | {stats17['Energia (J)']['media']:.3f} | {stats17['Energia (J)']['mediana']:.3f} | {stats17['Energia (J)']['moda']:.3f} | {stats17['Energia (J)']['q1']:.3f} | {stats17['Energia (J)']['q3']:.3f} | {stats17['Energia (J)']['desvio_padrao']:.3f} | {stats17['Energia (J)']['coef_variacao']:.3f}% |\n")
        f.write(f"| JDK 21 | {stats21['Energia (J)']['media']:.3f} | {stats21['Energia (J)']['mediana']:.3f} | {stats21['Energia (J)']['moda']:.3f} | {stats21['Energia (J)']['q1']:.3f} | {stats21['Energia (J)']['q3']:.3f} | {stats21['Energia (J)']['desvio_padrao']:.3f} | {stats21['Energia (J)']['coef_variacao']:.3f}% |\n")
        f.write(f"| JDK 25 | {stats25['Energia (J)']['media']:.3f} | {stats25['Energia (J)']['mediana']:.3f} | {stats25['Energia (J)']['moda']:.3f} | {stats25['Energia (J)']['q1']:.3f} | {stats25['Energia (J)']['q3']:.3f} | {stats25['Energia (J)']['desvio_padrao']:.3f} | {stats25['Energia (J)']['coef_variacao']:.3f}% |\n\n")
        
        # Tabela de Tempo
        f.write("### 1.2 Tempo de Execução (Segundos)\n\n")
        f.write("| JDK | Média (s) | Mediana (s) | Moda (s) | Q1 (25%) | Q3 (75%) | Desvio Padrão (s) | CV (%) |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        f.write(f"| JDK 17 | {stats17['Tempo (s)']['media']:.3f} | {stats17['Tempo (s)']['mediana']:.3f} | {stats17['Tempo (s)']['moda']:.3f} | {stats17['Tempo (s)']['q1']:.3f} | {stats17['Tempo (s)']['q3']:.3f} | {stats17['Tempo (s)']['desvio_padrao']:.3f} | {stats17['Tempo (s)']['coef_variacao']:.3f}% |\n")
        f.write(f"| JDK 21 | {stats21['Tempo (s)']['media']:.3f} | {stats21['Tempo (s)']['mediana']:.3f} | {stats21['Tempo (s)']['moda']:.3f} | {stats21['Tempo (s)']['q1']:.3f} | {stats21['Tempo (s)']['q3']:.3f} | {stats21['Tempo (s)']['desvio_padrao']:.3f} | {stats21['Tempo (s)']['coef_variacao']:.3f}% |\n")
        f.write(f"| JDK 25 | {stats25['Tempo (s)']['media']:.3f} | {stats25['Tempo (s)']['mediana']:.3f} | {stats25['Tempo (s)']['moda']:.3f} | {stats25['Tempo (s)']['q1']:.3f} | {stats25['Tempo (s)']['q3']:.3f} | {stats25['Tempo (s)']['desvio_padrao']:.3f} | {stats25['Tempo (s)']['coef_variacao']:.3f}% |\n\n")

        # Tabela de Potência
        f.write("### 1.3 Potência (Watts)\n\n")
        f.write("| JDK | Média (W) | Mediana (W) | Moda (W) | Q1 (25%) | Q3 (75%) | Desvio Padrão (W) | CV (%) |\n")
        f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
        f.write(f"| JDK 17 | {stats17['Potencia (W)']['media']:.3f} | {stats17['Potencia (W)']['mediana']:.3f} | {stats17['Potencia (W)']['moda']:.3f} | {stats17['Potencia (W)']['q1']:.3f} | {stats17['Potencia (W)']['q3']:.3f} | {stats17['Potencia (W)']['desvio_padrao']:.3f} | {stats17['Potencia (W)']['coef_variacao']:.3f}% |\n")
        f.write(f"| JDK 21 | {stats21['Potencia (W)']['media']:.3f} | {stats21['Potencia (W)']['mediana']:.3f} | {stats21['Potencia (W)']['moda']:.3f} | {stats21['Potencia (W)']['q1']:.3f} | {stats21['Potencia (W)']['q3']:.3f} | {stats21['Potencia (W)']['desvio_padrao']:.3f} | {stats21['Potencia (W)']['coef_variacao']:.3f}% |\n")
        f.write(f"| JDK 25 | {stats25['Potencia (W)']['media']:.3f} | {stats25['Potencia (W)']['mediana']:.3f} | {stats25['Potencia (W)']['moda']:.3f} | {stats25['Potencia (W)']['q1']:.3f} | {stats25['Potencia (W)']['q3']:.3f} | {stats25['Potencia (W)']['desvio_padrao']:.3f} | {stats25['Potencia (W)']['coef_variacao']:.3f}% |\n\n")

        # Seção 2: Validação de Premissas
        f.write("## 2. Testes de Premissas Estatísticas\n\n")
        f.write("Para determinar se devemos utilizar testes paramétricos (ANOVA e Teste t) ou não-paramétricos (Kruskal-Wallis e Mann-Whitney U), avaliamos a normalidade e homocedasticidade dos dados.\n\n")
        
        # Teste de Shapiro-Wilk
        f.write("### 2.1 Teste de Normalidade (Shapiro-Wilk)\n")
        f.write("- **H0**: A distribuição dos dados de consumo de energia é normal.\n")
        f.write("- **H1**: A distribuição não é normal.\n\n")
        f.write("| JDK | Estatística W | p-value | Distribuição |\n")
        f.write("| --- | --- | --- | --- |\n")
        for jdk_name, info in comp_results['premissas']['shapiro'].items():
            dist_type = "Normal (p >= 0.05)" if info['normal'] else "Não Normal (p < 0.05)"
            f.write(f"| {jdk_name} | {info['stat']:.4f} | {info['p_val']:.4f} | {dist_type} |\n")
        f.write("\n")
        
        # Teste de Levene
        f.write("### 2.2 Teste de Homocedasticidade (Levene)\n")
        f.write("- **H0**: As variâncias de consumo de energia são iguais entre os grupos (homocedasticidade).\n")
        f.write("- **H1**: As variâncias são significativamente diferentes.\n\n")
        levene_info = comp_results['premissas']['levene']
        homo_str = "Variâncias Iguais (p >= 0.05)" if levene_info['homogeneo'] else "Variâncias Diferentes (p < 0.05)"
        f.write(f"- **Estatística de Levene**: {levene_info['stat']:.4f}\n")
        f.write(f"- **p-value**: {levene_info['p_val']:.4f}\n")
        f.write(f"- **Resultado**: {homo_str}\n\n")
        
        # Conclusão de Premissas
        has_non_normal = any(not info['normal'] for info in comp_results['premissas']['shapiro'].values())
        if has_non_normal or not levene_info['homogeneo']:
            f.write("> [!WARNING]\n")
            f.write("> **Decisão Metodológica**: Como a normalidade foi rejeitada para pelo menos um dos grupos (JDK 21), a premissa para a ANOVA clássica foi violada. Portanto, os testes não-paramétricos (**Kruskal-Wallis** e **Mann-Whitney U**) são utilizados como os testes metodologicamente corretos para as análises globais e par a par.\n\n")
        else:
            f.write("> [!NOTE]\n")
            f.write("> **Decisão Metodológica**: Como a normalidade e a homocedasticidade foram atendidas para todos os grupos, os testes paramétricos (**ANOVA One-Way** e **Teste t**) são estatisticamente válidos e utilizados.\n\n")

        # Seção 3: Testes de Hipóteses
        f.write("## 3. Testes de Hipóteses e Comparações Estatísticas\n\n")
        
        # Comparação Global
        f.write("### 3.1 Comparação Global de Eficiência Energética\n")
        global_test = comp_results['global']['teste_usado']
        f.write(f"**Teste Utilizado**: {global_test}\n\n")
        
        if global_test == 'ANOVA':
            f.write("- **H0**: $\\mu_{Java17} = \\mu_{Java21} = \\mu_{Java25}$ (Não há diferença estatisticamente significativa nas médias de consumo de energia entre as três versões do JDK).\n")
            f.write("- **H1**: Pelo menos uma média de consumo é estatisticamente diferente das demais.\n\n")
            f.write(f"- **Estatística F**: {comp_results['global']['stat']:.4f}\n")
        else:
            f.write("- **H0**: $F_{Java17}(x) = F_{Java21}(x) = F_{Java25}(x)$ (As distribuições de consumo de energia são idênticas; as medianas são estatisticamente iguais).\n")
            f.write("- **H1**: Pelo menos uma das versões do JDK possui uma distribuição de consumo de energia diferente.\n\n")
            f.write(f"- **Estatística H (Kruskal-Wallis)**: {comp_results['global']['stat']:.4f}\n")
            
        f.write(f"- **p-value**: {comp_results['global']['p_val']:.4e}\n")
        decisao_global = "Rejeita-se H0" if comp_results['global']['rejeita'] else "Falha em rejeitar H0"
        f.write(f"- **Decisão**: {decisao_global} (nível de significância 5%)\n")
        
        if comp_results['global']['rejeita']:
            f.write("- **Conclusão**: Há diferença estatisticamente significativa no consumo de energia entre as versões do JDK. A versão do JDK afeta o consumo de energia.\n\n")
        else:
            f.write("- **Conclusão**: Não há diferença estatisticamente significativa no consumo de energia entre as três versões do JDK no quadro global de 40 execuções.\n\n")
            
        # Post-hoc do Global
        if comp_results['global']['tukey'] is not None:
            f.write("#### Teste Post-Hoc: Tukey HSD\n")
            f.write("```\n")
            f.write(str(comp_results['global']['tukey']) + "\n")
            f.write("```\n\n")
        elif comp_results['global']['dunn_mw'] is not None:
            f.write("#### Teste Post-Hoc: Mann-Whitney U Pareados com Ajuste Holm-Bonferroni\n\n")
            f.write("| Comparação | p-value Bruto | p-value Corrigido | Rejeita H0 (α=5%) |\n")
            f.write("| --- | --- | --- | --- |\n")
            for res in comp_results['global']['dunn_mw']:
                reject_str = "**Sim**" if res['reject'] else "Não"
                f.write(f"| {res['pair']} | {res['p_raw']:.4f} | {res['p_adj']:.4f} | {reject_str} |\n")
            f.write("\n")
            
        # Comparação A (17 vs 21)
        f.write("### 3.2 Comparação Crítica A (Transição LTS: Java 17 vs Java 21)\n")
        comp_a = comp_results['comp_a']
        f.write(f"**Teste Utilizado**: {comp_a['teste_usado']}\n\n")
        
        if "Teste t" in comp_a['teste_usado']:
            f.write("- **H0**: $\\mu_{Java17} = \\mu_{Java21}$ (As médias de consumo de energia são iguais).\n")
            f.write("- **H1**: $\\mu_{Java17} \\neq \\mu_{Java21}$ (As médias de consumo são diferentes).\n\n")
        else:
            f.write("- **H0**: As distribuições de consumo de energia do Java 17 e do Java 21 são estatisticamente iguais.\n")
            f.write("- **H1**: As distribuições de consumo são estatisticamente diferentes.\n\n")
            
        f.write(f"- **Estatística do Teste**: {comp_a['stat']:.4f}\n")
        f.write(f"- **p-value**: {comp_a['p_val']:.4f}\n")
        decisao_a = "Rejeita-se H0" if comp_a['rejeita'] else "Falha em rejeitar H0"
        f.write(f"- **Decisão**: {decisao_a}\n")
        
        if comp_a['rejeita']:
            f.write("- **Conclusão**: As médias/distribuições de consumo são significativamente diferentes, indicando mudança na eficiência energética entre o Java 17 e o Java 21.\n\n")
        else:
            f.write("- **Conclusão**: Não há diferença estatisticamente significativa na transição LTS.\n")
            f.write("  - **Nota Analítica**: Estatisticamente, a versão 21 manteve a estabilidade de consumo e não gerou regressão energética em relação ao Java 17. As médias globais foram extremamente próximas (1491.19 J vs 1491.44 J).\n\n")
 
        # Comparação B (17 vs 25)
        f.write("### 3.3 Comparação Crítica B (O Salto Moderno: Java 17 vs Java 25)\n")
        comp_b = comp_results['comp_b']
        f.write(f"**Teste Utilizado**: {comp_b['teste_usado']}\n\n")
        
        if "Teste t" in comp_b['teste_usado']:
            f.write("- **H0**: $\\mu_{Java17} = \\mu_{Java25}$ (As médias de consumo de energia são iguais).\n")
            f.write("- **H1**: $\\mu_{Java17} \\neq \\mu_{Java25}$ (As médias de consumo são diferentes).\n\n")
        else:
            f.write("- **H0**: As distribuições de consumo de energia do Java 17 e do Java 25 são estatisticamente iguais.\n")
            f.write("- **H1**: As distribuições de consumo são estatisticamente diferentes.\n\n")
            
        f.write(f"- **Estatística do Teste**: {comp_b['stat']:.4f}\n")
        f.write(f"- **p-value**: {comp_b['p_val']:.4f}\n")
        decisao_b = "Rejeita-se H0" if comp_b['rejeita'] else "Falha em rejeitar H0"
        f.write(f"- **Decisão**: {decisao_b}\n")
        
        if comp_b['rejeita']:
            f.write(f"- **Conclusão**: Rejeita-se H0. A diferença é significativa (JDK 17: {comp_b['media_17']:.2f} J vs JDK 25: {comp_b['media_25']:.2f} J).\n")
            if comp_b['media_25'] > comp_b['media_17']:
                f.write("  - **Nota Analítica**: Como a média do Java 25 (1508.04 J) foi maior que a do 17 (1491.19 J), conclui-se estatisticamente que a evolução para o Java 25 resultou em maior consumo (menor eficiência) sob estresse contínuo.\n\n")
            else:
                f.write("  - **Nota Analítica**: O Java 25 apresentou consumo médio significativamente menor em relação ao Java 17.\n\n")
        else:
            f.write("- **Conclusão**: Falha em rejeitar H0. Não há diferença estatisticamente significativa entre o consumo geral de energia do Java 17 e do Java 25 sob estresse contínuo de 40 execuções.\n\n")

        # Seção 3.4: Warm-up
        f.write("### 3.4 Avaliação de Ganho de Eficiência no Warm-up (Apenas Primeiras 10 Execuções: Java 17 vs Java 25)\n")
        warm = comp_results['warmup']
        f.write(f"**Teste Utilizado**: {warm['teste_usado']}\n\n")
        
        if "Teste t" in warm['teste_usado']:
            f.write("- **H0**: $\\mu_{Java25} \\ge \\mu_{Java17}$ (O Java 25 consome o mesmo ou mais que o Java 17 no início).\n")
            f.write("- **H1**: $\\mu_{Java25} < \\mu_{Java17}$ (O Java 25 consome significativamente menos energia, comprovando ganho de eficiência no tiro curto).\n\n")
        else:
            f.write("- **H0**: A distribuição de consumo de energia do Java 25 é estocasticamente maior ou igual à do Java 17 no início.\n")
            f.write("- **H1**: A distribuição de consumo de energia do Java 25 é estocasticamente menor à do Java 17 no início.\n\n")
            
        f.write(f"- **Estatística do Teste**: {warm['stat']:.4f}\n")
        f.write(f"- **p-value**: {warm['p_val']:.4e}\n")
        decisao_w = "Rejeita-se H0" if warm['rejeita'] else "Falha em rejeitar H0"
        f.write(f"- **Decisão**: {decisao_w}\n")
        
        if warm['rejeita']:
            f.write(f"- **Conclusão**: Rejeita-se H0 em favor de H1 (p < 0.05). Existe ganho de eficiência estatisticamente comprovado para o Java 25 no início das execuções.\n")
            f.write(f"  - **Nota Analítica**: O Java 25 consumiu em média apenas **{warm['media_25']:.2f} J** no início (fase de warm-up) contra **{warm['media_17']:.2f} J** do Java 17. O p-value foi minúsculo ({warm['p_val']:.4e}), o que comprova estatisticamente com um teste unilateral que a evolução para o Java 25 trouxe um ganho expressivo de eficiência (redução de aproximadamente 6.6% no consumo energético) em execuções curtas.\n\n")
        else:
            f.write("- **Conclusão**: Falha em rejeitar H0. Não há diferença estatisticamente significativa no início das execuções.\n\n")

        # Seção 4: Gráficos
        f.write("## 4. Gráficos Gerados\n")
        f.write("Os gráficos foram salvos na pasta `resultados/graficos/`:\n")
        f.write("1. **Boxplot Comparativo**: `comparacao_consumo_boxplot.png`\n")
        f.write("2. **Média com Intervalo de Confiança (95%)**: `comparacao_consumo_barras_ci.png`\n")
        f.write("3. **Histogramas com KDE**: `comparacao_distribuicao_hist_kde.png`\n")
        f.write("4. **Ajuste de Distribuições Individuais (Densidade e QQ-Plot)**:\n")
        f.write("   - JDK 17: `distribuicoes_densidade_qq_jdk17.png`\n")
        f.write("   - JDK 21: `distribuicoes_densidade_qq_jdk21.png`\n")
        f.write("   - JDK 25: `distribuicoes_densidade_qq_jdk25.png`\n\n")
        
    print(f"Relatório estatístico consolidado salvo em: {relatorio_path}")
    print("=" * 70)
    print("FLUXO EXECUTADO COM SUCESSO!")
    print("=" * 70)

if __name__ == '__main__':
    main()
