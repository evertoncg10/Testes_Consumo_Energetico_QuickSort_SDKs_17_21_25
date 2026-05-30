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
    
    # 2. Executar a análise comparativa (ANOVA, Tukey, Testes t e gráficos comparativos)
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

        # Seção 2: Testes de Hipóteses
        f.write("## 2. Testes de Hipóteses e Comparações Estatísticas\n\n")
        
        # ANOVA
        f.write("### 2.1 Análise de Variância (ANOVA One-way)\n")
        f.write(f"- **Estatística F**: {comp_results['anova']['f_val']:.4f}\n")
        f.write(f"- **p-value**: {comp_results['anova']['p_val']:.4e}\n")
        decisao_anova = "Rejeita-se H0" if comp_results['anova']['rejeita'] else "Falha em rejeitar H0"
        f.write(f"- **Decisão**: {decisao_anova} (nível de significância 5%)\n")
        if comp_results['anova']['rejeita']:
            f.write("- **Conclusão**: Existe uma diferença estatisticamente significativa no consumo de energia entre as três versões do JDK. A versão do JDK afeta o consumo de energia.\n\n")
        else:
            f.write("- **Conclusão**: Não há diferença estatisticamente significativa nas médias de consumo de energia entre as três versões do JDK.\n\n")
            
        # Comparação A
        f.write("### 2.2 Comparação Crítica A (Transição LTS: Java 17 vs Java 21) - Teste t\n")
        f.write(f"- **p-value**: {comp_results['comp_a']['p_val']:.4f}\n")
        decisao_a = "Rejeita-se H0" if comp_results['comp_a']['rejeita'] else "Falha em rejeitar H0"
        f.write(f"- **Decisão**: {decisao_a}\n")
        if comp_results['comp_a']['rejeita']:
            f.write("- **Conclusão**: As médias de consumo são significativamente diferentes, indicando mudança na eficiência energética entre o Java 17 e o Java 21.\n\n")
        else:
            f.write("- **Conclusão**: As médias de consumo são estatisticamente equivalentes. Estatisticamente, a versão 21 manteve a estabilidade de consumo e não gerou regressão energética em relação ao Java 17.\n\n")

        # Comparação B
        f.write("### 2.3 Comparação Crítica B (O Salto Moderno: Java 17 vs Java 25) - Teste t\n")
        f.write(f"- **p-value**: {comp_results['comp_b']['p_val']:.4f}\n")
        decisao_b = "Rejeita-se H0" if comp_results['comp_b']['rejeita'] else "Falha em rejeitar H0"
        f.write(f"- **Decisão**: {decisao_b}\n")
        if comp_results['comp_b']['rejeita']:
            media_17 = stats17['Energia (J)']['media']
            media_25 = stats25['Energia (J)']['media']
            f.write(f"- **Conclusão**: Rejeita-se H0. A diferença é significativa (JDK 17: {media_17:.2f} J vs JDK 25: {media_25:.2f} J).\n")
            if media_25 > media_17:
                f.write("  Estatisticamente, a evolução para o Java 25 resultou em maior consumo (menor eficiência) sob estresse contínuo.\n\n")
            else:
                f.write("  Estatisticamente, a evolução para o Java 25 resultou em menor consumo (maior eficiência).\n\n")
        else:
            f.write("- **Conclusão**: Falha em rejeitar H0. Não há diferença estatisticamente significativa entre o consumo do Java 17 e do Java 25.\n\n")

        f.write("## 3. Gráficos Gerados\n")
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
