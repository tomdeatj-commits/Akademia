#!/usr/bin/env python3
"""Transforma CSVs efetivamente exportados do Earth Engine em fenotipagem da Akademia.

GEDI L2A RH98, L2B PAI, L4A AGBD e Sentinel-2 NDVI/NDRE são proxies.
Não identifica pragas e não declara validação de 3-PG.
"""
import argparse
import json
import math
from pathlib import Path
import pandas as pd

PRODUTOS = {
    ("GEDI_L2A","rh98"):("https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI02_A_002_MONTHLY","estrutura_dossel"),
    ("GEDI_L2B","pai"):("https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI02_B_002_MONTHLY","area_total_plantas"),
    ("GEDI_L4A","agbd"):("https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI04_A_002_MONTHLY","biomassa_aerea_predita"),
    ("SENTINEL2_SR","ndvi"):("https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED","indice_espectral"),
    ("SENTINEL2_SR","ndre"):("https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED","indice_espectral")
}
COLUNAS=("talhao_id","genotipo","solo","ano_mes","produto","variavel",
         "valor","n_pixels_validos","unidade","origem","comparavel")


def integrar(arquivos,sitio_id):
    df=pd.concat((pd.read_csv(arq) for arq in arquivos),ignore_index=True)
    falta=set(COLUNAS)-set(df)
    if falta: raise ValueError(f"Exportação incompleta: {sorted(falta)}")
    if df.empty: raise ValueError("Não há observações válidas para importar")
    if df[list(COLUNAS)].isna().any().any():
        raise ValueError("Há talhões sem genótipo/solo/valor; complete os metadados antes de importar")
    df["n_pixels_validos"]=pd.to_numeric(df.n_pixels_validos,errors="raise")
    df["valor"]=pd.to_numeric(df.valor,errors="raise")
    if (df.n_pixels_validos<=0).any() or not df.valor.map(math.isfinite).all():
        raise ValueError("Amostras não finitas ou sem pixels válidos")
    if not set(df.genotipo).issubset({"G1","G2"}) or not set(df.solo).issubset({"arenoso","argiloso"}):
        raise ValueError("Atribua G1/G2 e textura aos talhões antes de importar")
    if pd.to_datetime(df.ano_mes+"-01",format="%Y-%m-%d",errors="coerce").isna().any():
        raise ValueError("Data inválida; formato esperado YYYY-MM")
    if any((r.produto,r.variavel) not in PRODUTOS for r in df.itertuples()):
        raise ValueError("Produto/variável Earth Engine não reconhecido")
    if df.duplicated(["talhao_id","ano_mes","produto","variavel"]).any():
        raise ValueError("Observações duplicadas talhão × mês × produto × variável")
    df["fonte"]=df.apply(lambda r:PRODUTOS[(r.produto,r.variavel)][0],axis=1)
    df["natureza"]=df.apply(lambda r:PRODUTOS[(r.produto,r.variavel)][1],axis=1)
    df["sitio_id"]=sitio_id
    df["comparavel"]="nao"
    df["tipo_evidencia"]="proxy_indireto_sem_ajuste"
    df=df.sort_values(["talhao_id","ano_mes","variavel"])
    # Anomalia sazonal relativa a anos anteriores do MESMO talhão/mês.
    # Não cria limiar de praga ou uma medida inexistente de IAF.
    df["desvio_sazonal"]=float("nan")
    df["n_anos_referencia"]=0
    for (talhao,var,mes),idx in df.groupby(
        ["talhao_id","variavel",df.ano_mes.str[-2:]],sort=False).groups.items():
        sub=df.loc[idx].sort_values("ano_mes")
        for i,(j,row) in enumerate(sub.iterrows()):
            anteriores=sub.iloc[:i].valor
            if len(anteriores)>=3:
                df.loc[j,"desvio_sazonal"]=float(row.valor-float(anteriores.median()))
                df.loc[j,"n_anos_referencia"]=len(anteriores)
    resumo=df.groupby(["produto","variavel"],as_index=False).agg(
        n_registros=("valor","size"),n_talhoes=("talhao_id","nunique"),
        n_meses=("ano_mes","nunique"))
    return df,resumo


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("arquivos",type=Path,nargs="+",help="CSVs exportados pelo Earth Engine")
    p.add_argument("--sitio-id",required=True)
    p.add_argument("--saida",type=Path,required=True)
    args=p.parse_args()
    dados,resumo=integrar(args.arquivos,args.sitio_id)
    args.saida.mkdir(parents=True,exist_ok=True)
    dados.to_csv(args.saida/"fenotipagem_gee_importada.csv",index=False)
    resumo.to_csv(args.saida/"disponibilidade_sensoriamento.csv",index=False)
    print(json.dumps(dict(status="proxies_importados_sem_validacao_biologica",
                          registros=len(dados),talhoes=dados.talhao_id.nunique(),
                          resumo=resumo.to_dict("records")),ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
