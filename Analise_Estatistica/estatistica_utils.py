import os
import pandas as pd  # type: ignore
import numpy as np
import scipy.stats as stats  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore

# Configuração estética global dos gráficos
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Liberation Sans']
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['grid.color'] = '#F0F0F0'
plt.rcParams['grid.linestyle'] = '-'
plt.rcParams['grid.linewidth'] = 0.5

# Paleta de cores premium para os JDKs
PALETA_JDK = {
    'JDK 17': '#F07167', # Vermelho/coral pastel
    'JDK 21': '#00AFB9', # Ciano/Azul piscina pastel
    'JDK 25': '#FED9B7'  # Amarelo/Laranja pálido pastel
}

def carregar_dados(caminho_arquivo, n_linhas=40):
    """
    Carrega os dados de uma planilha Excel dos testes do JDK e padroniza as colunas.
    Pega apenas as primeiras n_linhas que correspondem às execuções de teste.
    """
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_arquivo}")
        
    df = pd.read_excel(caminho_arquivo)
    
    # Renomear as colunas por índice para evitar problemas de codificação
    novas_colunas = ['Execucao', 'Tempo (s)', 'Energia (J)', 'Potencia (W)']
    df.columns = novas_colunas[:df.shape[1]]
    
    # Selecionar apenas as primeiras n_linhas e remover linhas nulas
    df = df.iloc[:n_linhas].copy()
    
    # Converter tipos numéricos
    for col in ['Tempo (s)', 'Energia (J)', 'Potencia (W)']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    # Garantir que a coluna de Execução seja inteira
    df['Execucao'] = df['Execucao'].astype(int)
    
    return df

def calcular_estatisticas_descritivas(df):
    """
    Calcula as estatísticas descritivas solicitadas para cada métrica:
    média, mediana, moda, quartis, desvio padrão e coeficiente de variação.
    """
    stats_dict = {}
    metricas = ['Energia (J)', 'Tempo (s)', 'Potencia (W)']
    
    for metrica in metricas:
        if metrica not in df.columns:
            continue
            
        dados = df[metrica].dropna()
        
        # Estatísticas básicas
        media = dados.mean()
        mediana = dados.median()
        
        # Moda (pode ter múltiplos valores, pegamos a primeira ou retornamos string formatada)
        moda_series = dados.mode()
        if not moda_series.empty:
            moda = moda_series.iloc[0]
        else:
            moda = np.nan
            
        # Quartis
        q1 = dados.quantile(0.25)
        q3 = dados.quantile(0.75)
        
        # Variabilidade
        desvio_padrao = dados.std(ddof=1)
        coef_variacao = (desvio_padrao / media) * 100 if media != 0 else 0
        
        stats_dict[metrica] = {
            'media': media,
            'mediana': mediana,
            'moda': moda,
            'q1': q1,
            'q3': q3,
            'desvio_padrao': desvio_padrao,
            'coef_variacao': coef_variacao,
            'n': len(dados)
        }
        
    return stats_dict

def calcular_tamanho_amostra_e_intervalo_confianca(dados, conf_level=0.95):
    """
    Calcula o intervalo de confiança para a média populacional e a margem de erro atual.
    Também calcula o tamanho de amostra exigido para margens de erro de 1%, 2% e 5% da média.
    """
    dados = dados.dropna().values
    n = len(dados)
    media = np.mean(dados)
    std_amostral = np.std(dados, ddof=1)
    
    # Erro padrão da média
    sem = std_amostral / np.sqrt(n)
    
    # Intervalo de confiança (t-student)
    ic_inf, ic_sup = stats.t.interval(conf_level, df=n-1, loc=media, scale=sem)
    margem_erro_atual = ic_sup - media
    
    # Cálculos de tamanho amostral teórico
    tamanho_amostral = {}
    for conf in [0.95, 0.99]:
        # Valor crítico Z
        z_crit = stats.norm.ppf(1 - (1 - conf) / 2)
        
        tamanho_amostral[conf] = {}
        for perc_erro in [1, 2, 5]:
            E = media * (perc_erro / 100.0) # Margem de erro absoluta desejada
            # Fórmula do tamanho amostral: n = (Z * s / E)^2
            n_req = ((z_crit * std_amostral) / E) ** 2
            tamanho_amostral[conf][perc_erro] = int(np.ceil(n_req))
            
    return {
        'ic_inferior': ic_inf,
        'ic_superior': ic_sup,
        'margem_erro_atual': margem_erro_atual,
        'margem_erro_atual_pct': (margem_erro_atual / media) * 100,
        'tamanho_amostral_requerido': tamanho_amostral
    }

