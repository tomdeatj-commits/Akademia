"""Planejamento e perturbações de clima: 2 genótipos × 2 solos × 3 cenários.
Sem valores climáticos ou edáficos presumidos. O campo 'fonte' é obrigatório.
"""
from __future__ import annotations
import calendar
import math

CLIMAS = ("historico", "SSP2-4.5", "SSP5-8.5")
TIPOS_DANO = ("desfolha", "eficiencia", "mortalidade")
COLUNAS_DELTA = ("ssp", "month", "delta_tmin_c", "delta_tmax_c",
                 "fator_precipitacao", "fator_radiacao", "fonte", "periodo")


def validar_config(c):
    erros = []
    def exigir(cond, msg):
        if not cond:
            erros.append(msg)
    genes, solos = c.get("genotipos", []), c.get("solos", [])
    exigir(len(genes) == 2, "São exigidos dois genótipos distintos")
    exigir(len(solos) == 2, "São exigidos dois solos com textura contrastante")
    exigir({g.get("id") for g in genes} == {"G1", "G2"} if len(genes)==2 else False,
          "Identifique os genótipos como G1 e G2 (sem presumir tolerância)")
    exigir({s.get("id") for s in solos} == {"arenoso", "argiloso"} if len(solos)==2 else False,
          "As texturas precisam ser arenoso e argiloso")
    for g in genes:
        exigir(bool(g.get("codigo_material")), "Cada genótipo precisa de codigo_material com parâmetros rastreáveis")
        exigir(bool(g.get("fonte_parametros")), "Falta fonte_parametros do genótipo")
        if g.get("classe_tolerancia") in ("tolerante", "sensivel"):
            exigir(bool(g.get("fonte_tolerancia")), "Classe de tolerância requer fonte_tolerancia")
    for s in solos:
        exigir(s.get("soil_class") == (1 if s.get("id") == "arenoso" else 4),
              "soil_class 1 (arenoso) ou 4 (argiloso), conforme r3PG")
        cad = s.get("cad_mm")
        exigir(isinstance(cad, (int, float)) and not isinstance(cad,bool) and math.isfinite(cad) and cad > 0,
              "Cada solo exige CAD em mm, medida ou derivada de fonte identificada")
        exigir(bool(s.get("fonte")), "Falta fonte da CAD/textura do solo")
    site = c.get("sitio", {})
    lat, lon = site.get("latitude"), site.get("longitude")
    exigir(isinstance(lat,(int,float)) and -90<=lat<=90 and
          isinstance(lon,(int,float)) and -180<=lon<=180 and bool(site.get("fonte")),
          "Coordenadas representativas e fonte do sítio são obrigatórias")
    exigir(bool(c.get("plantio")), "Falta mês do plantio")
    exigir(c.get("idade_final_meses") == 84, "O protocolo aprovado estabelece 84 meses")
    n = c.get("densidade_inicial_ha")
    exigir(isinstance(n,(int,float)) and n>0 and bool(c.get("fonte_densidade")),
          "Densidade inicial precisa de valor e fonte")
    fr = c.get("fertilidade_fr")
    exigir(isinstance(fr,(int,float)) and 0<=fr<=1 and bool(c.get("fonte_fr")),
          "Fertilidade FR, igual nos solos, precisa de valor e fonte")
    exigir(0 < c.get("fracao_agua_inicial",0) <= 1, "Informe fração inicial de água, de 0 a 1")
    clim = c.get("clima",{})
    exigir(bool(clim.get("historico_csv")) and bool(clim.get("deltas_climbra_csv")),
          "Exija séries históricas e arquivo de deltas derivado do CLIMBra")
    exigir(bool(clim.get("fonte_climbra")) and bool(clim.get("periodo_referencia")) and bool(clim.get("periodo_futuro")),
          "Fonte e períodos climático-base e futuro são obrigatórios")
    exigir(clim.get("geadas") in ("dias_futuros_no_delta", "historico_fixo_com_ressalva"),
          "Defina método de dias de geada nos cenários futuros")
    for p in c.get("pragas",[]):
        exigir(bool(p.get("id") and p.get("agente") and p.get("fonte")),
              "Cada cenário de dano exige id, agente e fonte")
        exigir(p.get("classificacao") in ("hipotese", "literatura"),
              "Cada dano precisa de classificação hipótese/literatura")
        seen = set()
        for e in p.get("eventos",[]):
            tipo, mes, frac = e.get("tipo"),e.get("idade_meses"),e.get("fracao")
            exigir(tipo in TIPOS_DANO, "Tipo de dano inválido")
            exigir(isinstance(mes,int) and 1<=mes<=84, "Evento fora do período de 7 anos")
            exigir(isinstance(frac,(int,float)) and 0 <= frac < 1,
                  "Fração do evento precisa ser >=0 e <1 (100% não é aceito pelo motor)")
            key=(tipo,mes)
            exigir(key not in seen, "Eventos do mesmo mecanismo no mesmo mês precisam ser consolidados")
            seen.add(key)
    ids=[p.get("id") for p in c.get("pragas",[])]
    exigir(len(set(ids))==len(ids) and "controle" not in ids, "IDs de danos precisam ser únicos")
    if erros:
        raise ValueError("; ".join(erros))
    return c


