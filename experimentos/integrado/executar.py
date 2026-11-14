#!/usr/bin/env python3
"""Orquestrador operacional: genótipo × solo × clima, com pragas e fenotipagem.
Exige dados reais em vez de imputar tolerância, textura ou projeções climáticas.

Uso:
  python3 experimentos/integrado/executar.py --config experimento.json --modo planejar
  python3 experimentos/integrado/executar.py --config experimento.json --modo executar --saida resultados/
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import sys
from pathlib import Path
import pandas as pd
from cenarios import CLIMAS, COLUNAS_DELTA, planejar, perturbar, programar_praga, validar_deltas

RAIZ=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RAIZ/"experimentos"))
sys.path.insert(0,str(RAIZ/"modelo"))
from clones import MATERIAIS, params  # noqa:E402
from threepg_pjs import run_3pg_pjs  # noqa:E402

VARS=("volume","biom_stem","biom_foliage","biom_root","lai","dbh","height","stems_n","asw")
UNIDADES_COMPATIVEIS={
    "volume":{"m3/ha","m³/ha"},
    "biom_stem":{"Mg/ha","t/ha"},
    "biom_foliage":{"Mg/ha","t/ha"},
    "biom_root":{"Mg/ha","t/ha"},
    "lai":{"m2/m2","m²/m²"},
    "dbh":{"cm"},"height":{"m"},
    "stems_n":{"arvores/ha","árvores/ha"},
    "asw":{"mm"}
}

COLUNAS_CLIMA=("year","month","tmp_min","tmp_max","prcp","srad","frost_days")


def carregar_config(path):
    c=json.loads(Path(path).read_text(encoding="utf-8"))
    c=planejar(c) and c
    for g in c["genotipos"]:
        if g["codigo_material"] not in MATERIAIS:
            raise ValueError(f'Material {g["codigo_material"]} não parametrizado no 3-PG disponível')
    return c


def _ler_clima(path):
    d=pd.read_csv(path)
    missing=set(COLUNAS_CLIMA)-set(d.columns)
    if missing: raise ValueError(f"Clima histórico sem {sorted(missing)}")
    if d[list(COLUNAS_CLIMA)].isna().any().any():
        raise ValueError("Clima histórico contém NA; verificar fonte")
    if d.duplicated(["year","month"]).any():
        raise ValueError("Clima histórico possui meses duplicados")
    dt=pd.to_datetime(dict(year=d.year,month=d.month,day=1))
    if not dt.is_monotonic_increasing or len(pd.period_range(dt.min(),dt.max(),freq="M"))!=len(d):
        raise ValueError("Clima histórico deve ser mensal, consecutivo e ordenado")
    if (d.tmp_min>d.tmp_max).any() or (d.prcp<0).any() or (d.srad<=0).any():
        raise ValueError("Clima histórico contém valores inconsistentes")
    # Campos derivados são calculados pelo motor para cada clima, não reutilizados.
    return d.drop(columns=[x for x in ("tmp_ave","vpd_day") if x in d])


def _validar_periodo(c, clima):
    plantio=pd.Period(c["plantio"],freq="M")
    fim=plantio + 84
    inicio=pd.Period(year=int(clima.year.iloc[0]),month=int(clima.month.iloc[0]),freq="M")
    ultimo=pd.Period(year=int(clima.year.iloc[-1]),month=int(clima.month.iloc[-1]),freq="M")
    if inicio>plantio or ultimo<fim:
        raise ValueError(f"Histórico insuficiente: requer ao menos {plantio} até {fim}")
    return plantio, fim


def simular(c, plano, clima):
    plantio,fim=_validar_periodo(c,clima["historico"])
    genes={g["id"]:g for g in c["genotipos"]}
    solos={s["id"]:s for s in c["solos"]}
    pragas={p["id"]:p for p in c.get("pragas",[])}
    mensal=[]
    finais=[]
    for row in plano:
        gid, sid, ssp, dano=row["genotipo"],row["solo"],row["clima"],row["dano"]
        g,so=genes[gid],solos[sid]
        m=MATERIAIS[g["codigo_material"]]
        mes_inicio=plantio+int(m["idade_inicial_meses"])
        if mes_inicio>=fim: raise ValueError("Idade de inicialização incompatível com o ciclo de 7 anos")
        local=dict(latitude=float(c["sitio"]["latitude"]),altitude=float(c["sitio"].get("altitude_m",0)),
                   soil_class=int(so["soil_class"]),asw_i=float(so["cad_mm"])*float(c["fracao_agua_inicial"]),
                   asw_min=0.0,asw_max=float(so["cad_mm"]),
                   **{"from":str(mes_inicio),"to":str(fim)})
        especie=dict(planted=str(plantio),fertility=float(c["fertilidade_fr"]),
                     stems_n=float(c["densidade_inicial_ha"]),
                     biom_stem=float(m["WS0"]),biom_root=float(m["WR0"]),biom_foliage=float(m["WF0"]))
        eventos=programar_praga(str(plantio),pragas.get(dano))
        out=run_3pg_pjs(local,especie,clima[ssp],params(g["codigo_material"]),
                        defoliation_events=eventos["desfolha"] or None,
                        efficiency_events=eventos["eficiencia"] or None,
                        mortality_events=eventos["mortalidade"] or None,
                        compensation=({k:c["compensacao"][k] for k in ("U","gam","a","u_meses")}
                                      if c.get("compensacao") is not None else None))
        if not len(out): raise RuntimeError(f'Simulação vazia: {row["id"]}')
        out=out.copy()
        out.insert(0,"cenario_id",row["id"])
        out.insert(1,"genotipo",gid)
        out.insert(2,"solo",sid)
        out.insert(3,"clima",ssp)
        out.insert(4,"dano",dano)
        out["ano_mes"]=pd.to_datetime(out["date"]).dt.strftime("%Y-%m")
        mensal.append(out)
        end=out.iloc[-1]
        if end["ano_mes"]!=str(fim):
            raise RuntimeError(f'Última data fora do ciclo de 7 anos: {row["id"]}')
        f=dict(row)
        for k in VARS: f[k]=float(end[k])
        f["biomassa_total"]=f["biom_stem"]+f["biom_foliage"]+f["biom_root"]
        f["biomassa_aerea_aprox"]=f["biom_stem"]+f["biom_foliage"]
        f["data_final"]=str(end["date"])
        finais.append(f)
    return pd.concat(mensal,ignore_index=True),pd.DataFrame(finais)


def contrastes(finais):
    out=[]
    index=finais.set_index(["genotipo","solo","clima","dano"])
    for r in finais.itertuples(index=False):
        chave=(r.genotipo,r.solo,r.clima,r.dano)
        base=index.loc[(r.genotipo,r.solo,"historico",r.dano)]
        sem_dano=index.loc[(r.genotipo,r.solo,r.clima,"controle")]
        outros=index.loc[("G1",r.solo,r.clima,r.dano)]
        for var in ("volume","biom_stem","biom_foliage","lai","stems_n"):
            now=float(getattr(r,var))
            def variacao(den):
                return 100*(now/float(den)-1) if float(den)!=0 else None
            out.append(dict(cenario_id=r.id,genotipo=r.genotipo,solo=r.solo,clima=r.clima,
                            dano=r.dano,variavel=var,valor_final=now,
                            variacao_vs_historico_pct=variacao(base[var]),
                            variacao_vs_sem_dano_pct=variacao(sem_dano[var]),
                            diferenca_vs_G1=now-float(outros[var]),
                            papel="simulacao_condicional"))
    return pd.DataFrame(out)


def confrontar_fenotipos(mensal,caminho,site_id):
    """Compara somente campo mensurado e declaração explícita de compatibilidade.
    GEDI e índices espectrais: proxy sem diferença automática com 3-PG."""
    if not caminho: return pd.DataFrame()
    d=pd.read_csv(caminho)
    obrig=("genotipo","solo","ano_mes","variavel","valor","unidade","fonte","origem","comparavel","sitio_id")
    falta=set(obrig)-set(d)
    if falta: raise ValueError(f"Fenotipagem sem colunas: {sorted(falta)}")
    if d[list(obrig)].isna().any().any(): raise ValueError("Fenotipagem sem fonte/identificação completa")
    regs=[]
    for item in d.to_dict("records"):
        b=dict(item)
        b["valor_simulado"]=None
        b["erro_sim_menos_obs"]=None
        b["tipo_confronto"]="proxy_sem_equivalencia"
        if str(item["sitio_id"])!=str(site_id):
            b["tipo_confronto"]="local_incompativel"
        elif item["origem"]=="campo" and str(item["comparavel"]).lower() in ("sim","true","1") and item["variavel"] in UNIDADES_COMPATIVEIS and item["unidade"] in UNIDADES_COMPATIVEIS[item["variavel"]]:
            sub=mensal[(mensal.genotipo==item["genotipo"]) &
                      (mensal.solo==item["solo"]) & (mensal.clima=="historico") &
                      (mensal.dano=="controle") & (mensal.ano_mes==str(item["ano_mes"]))]
            if len(sub)==1:
                m=float(sub.iloc[0][item["variavel"]])
                b["valor_simulado"]=m
                b["erro_sim_menos_obs"]=m-float(item["valor"])
                b["tipo_confronto"]="campo_compativel_declarado"
            else: b["tipo_confronto"]="sem_coincidencia_temporal"
        regs.append(b)
    return pd.DataFrame(regs)


def executar(arquivo_config,dir_saida):
    c=carregar_config(arquivo_config)
    plano=planejar(c)
    base=Path(arquivo_config).resolve().parent
    resolve=lambda p: (base/p).resolve() if p else None
    hist=_ler_clima(resolve(c["clima"]["historico_csv"]))
    d=pd.read_csv(resolve(c["clima"]["deltas_climbra_csv"]))
    validar_deltas(d,c["clima"]["geadas"])
    meteo={ssp:perturbar(hist,d,ssp,c["clima"]["geadas"]) for ssp in CLIMAS}
    mensal,finais=simular(c,plano,meteo)
    fatores=contrastes(finais)
    obs=confrontar_fenotipos(mensal,resolve(c.get("fenotipagem_csv")) if c.get("fenotipagem_csv") else None,c["sitio"]["id"])
    destino=Path(dir_saida)
    destino.mkdir(parents=True,exist_ok=True)
    pd.DataFrame(plano).to_csv(destino/"matriz_cenarios.csv",index=False)
    mensal.to_csv(destino/"simulacoes_mensais.csv",index=False)
    finais.to_csv(destino/"resultados_84_meses.csv",index=False)
    fatores.to_csv(destino/"contrastes_genotipo_solo_clima_pragas.csv",index=False)
    if len(obs): obs.to_csv(destino/"confronto_fenotipagem.csv",index=False)
    relatorio=dict(status="executado_sem_validacao_biologica",n_base=12,n_cenarios=len(plano),
                   n_pragas=len(c.get("pragas",[])),n_fenotipos=len(obs),
                   motor="3-PGpjs porte Python existente na Akademia; não é execução direta do R r3PG",
                   fonte_clima=c["clima"]["fonte_climbra"],
                   fonte_periodos=[c["clima"]["periodo_referencia"],c["clima"]["periodo_futuro"]],
                   ressalvas=["As classes G1/G2 não demonstram tolerância sem fenotipagem e teste independente",
                             "A biomassa aérea aproximada não equivale automaticamente a GEDI AGBD",
                             "Cenários de pragas impõem a intensidade/frequência; não estimam risco de ocorrência",
                             "A comparação de GEDI ou índices espectrais não é validação automática",
                             "Mudanças de dias de geada só são consideradas quando fornecidas"],
                   configuracao=c)
    (destino/"manifesto_execucao.json").write_text(json.dumps(relatorio,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return relatorio


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config",required=True,type=Path)
    p.add_argument("--modo",choices=["planejar","executar"],default="planejar")
    p.add_argument("--saida",default="experimentos/integrado/saida")
    args=p.parse_args()
    c=carregar_config(args.config)
    if args.modo=="planejar":
        print(json.dumps(dict(n_cenarios=len(planejar(c)),cenarios=planejar(c)),ensure_ascii=False,indent=2))
    else:
        print(json.dumps(executar(args.config,args.saida),ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
