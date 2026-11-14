#!/usr/bin/env python3
"""Pares controle/tratamento transcritos das tabelas originais (conferidos visualmente
nas imagens das páginas) e perdas calculadas. Nada foi digitalizado de gráficos.
Saída: dados_tratamentos_observados_verificado.csv"""
import pandas as pd
B = dict(study_id="Bertulio_2008", fonte="Bertulio et al. (2008), Revista de Agricultura, p.122; PDF escaneado, conferido na imagem",
         especie_ou_clone=None, local="Campo Verde, MT (coordenadas não informadas)", idade_inicial_meses=14,
         espacamento="3 x 3 m", desfolha="100% artificial manual, a partir do 1º galho vivo", eventos="2 (abril/2007 e janeiro/2008)",
         n_arvores="tratamento: blocos de 10 árvores/clone (nº de blocos não informado no trecho lido); testemunha: 40 árvores/clone",
         mortalidade_obs="0 em todos os grupos (Tabelas 1 e 2)")
linhas = []
T = {  # (clone, tabela, idade, variável, unidade): (desfolha, testemunha)
 ("urocam", "Tabela 1", 14, "CAP", "cm"): (22.50, 23.97), ("urocam", "Tabela 1", 14, "altura", "m"): (8.74, 8.86),
 ("urocam", "Tabela 1", 14, "volume", "m3/árvore"): (0.0282, 0.0337),
 ("urograndis", "Tabela 1", 14, "CAP", "cm"): (27.15, 26.98), ("urograndis", "Tabela 1", 14, "altura", "m"): (11.10, 10.71),
 ("urograndis", "Tabela 1", 14, "volume", "m3/árvore"): (0.0523, 0.0515),
 ("urocam", "Tabela 2", 26, "CAP", "cm"): (26.35, 36.4275), ("urocam", "Tabela 2", 26, "altura", "m"): (9.45, 14.35),
 ("urocam", "Tabela 2", 26, "volume", "m3/árvore"): (0.0419, 0.1221),
 ("urograndis", "Tabela 2", 26, "CAP", "cm"): (29.4625, 38.6225), ("urograndis", "Tabela 2", 26, "altura", "m"): (15.0, 17.885),
 ("urograndis", "Tabela 2", 26, "volume", "m3/árvore"): (0.083, 0.1734)}
nomes = {"urocam": "E. urophylla × E. camaldulensis (urocam)", "urograndis": "E. urophylla × E. grandis (urograndis)"}
for (cl, tab, idade, var, un), (trat, ctrl) in T.items():
    linhas.append(dict(B, especie_ou_clone=nomes[cl], tabela=tab, idade_meses=idade, tratamento="desfolha 100%, 2 eventos",
                       variavel=var, unidade=un, valor_controle=ctrl, valor_tratamento=trat))
M = dict(study_id="Matrangolo_2010", fonte="Matrangolo et al. (2010), Pesq. agropec. bras. 45(9):952-957, Tabela 2, p.956",
         especie_ou_clone="E. grandis (seminal)", local="Viçosa, MG, 20°46'16\"S 42°52'41\"W, 650 m", idade_inicial_meses=0,
         espacamento="3,0 x 2,0 m", desfolha="100% artificial (total)", n_arvores="60 árvores por tratamento",
         tabela="Tabela 2", idade_meses=92)
ctrl = dict(mort=8.0, N=1533, dap=18.4, vt_arv=0.30595, vt_ha=469.1)
trats = {2: ("1 evento (56 DAP)", 6.9, 1552, 15.1, 0.18778, 291.4), 3: ("2 eventos (56 e 143 DAP)", 8.3, 1528, 12.3, 0.11700, 178.8),
         4: ("2 eventos (56 e 267 DAP)", 8.7, 1521, 12.6, 0.11831, 180.0), 5: ("3 eventos (56, 143 e 278 DAP)", 8.8, 1520, 9.7, 0.06273, 95.4)}
for k, (desc, mort, N, dap, va, vh) in trats.items():
    for var, un, c, t in (("DAP médio", "cm", ctrl["dap"], dap), ("volume por árvore (ff=0,40)", "m3/árvore", ctrl["vt_arv"], va),
                          ("volume por hectare (ff=0,40)", "m3/ha", ctrl["vt_ha"], vh)):
        linhas.append(dict(M, tratamento=f"T{k}: {desc}", eventos=desc, variavel=var, unidade=un, valor_controle=c,
                           valor_tratamento=t, mortalidade_obs=f"controle {ctrl['mort']}%; tratamento {mort}% (mesmos níveis, segundo o texto)"))
d = pd.DataFrame(linhas)
d["L_obs_pct_calculado"] = (100 * (1 - d.valor_tratamento / d.valor_controle)).round(3)
# Bertulio: ajuste pela linha de base (Tabela 1 = idade inicial 14 meses = início do experimento)
base = d[(d.study_id == "Bertulio_2008") & (d.idade_meses == 14)].set_index(["especie_ou_clone", "variavel"])
def ajust(r):
    if r.study_id != "Bertulio_2008" or r.idade_meses != 26: return None
    b = base.loc[(r.especie_ou_clone, r.variavel)]
    return round(100 * (1 - (r.valor_tratamento / r.valor_controle) / (b.valor_tratamento / b.valor_controle)), 3)
d["L_obs_pct_ajustado_linha_base"] = d.apply(ajust, axis=1)
d["tipo_valor"] = "controle/tratamento transcritos da tabela; perdas calculadas"
d["aplicabilidade"] = d.study_id.map({"Bertulio_2008": "híbridos de E. urophylla: calibração e teste interno (mesmo experimento), não independente",
                                      "Matrangolo_2010": "E. grandis: plausibilidade biológica (transferência taxonômica)"})
d.to_csv("dados_tratamentos_observados_verificado.csv", index=False)
pd.set_option("display.width", 220)
print(d[["study_id", "especie_ou_clone", "idade_meses", "tratamento", "variavel", "valor_controle", "valor_tratamento",
         "L_obs_pct_calculado", "L_obs_pct_ajustado_linha_base"]].to_string())
