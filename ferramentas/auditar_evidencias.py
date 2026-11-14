#!/usr/bin/env python3
"""Conferência aritmética e classificação de evidências existentes (sem recalibrar).
Uso: python3 ferramentas/auditar_evidencias.py [--output relatorio.json]
Os dados publicados precisam de conferência com os artigos primários em separado.
"""
import argparse
import csv
import json
import math
from pathlib import Path


def perda_pct(controle, tratamento):
    if not all(map(math.isfinite, (controle, tratamento))) or controle <= 0:
        raise ValueError("controle deve ser positivo e os valores devem ser finitos")
    return 100 * (1 - tratamento / controle)


def auditar_pares(linhas):
    problemas, bases, contagens = [], {}, {}
    for i, r in enumerate(linhas, 2):
        estudo = r.get("study_id", "")
        contagens[estudo] = contagens.get(estudo, 0) + 1
        chave = (r.get("especie_ou_clone"), r.get("variavel"))
        try:
            c, t = float(r["valor_controle"]), float(r["valor_tratamento"])
            informado = float(r["L_obs_pct_calculado"])
            calculado = round(perda_pct(c, t), 3)
            if abs(calculado - informado) > 0.00051:
                problemas.append(f"linha {i}: perda informada {informado} != {calculado}")
            if estudo == "Bertulio_2008" and int(r["idade_meses"]) == 14:
                bases[chave] = (c, t)
        except (ValueError, TypeError, KeyError) as exc:
            problemas.append(f"linha {i}: registro inválido: {exc}")
    for i, r in enumerate(linhas, 2):
        if r.get("study_id") != "Bertulio_2008" or r.get("idade_meses") != "26":
            continue
        try:
            c, t = float(r["valor_controle"]), float(r["valor_tratamento"])
            bc, bt = bases[(r["especie_ou_clone"], r["variavel"])]
            calculado = round(100 * (1 - (t/c)/(bt/bc)), 3)
            informado = float(r["L_obs_pct_ajustado_linha_base"])
            if abs(calculado - informado) > 0.00051:
                problemas.append(f"linha {i}: ajuste de linha de base {informado} != {calculado}")
        except (ValueError, TypeError, KeyError, ZeroDivisionError) as exc:
            problemas.append(f"linha {i}: falha na linha de base: {exc}")
    return contagens, problemas


def auditar_oliveira(registro):
    try:
        t1 = registro["resultados"]["T1 100%"]
        obs = float(t1["observado"]["volume_publicado"])
        prev = float(t1["calibrado"]["volume"][1])
        declarado = float(registro["resultados"]["T1_metricas"]["erros_calibrado"][0])
        delta = round(prev - obs, 3)
        erros = [] if abs(delta - declarado) < 0.051 else [f"Oliveira: erro informado {declarado} != {delta} p.p."]
        return {"observado_pct": obs, "simulado_pct": prev, "desvio_pp": delta}, erros
    except (KeyError, TypeError, ValueError, IndexError) as exc:
        return {}, [f"Oliveira: entrada inválida: {exc}"]


def executar(raiz):
    with (raiz / "revisao/dados_tratamentos_observados_verificado.csv").open(encoding="utf-8-sig", newline="") as f:
        pares = list(csv.DictReader(f))
    with (raiz / "calibracao/saida/teste_oliveira2014.json").open(encoding="utf-8") as f:
        oliveira = json.load(f)
    contagens, problemas = auditar_pares(pares)
    confronto, outros = auditar_oliveira(oliveira)
    problemas.extend(outros)
    return {
        "status": "PASSOU" if not problemas else "FALHOU",
        "registros": len(pares), "por_estudo": contagens,
        "oliveira_t1": confronto, "problemas": problemas,
        "papel_cientifico": {
            "Bertulio_2008": "calibração + teste interno do mesmo experimento; não é teste externo independente",
            "Matrangolo_2010": "confronto externo de longo prazo, persistência ainda subestimada",
            "Oliveira_2014": "confronto externo pontual de curto prazo; não validação ampla"
        },
        "limites": [
            "Confere operações sobre CSV/JSON existentes; não comprova transcrição dos artigos.",
            "Não reexecuta o r3PG, a calibração nem o confronto de longo prazo.",
            "Dados de desfolha total (100%) não são intercambiáveis com cenários de 95%."
        ]
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--output", type=Path)
    a = p.parse_args()
    relatorio = executar(a.root)
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(json.dumps(relatorio, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))
    raise SystemExit(bool(relatorio["problemas"]))