def ajustar_e_plotar_distribucoes(df, metrica, jdk_name, output_path):
    """
    Ajusta distribuições teóricas (Normal, Log-normal, Gama, Weibull) nos dados da métrica
    e gera um gráfico lado a lado (Densidade de Distribuições e QQ-Plots).
    Retorna os parâmetros do ajuste.
    """
    dados = df[metrica].dropna().values
    n = len(dados)
    
    # 1. Ajuste dos parâmetros (estimadores de máxima verossimilhança)
    # Para Log-normal, fixamos floc=0 para obter a forma padrão 2-parâmetros LN(mu, sigma^2)
    params_norm = stats.norm.fit(dados)
    params_lognorm = stats.lognorm.fit(dados, floc=0)
    params_gamma = stats.gamma.fit(dados)
    params_weibull = stats.weibull_min.fit(dados)
    
    # Formatação das fórmulas matemáticas em texto para exibição
    # Normal: N(mu, sigma^2)
    mu_n, std_n = params_norm
    formula_normal = f"N({mu_n:.3f}, {std_n:.3f}^2)"
    
    # Lognormal: s (sigma) e scale (e^mu)
    s_ln, loc_ln, scale_ln = params_lognorm
    mu_ln = np.log(scale_ln)
    formula_lognorm = f"LN(mu={mu_ln:.3f}, sigma={s_ln:.3f})"
    
    # Gama: a (shape), loc, scale
    a_g, loc_g, scale_g = params_gamma
    formula_gamma = f"Gamma(shape={a_g:.3f}, scale={scale_g:.3f})"
    
    # Weibull: c (shape), loc, scale
    c_w, loc_w, scale_w = params_weibull
    formula_weibull = f"Weibull(shape={c_w:.3f}, scale={scale_w:.3f})"
    
    # 2. Criar a figura lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # --- PLOT DA ESQUERDA: Densidade de Distribuições ---
    ax_dens = axes[0]
    # Histograma empírico
    # Estilo refinado: barras cinzas suaves com bordas
    sns.histplot(dados, stat='density', bins=10, ax=ax_dens, color='#D3D3D3', edgecolor='#999999', alpha=0.6, label='Dados Exp.')
    
    # Eixo X para plotar as curvas contínuas
    x_min, x_max = np.min(dados) * 0.98, np.max(dados) * 1.02
    x = np.linspace(x_min, x_max, 500)
    
    # Plotar PDFs
    ax_dens.plot(x, stats.norm.pdf(x, *params_norm), color='black', linestyle='-', linewidth=1.5, label=f'Normal: {formula_normal}')
    ax_dens.plot(x, stats.lognorm.pdf(x, *params_lognorm), color='#E63946', linestyle='--', linewidth=1.5, label=f'Log-normal: {formula_lognorm}')
    ax_dens.plot(x, stats.gamma.pdf(x, *params_gamma), color='#4CAF50', linestyle='-.', linewidth=1.5, label=f'Gamma: {formula_gamma}')
    ax_dens.plot(x, stats.weibull_min.pdf(x, *params_weibull), color='#1D3557', linestyle=':', linewidth=1.5, label=f'Weibull: {formula_weibull}')
    
    ax_dens.set_title(f"Densidade de Distribuições - {jdk_name}", fontsize=12, fontweight='bold', pad=15)
    ax_dens.set_xlabel(f"{metrica}", fontsize=10)
    ax_dens.set_ylabel("Densidade", fontsize=10)
    ax_dens.grid(True, alpha=0.3)
    ax_dens.legend(fontsize=8, loc='upper right')
    
    # --- PLOT DA DIREITA: QQ-Plots ---
    ax_qq = axes[1]
    
    # Posições de plotagem p_i = (i - 0.5) / n para quantis empíricos ordenados
    p_i = (np.arange(1, n + 1) - 0.5) / n
    dados_ord = np.sort(dados)
    
    # Quantis teóricos para cada distribuição
    q_norm = stats.norm.ppf(p_i, *params_norm)
    q_lognorm = stats.lognorm.ppf(p_i, *params_lognorm)
    q_gamma = stats.gamma.ppf(p_i, *params_gamma)
    q_weibull = stats.weibull_min.ppf(p_i, *params_weibull)
    
    # Dispersão
    ax_qq.scatter(q_norm, dados_ord, facecolors='none', edgecolors='black', marker='o', s=30, alpha=0.8, label='Normal')
    ax_qq.scatter(q_lognorm, dados_ord, facecolors='none', edgecolors='#E63946', marker='o', s=30, alpha=0.8, label='Log-normal')
    ax_qq.scatter(q_gamma, dados_ord, facecolors='none', edgecolors='#4CAF50', marker='o', s=30, alpha=0.8, label='Gamma')
    ax_qq.scatter(q_weibull, dados_ord, facecolors='none', edgecolors='#1D3557', marker='o', s=30, alpha=0.8, label='Weibull')
    
    # Linha diagonal de referência (y = x)
    ref_min = min(np.min(dados), np.min(q_norm), np.min(q_lognorm), np.min(q_gamma), np.min(q_weibull))
    ref_max = max(np.max(dados), np.max(q_norm), np.max(q_lognorm), np.max(q_gamma), np.max(q_weibull))
    ax_qq.plot([ref_min, ref_max], [ref_min, ref_max], color='#555555', linestyle='-', linewidth=1, alpha=0.7)
    
    ax_qq.set_title(f"QQ-Plots de Distribuições - {jdk_name}", fontsize=12, fontweight='bold', pad=15)
    ax_qq.set_xlabel("Quantis Teóricos", fontsize=10)
    ax_qq.set_ylabel("Quantis Empíricos", fontsize=10)
    ax_qq.grid(True, alpha=0.3)
    ax_qq.legend(fontsize=9, loc='lower right')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    return {
        'Normal': {'params': params_norm, 'formula': formula_normal},
        'Log-normal': {'params': params_lognorm, 'formula': formula_lognorm},
        'Gamma': {'params': params_gamma, 'formula': formula_gamma},
        'Weibull': {'params': params_weibull, 'formula': formula_weibull}
    }