def planejar(c):
    validar_config(c)
    cenarios = []
    for g in c["genotipos"]:
        for s in c["solos"]:
            for climate in CLIMAS:
                for p in [None] + c.get("pragas",[]):
                    pest = p["id"] if p else "controle"
                    cenarios.append(dict(id=f'{g["id"]}__{s["id"]}__{climate}__{pest}',
                                          genotipo=g["id"], solo=s["id"], clima=climate,
                                          dano=pest, tipo_resultado="simulacao"))
    return cenarios


def validar_deltas(df, geadas):
    faltas = set(COLUNAS_DELTA)-set(df.columns)
    if faltas: raise ValueError(f"Deltas climáticos sem colunas: {sorted(faltas)}")
    if geadas=="dias_futuros_no_delta" and "frost_days" not in df.columns:
        raise ValueError("Geadas futuras declaradas, mas a coluna frost_days não existe")
    pares = {(str(r.ssp), int(r.month)) for r in df.itertuples()}
    esperado={(s,m) for s in CLIMAS[1:] for m in range(1,13)}
    if len(df)!=24 or pares!=esperado:
        raise ValueError("CLIMBra: forneça exatamente 24 deltas (2 SSP × 12 meses), sem duplicações")
    cols = ["delta_tmin_c","delta_tmax_c","fator_precipitacao","fator_radiacao"]
    if df[cols].isna().any().any() or not all(math.isfinite(float(x)) for x in df[cols].to_numpy().flat):
        raise ValueError("Deltas climáticos precisam ser finitos e completos")
    if (df["fator_precipitacao"]<0).any() or (df["fator_radiacao"]<=0).any():
        raise ValueError("Fatores de precipitação/radiação inválidos")
    if (df["fonte"].astype(str).str.strip()=="").any() or (df["periodo"].astype(str).str.strip()=="").any():
        raise ValueError("Faltam metadados da fonte/período CLIMBra")
    if geadas=="dias_futuros_no_delta":
        if df["frost_days"].isna().any() or (df["frost_days"]<0).any() or (df["frost_days"]>31).any():
            raise ValueError("frost_days futuro precisa ser informado por mês (0 a 31)")
    return True


def perturbar(historico, deltas, ssp, geadas):
    if ssp=="historico": return historico.copy()
    d = deltas[deltas.ssp == ssp].set_index("month")
    out = historico.copy()
    m = out["month"].astype(int)
    out["tmp_min"] = out["tmp_min"] + m.map(d.delta_tmin_c).to_numpy()
    out["tmp_max"] = out["tmp_max"] + m.map(d.delta_tmax_c).to_numpy()
    out["prcp"] = out["prcp"] * m.map(d.fator_precipitacao).to_numpy()
    out["srad"] = out["srad"] * m.map(d.fator_radiacao).to_numpy()
    if geadas=="dias_futuros_no_delta":
        out["frost_days"] = m.map(d.frost_days).to_numpy()
    if (out.tmp_min>out.tmp_max).any() or (out.prcp<0).any() or (out.srad<=0).any():
        raise ValueError("Perturbação inválida: temperatura mínima > máxima ou precipitação/radiação inconsistente")
    # Nunca transportar VPD ou temperatura média derivados do clima original para o futuro.
    for col in ("tmp_ave","vpd_day"):
        if col in out: out=out.drop(columns=col)
    return out


def data_evento(plantio, idade_meses):
    import pandas as pd
    return str(pd.Period(plantio,freq="M")+idade_meses)


def programar_praga(plantio, dano):
    ev={"desfolha":{},"eficiencia":{},"mortalidade":{}}
    if dano is None: return ev
    for e in dano["eventos"]:
        ev[e["tipo"]][data_evento(plantio,int(e["idade_meses"]))]=float(e["fracao"])
    return ev
