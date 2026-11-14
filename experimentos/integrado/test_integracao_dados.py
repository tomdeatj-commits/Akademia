"""Verificadores de CLIMBra/GEDI com dados 100% sintéticos."""
import sys
import tempfile
import unittest
from pathlib import Path
import pandas as pd

RAIZ=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(RAIZ/"sensoriamento"))
sys.path.insert(0,str(Path(__file__).parent))
from importar_gee import integrar
from gerar_deltas_climbra import construir


class FontesIntegradasTeste(unittest.TestCase):
    def test_importacao_retem_proveniencia_e_nao_confunde_gd_com_campo(self):
        rows=[]
        for y in [2020,2021,2022,2023]:
            rows.append(dict(talhao_id="T_TESTE",genotipo="G1",solo="arenoso",
                ano_mes=f"{y}-07",produto="SENTINEL2_SR",variavel="ndvi",
                valor=.45 if y<2023 else .25,n_pixels_validos=45,
                unidade="índice sem unidade",origem="SENTINEL2_SR",comparavel="nao"))
        rows.append(dict(talhao_id="T_TESTE",genotipo="G1",solo="arenoso",
            ano_mes="2023-07",produto="GEDI_L4A",variavel="agbd",
            valor=125,n_pixels_validos=2,unidade="Mg/ha",
            origem="GEDI_L4A",comparavel="nao"))
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"export.csv"
            pd.DataFrame(rows).to_csv(f,index=False)
            dados,resumo=integrar([f],"ld_teste")
            self.assertEqual(len(dados),5)
            ano=dados[(dados.ano_mes=="2023-07")&(dados.variavel=="ndvi")].iloc[0]
            self.assertEqual(ano.n_anos_referencia,3)
            self.assertAlmostEqual(ano.desvio_sazonal,-0.2)
            self.assertTrue((dados.comparavel=="nao").all())
            self.assertTrue((dados.tipo_evidencia=="proxy_indireto_sem_ajuste").all())
            self.assertEqual(len(resumo),2)

    def test_arquivo_gee_regional_sem_genotipo_aceito_apenas_como_proxy(self):
        x=pd.DataFrame([dict(talhao_id="T",genotipo="",
            solo="arenoso",ano_mes="2022-01",produto="GEDI_L4A",
            variavel="agbd",valor=120,n_pixels_validos=2,
            unidade="Mg/ha",origem="GEDI_L4A",comparavel="nao")])
        with tempfile.TemporaryDirectory() as d:
            f=Path(d)/"export.csv"
            x.to_csv(f,index=False)
            dados,_=integrar([f],"recorte_regional")
            self.assertEqual(len(dados),1)
            self.assertTrue(pd.isna(dados.iloc[0]["genotipo"]))
            self.assertEqual(dados.iloc[0]["escopo"],"area_referencia_sem_identidade_genetica")
            self.assertEqual(dados.iloc[0]["comparavel"],"nao")

    def test_deltas_ensemble_com_periodos_e_fonte(self):
        records=[]
        for gcm in ("GCM_TESTE_A","GCM_TESTE_B"):
            for name,ini,fim,inc in [("historico",1990,1999,0),
                                      ("SSP2-4.5",2041,2050,1),
                                      ("SSP5-8.5",2041,2050,2)]:
                for date in pd.date_range(f"{ini}-01-01",f"{fim}-12-31",freq="D"):
                    records.append(dict(gcm=gcm,cenario=name,data=str(date.date()),
                            tasmin_c=18+inc,tasmax_c=29+inc,pr_mm_d=2*(1+inc*.1),
                            rss_mj_m2_d=16))
        d=pd.DataFrame(records)
        delta,por_gcm,meta=construir(d,1990,1999,2041,2050,
                                     "CLIMBra sintético TESTE","coordenada SINTETICA")
        self.assertEqual(len(delta),24)
        self.assertEqual(meta["n_modelos"],2)
        self.assertEqual(len(por_gcm),48)
        self.assertAlmostEqual(delta[(delta.ssp=="SSP2-4.5")&(delta.month==1)].delta_tmin_c.iloc[0],1)
        self.assertTrue((delta.fator_precipitacao>0).all())


if __name__=="__main__":
    unittest.main()
