"""Testes operacionais SEM DADOS DE CAMPO: fixtures sintéticas não são resultados científicos."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

DIRETORIO=Path(__file__).resolve().parent
sys.path.insert(0,str(DIRETORIO))
import cenarios
import executar


def configuracao():
    return {
        "sitio":{"id":"local_teste","latitude":-19.0,"longitude":-47.0,"fonte":"SINTETICO_TESTE"},
        "plantio":"2015-01","idade_final_meses":84,
        "densidade_inicial_ha":1111.111,"fonte_densidade":"SINTETICO_TESTE",
        "fertilidade_fr":0.8,"fonte_fr":"SINTETICO_TESTE",
        "fracao_agua_inicial":1.0,
        "genotipos":[
          {"id":"G1","codigo_material":"A1","fonte_parametros":"codigo existente; teste sintético",
           "classe_tolerancia":"nao_verificada"},
          {"id":"G2","codigo_material":"C5","fonte_parametros":"codigo existente; teste sintético",
           "classe_tolerancia":"nao_verificada"}],
        "solos":[{"id":"arenoso","soil_class":1,"cad_mm":100.0,"fonte":"SINTETICO_TESTE"},
                 {"id":"argiloso","soil_class":4,"cad_mm":220.0,"fonte":"SINTETICO_TESTE"}],
        "clima":{"historico_csv":"historico.csv","deltas_climbra_csv":"deltas.csv",
                 "fonte_climbra":"SINTETICO_TESTE, NAO CLIMBra REAL",
                 "periodo_referencia":"teste","periodo_futuro":"teste",
                 "geadas":"dias_futuros_no_delta"},
        "pragas":[{"id":"ataque_de_teste","agente":"não representa praga observada",
                   "fonte":"SINTETICO_TESTE","classificacao":"hipotese",
                   "eventos":[{"tipo":"desfolha","idade_meses":24,"fracao":0.25}]}]
    }


def arquivos_clima(pasta):
    tempo=pd.period_range("2015-01","2022-01",freq="M")
    historico=pd.DataFrame([dict(year=t.year,month=t.month,tmp_min=18.0,
                                tmp_max=30.0,prcp=120.0,srad=18.0,frost_days=0)
                            for t in tempo])
    historico.to_csv(pasta/"historico.csv",index=False)
    deltas=pd.DataFrame([
        dict(ssp=ssp,month=m,delta_tmin_c=delta,delta_tmax_c=delta,
             fator_precipitacao=1.0,fator_radiacao=1.0,
             fonte="SINTETICO_TESTE",periodo="teste",frost_days=0)
        for ssp,delta in [("SSP2-4.5",1.0),("SSP5-8.5",2.0)]
        for m in range(1,13)
    ])
    deltas.to_csv(pasta/"deltas.csv",index=False)
    return historico,deltas


class CenariosIntegradosTeste(unittest.TestCase):
    def test_fatorial_12_e_pragas_camada_separada(self):
        c=configuracao()
        nomes=cenarios.planejar(c)
        self.assertEqual(len(nomes),24)
        self.assertEqual(sum(x["dano"]=="controle" for x in nomes),12)
        self.assertEqual(len(set(x["id"] for x in nomes)),24)

    def test_nao_presumir_tolerancia(self):
        c=configuracao()
        c["genotipos"][0]["classe_tolerancia"]="tolerante"
        with self.assertRaisesRegex(ValueError,"fonte_tolerancia"):
            cenarios.validar_config(c)

    def test_nao_inventar_cad(self):
        c=configuracao()
        c["solos"][0]["cad_mm"]=None
        with self.assertRaisesRegex(ValueError,"CAD"):
            cenarios.validar_config(c)

    def test_perturbacao_e_vpd_derivado(self):
        with tempfile.TemporaryDirectory() as d:
            historico,deltas=arquivos_clima(Path(d))
            hist=historico.assign(tmp_ave=24.0,vpd_day=1.5)
            out=cenarios.perturbar(hist,deltas,"SSP2-4.5","dias_futuros_no_delta")
            self.assertAlmostEqual(out.tmp_min.iloc[0],19)
            self.assertAlmostEqual(out.tmp_max.iloc[0],31)
            self.assertNotIn("vpd_day",out.columns)
            self.assertAlmostEqual(out.prcp.iloc[0],120)

    def test_sem_cenario_futuro_gera_erro(self):
        with tempfile.TemporaryDirectory() as d:
            _,deltas=arquivos_clima(Path(d))
            with self.assertRaises(ValueError):
                cenarios.validar_deltas(deltas.iloc[:-1],"dias_futuros_no_delta")

    def test_fenotipagem_gedi_nao_valida_diretamente(self):
        mensal=pd.DataFrame([dict(genotipo="G1",solo="arenoso",clima="historico",
                                  dano="controle",ano_mes="2022-01",volume=12)])
        obs=pd.DataFrame([
           dict(genotipo="G1",solo="arenoso",ano_mes="2022-01",variavel="volume",
                valor=11.0,unidade="m3/ha",fonte="teste",origem="campo",
                comparavel="sim",sitio_id="local_teste"),
           dict(genotipo="G1",solo="arenoso",ano_mes="2022-01",variavel="agbd",
                valor=100.0,unidade="Mg/ha",fonte="GEDI",origem="GEDI_L4A",
                comparavel="nao",sitio_id="local_teste")])
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"observado.csv";obs.to_csv(f,index=False)
            out=executar.confrontar_fenotipos(mensal,f,"local_teste")
            self.assertEqual(out.loc[0,"tipo_confronto"],"campo_compativel_declarado")
            self.assertAlmostEqual(out.loc[0,"erro_sim_menos_obs"],1)
            self.assertEqual(out.loc[1,"tipo_confronto"],"proxy_sem_equivalencia")
            self.assertTrue(pd.isna(out.loc[1,"erro_sim_menos_obs"]))

    def test_execucao_com_motor_existente_e_arquivos(self):
        with tempfile.TemporaryDirectory() as d:
            raiz=Path(d)
            c=configuracao()
            arquivos_clima(raiz)
            arquivo=raiz/"config.json"
            arquivo.write_text(json.dumps(c),encoding="utf-8")
            output=raiz/"saida"
            resultado=executar.executar(arquivo,output)
            self.assertEqual(resultado["n_base"],12)
            self.assertEqual(resultado["n_cenarios"],24)
            final=pd.read_csv(output/"resultados_84_meses.csv")
            self.assertEqual(len(final),24)
            self.assertEqual(set(final["dano"]),{"controle","ataque_de_teste"})
            self.assertTrue((final["data_final"]=="2022-01-31").all())
            fatores=pd.read_csv(output/"contrastes_genotipo_solo_clima_pragas.csv")
            self.assertEqual(len(fatores),24*5)
            self.assertTrue((output/"simulacoes_mensais.csv").exists())
            self.assertEqual(resultado["status"],"executado_sem_validacao_biologica")


if __name__=="__main__":
    unittest.main()
