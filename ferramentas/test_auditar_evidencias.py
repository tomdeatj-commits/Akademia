"""Testes das evidências e da proteção contra publicação em main."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
from auditar_evidencias import auditar_pares, auditar_oliveira, perda_pct
import pipeline


class RastreabilidadeTest(unittest.TestCase):
    def test_perda_pct(self):
        self.assertAlmostEqual(perda_pct(469.1, 291.4), 37.88104881688339)

    def test_controle_zero_recusado(self):
        with self.assertRaises(ValueError):
            perda_pct(0, 10)

    def test_detectar_divergencia(self):
        linhas = [dict(study_id="Matrangolo_2010", idade_meses="92",
                       valor_controle="100", valor_tratamento="50",
                       L_obs_pct_calculado="99")]
        _, erros = auditar_pares(linhas)
        self.assertTrue(erros)

    def test_baseline_bertulio(self):
        comum = {"study_id": "Bertulio_2008", "especie_ou_clone": "clone fictício de teste",
                 "variavel": "volume"}
        d0 = dict(comum, idade_meses="14", valor_controle="100", valor_tratamento="90",
                  L_obs_pct_calculado="10.000")
        d1 = dict(comum, idade_meses="26", valor_controle="200", valor_tratamento="90",
                  L_obs_pct_calculado="55.000", L_obs_pct_ajustado_linha_base="50.000")
        _, erros = auditar_pares([d0, d1])
        self.assertFalse(erros)

    def test_oliveira(self):
        j = {"resultados": {
            "T1 100%": {"observado": {"volume_publicado": 35.4},
                        "calibrado": {"volume": [16.8, 33.0, 37.3]}},
            "T1_metricas": {"erros_calibrado": [-2.4]}
        }}
        confronto, erros = auditar_oliveira(j)
        self.assertFalse(erros)
        self.assertAlmostEqual(confronto["desvio_pp"], -2.4)

    def test_nao_publica_sem_flag(self):
        with patch.object(pipeline.sys, "argv", ["pipeline.py", "verificar"]), \
                patch.object(pipeline.subprocess, "run") as run:
            pipeline.commit("teste")
            run.assert_not_called()

    def test_recusa_publicar_na_main(self):
        with tempfile.TemporaryDirectory() as tmp:
            raiz = Path(tmp)
            (raiz / ".git").mkdir()
            fake = subprocess.CompletedProcess([], 0, stdout="main\n")
            with patch.object(pipeline, "RAIZ", raiz), \
                    patch.object(pipeline.sys, "argv", ["pipeline.py", "--publish", "verificar"]), \
                    patch.object(pipeline.subprocess, "run", return_value=fake) as run:
                with self.assertRaisesRegex(RuntimeError, "main/master"):
                    pipeline.commit("teste")
                self.assertEqual(run.call_count, 1)


if __name__ == "__main__":
    unittest.main()
