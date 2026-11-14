# Experimento integrado — genótipo × textura × clima + pragas + fenotipagem

**Objetivo:** executar a proposta aprovada em **12 combinações principais** (2 genótipos × 2 texturas de solo × 3 condições climáticas) e, separadamente, analisar o efeito condicional de eventos de pragas e doenças, mantendo uma mesma estrutura para fenotipagem e confrontos empíricos.

## O que funciona

| Arquivo | Função |
|---|---|
| `config.modelo.json` | Contrato de dados e proveniência, sem parâmetros inventados |
| `cenarios.py` | Gera as 12 condições e amplia com cenários de dano opcionais |
| `gerar_deltas_climbra.py` | Agrega séries diárias CLIMBra por GCM e extrai variações climáticas mensais reais |
| `executar.py` | Executa cada condição no motor Python 3-PGpjs existente, com eventos de dano |
| `test_*.py` | Testes sintéticos de execução, integridade dos cenários e métricas |
| `../../sensoriamento/earthengine/extrair_gedi_sent2_talhoes.js` | Exporta GEDI + Sentinel-2 por talhão pelo Earth Engine |
| `../../sensoriamento/importar_gee.py` | Normaliza observações GEDI/Sentinel-2 e calcula anomalias sazonais quando há série suficiente |
| `../../plataforma/integrado.html` | Prepara o JSON de entradas e permite abrir/filtrar/exportar resultados reais |

Os cenários **sem danos** continuam sendo exatamente 12. Se você cadastrar dois cenários de praga/doença, serão mais 24 simulações de sensibilidade (12 por cenário), sem alterar o fatorial aprovado. O modo atual é **compensação fisiológica desligada** (`compensation=None`); não misturar com a versão calibrada sem uma segunda execução identificada.

## Como executar usando dados reais

### 1. Confirmar as bases do experimento
Preencha uma cópia de `config.modelo.json` com a coordenada representativa do talhão da LD Celulose, a fonte, duas classes de textura, CAD do solo em mm, densidade inicial, FR, e os parâmetros de **dois genótipos com contraste comprovado**.

Os códigos `A1` e `C5` do modelo são referências históricas que já estão no projeto (Caldeira 2020 / Borges 2009). **NÃO são identificação, parametrização nem prova de tolerância dos dois clones da LD Celulose.** Se os genótipos reais forem outros, seus 82 parâmetros precisam ser cadastrados com rastreabilidade no catálogo do motor antes da simulação.

### 2. Preparar clima de entrada
Arquivo `clima_historico_mensal.csv`: colunas `year,month,tmp_min,tmp_max,prcp,srad,frost_days` cobrindo o plantio, a inicialização do modelo e o fim dos sete anos. Temperaturas em °C, chuva mensal em mm, radiação média diária MJ m⁻² d⁻¹, geadas em dias/mês.

CLIMBra (Ballarin et al., 2023): o conjunto diário corrigido por viés abrange SSP2-4.5 e SSP5-8.5, com histórico 1980–2013 e projeções 2015–2100, resolução 0,25°. **O download e o recorte de grade/GCM devem ser feitos do repositório científico oficial**, com coordenadas, modelos e período registrados.

Depois de recortar e normalizar os dados diários, a tabela de entrada deve trazer `gcm,cenario,data,tasmin_c,tasmax_c,pr_mm_d,rss_mj_m2_d`. Com os períodos efetivamente escolhidos, execute:

```bash
python3 experimentos/integrado/gerar_deltas_climbra.py \
  --entrada dados_climbra_diarios_normalizados.csv --saida clima_ld/ \
  --referencia 1981 2010 --futuro 2041 2070 \
  --fonte "CLIMBra — Ballarin et al. (2023), DOI e versão dos arquivos" \
  --celula "latitude, longitude, resolução, método de extração"
```

Este comando calcula os deltas **por GCM** e usa a mediana do conjunto de modelos que fornece todas as variáveis exigidas. Salva `deltas_climbra_mensais.csv`, `deltas_por_gcm.csv` e um manifesto com SHA-256 do arquivo de entrada.

O CLIMBra informa radiação solar **líquida** (`rss`), mas o 3-PG utiliza radiação incidente. Usar a **razão** da primeira para perturbar a segunda é uma hipótese que precisa de avaliação de plausibilidade. A projeção futura do CO₂ e a alteração de extremos diários **não** são consideradas aqui; esta execução mede o efeito climático condicional definido pelas entradas.

### 3. Planejar e executar
```bash
python3 experimentos/integrado/executar.py --config experimento_ld.json --modo planejar
python3 experimentos/integrado/executar.py --config experimento_ld.json --modo executar --saida saida_ld/
```

Saídas geradas: `matriz_cenarios.csv`, `simulacoes_mensais.csv`, `resultados_84_meses.csv`, `contrastes_genotipo_solo_clima_pragas.csv`, `interacoes_genotipo_solo_clima.csv`, `manifesto_execucao.json`.

