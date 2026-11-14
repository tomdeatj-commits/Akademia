#!/usr/bin/env python3
"""Gera perturbadores mensais para 3-PG de uma exportação DIÁRIA CLIMBra NORMALIZADA.
Não baixa o dataset nem interpola coordenadas: isso deve ser feito por arquivo de fonte
identificado (coordenada, GCMs, cenários, origem e versão da correção de viés).

CSV de entrada, uma linha/dia/modelo/cenário:
  gcm,cenario,data,tasmin_c,tasmax_c,pr_mm_d,rss_mj_m2_d
  cenario = historico | SSP2-4.5 | SSP5-8.5

A variável rss do CLIMBra (radiação solar líquida) não é necessariamente o mesmo
fluxo incidente srad do 3-PG; aplicar sua razão a srad é uma hipótese explícita.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd


def construir(diario,ref_ini,ref_fim,fut_ini,fut_fim,fonte,identificacao_celula):
    cols={"gcm","cenario","data","tasmin_c","tasmax_c","pr_mm_d","rss_mj_m2_d"}
    if cols-set(diario): raise ValueError(f"CLIMBra normalizado sem: {sorted(cols-set(diario))}")
    d=diario.copy()
    d["data"]=pd.to_datetime(d["data"],errors="raise")
    for col in ["tasmin_c","tasmax_c","pr_mm_d","rss_mj_m2_d"]:
        d[col]=pd.to_numeric(d[col],errors="raise")
    if d[list(cols-{"gcm","cenario","data"})].isna().any().any():
        raise ValueError("CLIMBra contém NA nas variáveis usadas")
    if (d.tasmin_c>d.tasmax_c).any() or (d.pr_mm_d<0).any() or (d.rss_mj_m2_d<0).any():
        raise ValueError("Dados diários inconsistentes")
    if d.duplicated(["gcm","cenario","data"]).any():
        raise ValueError("Dia repetido para um mesmo GCM/cenário")
    d["year"]=d.data.dt.year
    d["month"]=d.data.dt.month
    s=d.groupby(["gcm","cenario","year","month"],as_index=False).agg(
        tmp_min=("tasmin_c","mean"),tmp_max=("tasmax_c","mean"),
        prcp=("pr_mm_d","sum"),srad=("rss_mj_m2_d","mean"),
        frost_days=("tasmin_c",lambda t: float((t<=0).sum())),
        n_dias=("data","size")
    )
    s["dias_esperados"]=pd.to_datetime(dict(year=s.year,month=s.month,day=1)).dt.days_in_month
    if (s.n_dias!=s.dias_esperados).any():
        raise ValueError("CLIMBra contém mês incompleto; escolha recorte diário integral por ano")
    modelos=sorted(s.gcm.unique().tolist())
    detalhes=[]
    for g in modelos:
        b=s[(s.gcm==g)&(s.cenario=="historico")&s.year.between(ref_ini,ref_fim)]
        if (b.groupby("month").size().reindex(range(1,13),fill_value=0)<10).any():
            raise ValueError(f"{g}: base histórica insuficiente (mínimo 10 anos/mês)")
        for ssp in ("SSP2-4.5","SSP5-8.5"):
            futuro=s[(s.gcm==g)&(s.cenario==ssp)&s.year.between(fut_ini,fut_fim)]
            if (futuro.groupby("month").size().reindex(range(1,13),fill_value=0)<10).any():
                raise ValueError(f"{g} {ssp}: futuro insuficiente (mínimo 10 anos/mês)")
            bh=b.groupby("month")[["tmp_min","tmp_max","prcp","srad"]].mean()
            fh=futuro.groupby("month")[["tmp_min","tmp_max","prcp","srad","frost_days"]].mean()
            for month in range(1,13):
                if bh.loc[month,"prcp"]<=0 or bh.loc[month,"srad"]<=0:
                    raise ValueError(f"{g} mês {month}: não é possível obter razão com base zero")
                detalhes.append(dict(gcm=g,ssp=ssp,month=month,
                    delta_tmin_c=fh.loc[month,"tmp_min"]-bh.loc[month,"tmp_min"],
                    delta_tmax_c=fh.loc[month,"tmp_max"]-bh.loc[month,"tmp_max"],
                    fator_precipitacao=fh.loc[month,"prcp"]/bh.loc[month,"prcp"],
                    fator_radiacao=fh.loc[month,"srad"]/bh.loc[month,"srad"],
                    frost_days=fh.loc[month,"frost_days"]))
    tabela=pd.DataFrame(detalhes)
    agg=tabela.groupby(["ssp","month"],as_index=False)[
        ["delta_tmin_c","delta_tmax_c","fator_precipitacao","fator_radiacao","frost_days"]].median()
    agg["fonte"]=fonte
    agg["periodo"]=f"{ref_ini}-{ref_fim} vs {fut_ini}-{fut_fim}"
    meta=dict(n_modelos=len(modelos),modelos=modelos,celula=identificacao_celula,
              fonte=fonte,periodo_referencia=[ref_ini,ref_fim],
              periodo_futuro=[fut_ini,fut_fim],
              metodo="deltas temperatura + razões chuva/radiação por GCM, mediana entre GCMs",
              escala="perturbação aplicada ao mesmo histórico meteorológico para ciclo sintético de sete anos",
              hipoteses=["rss líquido do CLIMBra utilizado como razão para radiação incidente do 3-PG; verificar adequação",
                        "dias de geada futuros são climatologia mensal, não sequência meteorológica diária",
                        "não foram modelados extremos diários ou mudanças intra-mês",
                        "incerteza entre GCMs deve ser avaliada, mediana não é intervalo de confiança"])
    return agg,tabela,meta


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--entrada",type=Path,required=True)
    p.add_argument("--saida",type=Path,required=True)
    p.add_argument("--referencia",nargs=2,type=int,required=True,metavar=("INICIO","FIM"))
    p.add_argument("--futuro",nargs=2,type=int,required=True,metavar=("INICIO","FIM"))
    p.add_argument("--fonte",required=True)
    p.add_argument("--celula",required=True,help="Coordenada, grade e método de seleção")
    args=p.parse_args()
    for ini,fim in (args.referencia,args.futuro):
        if fim-ini+1<10: raise ValueError("Janelas precisam de ao menos 10 anos")
    data=pd.read_csv(args.entrada)
    d,g,meta=construir(data,*args.referencia,*args.futuro,args.fonte,args.celula)
    meta["arquivo_origem_sha256"]=hashlib.sha256(args.entrada.read_bytes()).hexdigest()
    args.saida.mkdir(parents=True,exist_ok=True)
    d.to_csv(args.saida/"deltas_climbra_mensais.csv",index=False)
    g.to_csv(args.saida/"deltas_por_gcm.csv",index=False)
    (args.saida/"metadados_climbra.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(meta,ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
