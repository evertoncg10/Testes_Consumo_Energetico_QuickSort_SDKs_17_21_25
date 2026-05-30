import os
import estatistica_utils as utils

def executar_analise():
    print("=" * 60)
    print("ANÁLISE ESTATÍSTICA INDIVIDUAL: JDK 17")
    print("=" * 60)
    
    # Caminhos de arquivos
    dados_dir = r"c:\Users\evert\Documents\0-Testes_Software_Verde\Testes_Versões_JDK_17_21_25\Testes_Consumo_Energetico_QuickSort_SDKs_17_21_25\Analise_Estatistica\dados"
    arquivo_xlsx = os.path.join(dados_dir, "Planilha_Dados_das_Execuções_JDK_17-0-18.xlsx")
    output_grafico = r"c:\Users\evert\Documents\0-Testes_Software_Verde\Testes_Versões_JDK_17_21_25\Testes_Consumo_Energetico_QuickSort_SDKs_17_21_25\Analise_Estatistica\resultados\graficos\distribuicoes_densidade_qq_jdk17.png"
    
    # 1. Carregar dados
    df = utils.carregar_dados(arquivo_xlsx, n_linhas=40)
    print(f"Dados carregados com sucesso: {len(df)} execuções válidas.")
    
    # 2. Calcular estatísticas descritivas
    stats_desc = utils.calcular_estatisticas_descritivas(df)
    
    # Imprimir tabela de estatísticas descritivas
    print("\n--- Estatísticas Descritivas ---")
    print(f"{'Métrica':<15} | {'Média':<10} | {'Mediana':<10} | {'Moda':<10} | {'Q1 (25%)':<10} | {'Q3 (75%)':<10} | {'Desvio Padrão':<14} | {'CV (%)':<8}")
    print("-" * 105)
    for metrica, vals in stats_desc.items():
        print(f"{metrica:<15} | {vals['media']:<10.3f} | {vals['mediana']:<10.3f} | {vals['moda']:<10.3f} | {vals['q1']:<10.3f} | {vals['q3']:<10.3f} | {vals['desvio_padrao']:<14.3f} | {vals['coef_variacao']:<8.3f}%")
    
    # 3. Intervalo de confiança e tamanho amostral (métrica: Energia (J))
    energia_serie = df['Energia (J)']
    analise_amostra = utils.calcular_tamanho_amostra_e_intervalo_confianca(energia_serie, conf_level=0.95)
    
    print("\n--- Intervalo de Confiança e Amostragem (Energia J) ---")
    print(f"Intervalo de Confiança (95%): [{analise_amostra['ic_inferior']:.3f} J, {analise_amostra['ic_superior']:.3f} J]")
    print(f"Margem de Erro Atual (n=40): {analise_amostra['margem_erro_atual']:.3f} J ({analise_amostra['margem_erro_atual_pct']:.3f}%)")
    
    print("\nTamanho Amostral Necessário vs Margem de Erro Teórica:")
    print(f"{'Nível de Confiança':<20} | {'Margem de Erro 1%':<20} | {'Margem de Erro 2%':<20} | {'Margem de Erro 5%':<20}")
    print("-" * 90)
    for conf, erros in analise_amostra['tamanho_amostral_requerido'].items():
        conf_pct = f"{conf*100:.0f}%"
        print(f"{conf_pct:<20} | {erros[1]:<20} | {erros[2]:<20} | {erros[5]:<20}")
        
    # 4. Ajustar distribuições e gerar gráfico lado a lado
    print("\n--- Ajustando Distribuições de Probabilidade (Energia J) ---")
    dist_fits = utils.ajustar_e_plotar_distribucoes(df, 'Energia (J)', 'JDK 17', output_grafico)
    for dist, info in dist_fits.items():
        print(f"Fórmula Ajustada {dist:<12}: f(x) = {info['formula']}")
        
    print(f"\nGráficos de Densidade e QQ-Plot salvos em: {output_grafico}")
    print("=" * 60 + "\n")
    return df, stats_desc

if __name__ == '__main__':
    executar_analise()