A tabela `interacoes_genotipo_solo_clima.csv` responde explicitamente à pergunta aprovada:
para cada SSP e dano, calcula a vantagem G2−G1 no solo arenoso e argiloso, sua mudança
em relação ao histórico e o contraste de diferenças que caracteriza a interação tripla.
`modulacao_adicional_por_dano` compara esse contraste sob ataque com o controle.
São resultados do fatorial simulado, **sem inferência estatística nem validação de campo**.

A compensação fisiológica é opcional: inclua no JSON o objeto
`"compensacao":{"modo":"parametros_explicitos","U":...,"gam":...,"a":...,"u_meses":...,"fonte":"..."}`
com **valores identificados na fonte**, caso queira habilitar a extensão já implementada.
A calibração histórica de Bertulio continua sob auditoria e não é ativada automaticamente.

O módulo executa a **porta Python já existente do 3-PGpjs**, não uma chamada direta ao R/r3PG. Para cumprir integralmente o método aprovado, ainda é necessário confrontar os controles e resultados com a implementação **r3PG em R**, com versão e commit registrados.

### 4. Pragas, doenças e recuperação
Cada evento é definido por `tipo: desfolha | eficiencia | mortalidade`, `idade_meses` e `fracao` (0 a menos de 1), além de agente, fonte e classe de evidência. O cenário pode conter vários eventos e mecanismos em sequência temporal.

O mecanismo é **imposto**: não representa previsão de incidência de uma praga, severidade observada, sobrevivência empiricamente calibrada ou causalidade atribuída a um índice espectral. Eventos anteriores à inicialização do material genético devem ser excluídos do cronograma.

Os contrastes calculados distinguem: diferença futura versus clima histórico, diferença sob dano versus controle e G2 versus G1 na mesma condição. **G2 não significa genótipo tolerante** até que essa atribuição seja sustentada por fonte experimental.

### 5. GEDI, Sentinel-2 e fenotipagem
No <https://code.earthengine.google.com/> abra `sensoriamento/earthengine/extrair_gedi_sent2_talhoes.js`, substitua o ID do asset pelos talhões reais, confira os campos `talhao_id`, `genotipo`, `solo` e execute as tarefas de exportação para o Drive.

O script retorna, por talhão/mês com pixels válidos:
- GEDI L2A: RH98 (altura relativa do dossel);
- GEDI L2B: PAI (índice de área de **plantas**, não LAI foliar exato);
- GEDI L4A: AGBD (biomassa aérea **predita**, com incerteza própria);
- Sentinel-2: NDVI e NDRE (sinais espectrais, não diagnósticos de pragas).

```bash
python3 sensoriamento/importar_gee.py --sitio-id ld_celulose_talhao \
  --saida fenotipagem/ gedi_*.csv
```

> Substitua `gedi_*.csv` pelos nomes **reais** dos CSVs exportados do Drive (GEDI e Sentinel-2). Eles precisam conter identificadores de talhão e suas classes correspondentes.

Para incorporar os proxies ao relatório, aponte `fenotipagem_csv` do JSON para `fenotipagem/fenotipagem_gee_importada.csv`. O orquestrador **não calcula erro observado×simulado para GEDI**: são variáveis distintas, sem equivalência definida. Uma tabela de medições de campo com mesmo local, data, unidade, variável e declaração de comparabilidade pode produzir erros, mas não deve ser confundida com validação independente se tiver sido usada na calibração.

### 6. Interface
Execute `python3 plataforma/construir.py`. Abra `plataforma/integrado.html` ou `docs/integrado.html`. Acesse pelo botão **Genótipo × solo × clima × pragas** no simulador principal. Faça upload dos CSVs produzidos; a página filtra resultados, permite exportação e exibe curvas mensais sem pré-simulações.

## Faltas reais antes de declarar resultados da proposta

1. Delimitação/coordenada de plantio e autorização de uso dos talhões da LD.
2. Identificação dos dois genótipos, medições de tolerância térmica/hídrica e parametrização com fonte.
3. CAD, textura e profundidade medidas/derivadas para os dois solos.
4. Séries CLIMBra efetivas no local, metadados GCM/SSP, períodos e deltas.
5. Confronto independente com r3PG/R e fenotipagem de campo compatível.
6. Decisão documentada sobre compensação e persistência após ataques (o déficit de longo prazo permanece uma limitação conhecida do TCC).

**Aprovado não significa já executado ou validado.** Os testes incluídos usam dados SINTÉTICOS só para verificar o programa. Nenhum parâmetro, clima futuro ou resultado de campo da LD foi inventado.

## Fontes essenciais
- Ballarin, A. S. et al. (2023). *CLIMBra - Climate Change Dataset for Brazil*. Scientific Data 10, 47. <https://doi.org/10.1038/s41597-023-01956-z>
- r3PG — documentação de clima e execução: <https://cran.r-project.org/package=r3PG>
- GEDI L2A: <https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI02_A_002_MONTHLY>
- GEDI L2B: <https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI02_B_002_MONTHLY>
- GEDI L4A: <https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI04_A_002_MONTHLY>
- Sentinel-2: <https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED>
