"""Pipeline único do TCC II. Cada etapa é um comando; `tudo` roda na ordem. Ao final de cada etapa bem-sucedida,
regenera a passagem de bastão e faz commit (se houver git).

Uso: python3 ferramentas/pipeline.py <etapa> [<etapa> ...]
Etapas: verificar, testes, calibracao, experimentos, indicadores, analises, danos, auditoria, tcc, plataforma, passagem, tudo
"""
import subprocess, sys, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PY = sys.executable
ETAPAS = {
    "verificar": [[PY, "-c", "import numpy, pandas, sklearn; print('python ok')"], ["node", "--version"]],
    "testes": [[PY, "-m", "pytest", "-q", "modelo/testes"]],
    "evidencias": [[PY, "-m", "unittest", "discover", "-s", "ferramentas", "-p", "test_auditar_evidencias.py"],
                   [PY, "ferramentas/auditar_evidencias.py"]],
    "calibracao": [[PY, "calibrar.py", "0.999"], [PY, "calibrar.py", "0.99"], [PY, "calibrar_gamma.py"], [PY, "validacao_cruzada.py"],
                   [PY, "auditoria_calibracao.py"], [PY, "testes_adicionais.py"], [PY, "validacao_globulus.py"], [PY, "teste_oliveira2014.py"]],
    "experimentos": [[PY, "experimentos/run_experimentos.py"], [PY, "experimentos/controles.py"]],
    "indicadores": [[PY, "experimentos/indicadores.py"]],
    "analises": [[PY, "experimentos/analise.py"], [PY, "experimentos/estatisticas.py"],
                 [PY, "experimentos/validacao_kfold.py"], [PY, "experimentos/rf_figuras.py"]],
    "danos": [[PY, "experimentos/danos_v2.py"]],
    "biomas": [[PY, "experimentos/run_biomas.py"], [PY, "experimentos/rf_biomas.py"], [PY, "experimentos/morris_danos_biomas.py"]],
    "possibilidades": [[PY, "experimentos/possibilidades.py"], [PY, "experimentos/possibilidades_analise.py"]],
    "tabelas": [[PY, "tcc_docx/tabelas_dados.py"], ["node", "plataforma/extrair_material_tcc.js"], [PY, "plataforma/material_tcc.py"], [PY, "experimentos/figuras_novas.py"]],
    "auditoria": [[PY, "auditoria_final/auditar_numeros.py"]],
    "tcc": [["node", "gerar.js", "paginas.json"], ["node", "../ferramentas/conferir_texto_auditoria.js"]],
    "plataforma": [[PY, "plataforma/sincronizar_dados.py"], [PY, "plataforma/verificacao/comparar.py"], [PY, "plataforma/construir.py"]],
    "passagem": [[PY, "ferramentas/gerar_passagem.py"]],
}
CWD = {"calibracao": RAIZ / "calibracao", "tcc": RAIZ / "tcc_docx"}
ORDEM = ["verificar", "testes", "evidencias", "calibracao", "experimentos", "indicadores", "analises", "danos", "biomas", "possibilidades", "tabelas", "plataforma", "auditoria", "tcc"]


def commit(msg):
    """Publicação opt-in: nunca enviar automaticamente à branch principal."""
    if "--publish" not in sys.argv[1:]:
        return
    if not (RAIZ / ".git").exists():
        raise RuntimeError("Use --publish somente em checkout Git local")
    branch = subprocess.run(["git", "-C", str(RAIZ), "branch", "--show-current"],
                            capture_output=True, text=True, check=True).stdout.strip()
    if not branch or branch in ("main", "master"):
        raise RuntimeError("Publicação bloqueada em main/master; selecione uma branch de trabalho")
    subprocess.run(["git", "-C", str(RAIZ), "add", "-A"], check=True)
    staged = subprocess.run(["git", "-C", str(RAIZ), "diff", "--cached", "--quiet"])
    if staged.returncode == 0:
        print("[git] nenhuma alteração a publicar")
        return
    if staged.returncode != 1:
        raise RuntimeError("Falha na inspeção das alterações preparadas")
    subprocess.run(["git", "-C", str(RAIZ), "commit", "-m", msg], check=True)
    subprocess.run(["git", "-C", str(RAIZ), "push", "origin", f"HEAD:{branch}"],
                   check=True, timeout=600)
    print(f"[git] publicado em {branch}")



def rodar(etapa):
    t0 = time.time()
    for cmd in ETAPAS[etapa]:
        print(f"[{etapa}] $ {' '.join(cmd)}", flush=True)
        r = subprocess.run(cmd, cwd=CWD.get(etapa, RAIZ))
        if r.returncode != 0:
            if etapa in ("verificar", "testes", "evidencias"):
                sys.exit(r.returncode)
            print(f"[{etapa}] FALHOU (código {r.returncode}). A passagem de bastão foi atualizada com a falha registrada.")
            (RAIZ / "memoria/contexto_ativo.md").open("a", encoding="utf8").write(
                f"\n- FALHA na etapa `{etapa}` ({time.strftime('%d/%m %H:%M')}): comando `{' '.join(cmd)}`.\n")
            subprocess.run([PY, "ferramentas/gerar_passagem.py"], cwd=RAIZ)
            sys.exit(r.returncode)
    print(f"[{etapa}] ok em {time.time() - t0:.0f} s")
    if etapa not in ("passagem", "verificar", "testes", "evidencias"):
        subprocess.run([PY, "ferramentas/gerar_passagem.py"], cwd=RAIZ)
        commit(f"pipeline: etapa {etapa} concluída")


if __name__ == "__main__":
    pedidas = [a for a in sys.argv[1:] if a != "--publish"] or ["verificar"]
    for e in (ORDEM if pedidas == ["tudo"] else pedidas):
        if e not in ETAPAS:
            sys.exit(f"Etapa desconhecida: {e}. Opções: {', '.join(ETAPAS)}, tudo")
        rodar(e)