def salvar_boxplot_comparativo(dados_dict, metrica, output_path):
    """
    Gera um Boxplot comparando a distribuição dos dados da métrica para cada JDK.
    """
    plt.figure(figsize=(10, 5))
    
    # Montar DataFrame longo para o seaborn
    dados_long = []
    for jdk, serie in dados_dict.items():
        for val in serie.dropna():
            dados_long.append({'Grupo': jdk, metrica: val})
    df_long = pd.DataFrame(dados_long)
    
    # Criar Boxplot com cores personalizadas e estilo clean
    ax = sns.boxplot(
        x='Grupo', 
        y=metrica, 
        data=df_long, 
        hue='Grupo',
        palette=PALETA_JDK, 
        legend=False,
        width=0.5,
        linewidth=1.2,
        fliersize=4,
        flierprops=dict(markerfacecolor='#555555', marker='o', alpha=0.7)
    )
    
    # Ajustar rótulos e títulos
    plt.title(f"Comparação do {metrica}", fontsize=14, fontweight='bold', pad=28, loc='left')
    ax.text(0, 1.04, f"Distribuição para os grupos {', '.join(dados_dict.keys())}", transform=ax.transAxes, fontsize=11, color='#555555', ha='left')
    
    ax.set_xlabel("Grupo", fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel(metrica, fontsize=11, fontweight='bold', labelpad=10)
    
    # Estética limpa
    sns.despine()
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def salvar_grafico_barras_ci(dados_dict, metrica, output_path):
    """
    Gera um gráfico de barras comparando as médias com barras de erro de 95% de confiança.
    """
    plt.figure(figsize=(10, 5))
    
    grupos = list(dados_dict.keys())
    medias = []
    erros = []
    
    for jdk, serie in dados_dict.items():
        dados = serie.dropna().values
        mean = np.mean(dados)
        std_dev = np.std(dados, ddof=1)
        n = len(dados)
        
        # Calcular o intervalo de confiança t-Student de 95%
        sem = std_dev / np.sqrt(n)
        t_val = stats.t.ppf(0.975, df=n-1)
        margin_error = t_val * sem
        
        medias.append(mean)
        erros.append(margin_error)
        
    # Plotagem
    ax = plt.gca()
    cores = [PALETA_JDK[g] for g in grupos]
    
    bars = ax.bar(
        grupos, 
        medias, 
        yerr=erros, 
        color=cores, 
        edgecolor='#777777', 
        linewidth=0.8,
        capsize=8, 
        error_kw=dict(ecolor='black', elinewidth=1.2, capthick=1.2),
        width=0.4
    )
    
    # Adicionar valor numérico no topo das barras
    for bar, media in zip(bars, medias):
        yval = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2.0, 
            yval * 0.5, # Posição vertical intermediária para legibilidade
            f"{media:.2f}", 
            ha='center', 
            va='center', 
            color='black', 
            fontweight='bold',
            fontsize=10
        )
        
    plt.title(f"Média de {metrica} com Intervalo de Confiança (95%)", fontsize=14, fontweight='bold', pad=28, loc='left')
    ax.text(0, 1.04, "Comparação estatística entre execuções do QuickSort", transform=ax.transAxes, fontsize=11, color='#555555', ha='left')
    
    ax.set_xlabel("Linguagem / Versão SDK", fontsize=11, fontweight='bold', labelpad=10)
    ax.set_ylabel(f"Média {metrica}", fontsize=11, fontweight='bold', labelpad=10)
    
    sns.despine()
    ax.yaxis.grid(True, alpha=0.3)
    ax.set_axisbelow(True)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()

def salvar_histogramas_lado_a_lado(dados_dict, metrica, output_path):
    """
    Gera três histogramas de densidade horizontais lado a lado com suas curvas KDE individuais.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 4), sharey=False)
    
    for i, (jdk, serie) in enumerate(dados_dict.items()):
        ax = axes[i]
        dados = serie.dropna().values
        
        # Histograma com KDE
        sns.histplot(dados, kde=True, stat='density', bins=10, ax=ax, color=PALETA_JDK[jdk], edgecolor='#777777', alpha=0.7)
        
        ax.set_title(jdk, fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel(metrica, fontsize=10)
        
        if i == 0:
            ax.set_ylabel("Densidade", fontsize=10)
        else:
            ax.set_ylabel("", fontsize=10)
            
        ax.grid(True, alpha=0.2)
        sns.despine(ax=ax)
        
    plt.suptitle(f"Distribuição de {metrica} por Grupo", fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
