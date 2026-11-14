# Progresso
## Feito
- TCC v. 31/10 (manhã): 41 p., 9 figuras, 11 tabelas; auditoria 204/204; 36 testes (substituída pela versão da noite, abaixo).
- Plataforma: conceitos (49), modo explicar, cubagem e taper seccional.
- Calibração v3 (d = 0,999): U mediana 1,16 [IC90% 1,02–1,33]; a mediana 0,55 [0,05–0,975].
  Ajuste C5 (vol/CAP/alt, %): obs 52,9/24,2/19,1; original 64,8/28,5/34,7; calibrado 50,4/20,2/24,9.
  Teste A1-urocam, mesmo experimento, não independente (vol/CAP): obs 59,0/22,9; original 79,3/40,7; calibrado 64,8/29,7 (IC90% vol 53,7–78,6; CAP 22,5–40,0).
- Biomas: clima NASA POWER e solo (ALM 219 mm, ARA 194 mm, ELD 145 mm TECHS 6) prontos; controles rodados.
- Testes da v3: 13 novos (49 no total), todos aprovados (modelo/testes/test_compensacao_v3.py).
- Validação qualitativa E. globulus (calibracao/saida/validacao_globulus.csv): sem perda de DAP/altura nas duas versões
  (fraco para discriminar); IAF aos 18 meses (Barry), perda em relação ao controle: original 8,3%, calibrado 1,4% (IC90% −2,4 a 6,7) → mais próximo
  de "área foliar sem diferença".
- Bloco por bioma (experimentos/run_biomas.py → saida/biomas/): 1.728 tratamentos × 2 versões; a versão original reproduz
  o bloco LOCAL do TCC (diferença máx. 3e-14). Calibrado reduz perdas (ex.: IND A1 50% PA 13,8 → 8,8%) e a recuperação
  relativa de 23–35 para 8–15 meses (exceto ARA, 2–8). Incerteza (200 amostras) em incerteza_posterior_d50.csv.
- RF 6 locais (saida/biomas/rf_*.csv): importância perda de volume — intensidade 50,6/47,3%, frequência 44,3/42,1%
  (original/calibrado). Local fora, RQEM média: original 63% (local categórico) e 66% (clima numérico); calibrado 143% e 69%
  (descrever o clima por números melhora a transferência na versão calibrada; R² 0,17 → 0,83).
- Morris C5, 6 locais (morris_C5_6locais.csv): nWs é o mais influente em todos; depois k, y ou SLA1, conforme o local; dominam a perda de volume em todos os locais.
- Danos, 6 locais, C5 (danos_6locais.csv): formigas original 2,5–6,6% (−0,6 em ARA) → calibrado 0,5–3,0%; em ARA a desfolha
  economiza água e o original dá ganho (−2,5% lagarta), atenuado na calibrada (−0,4%).
- Plausibilidade ARA: biomassa aérea simulada aos 54 meses 57–62 t/ha × 51–132 t/ha (média 88) de 15 clones na estação do IPA
  (Alves et al., 2007, Rev. Ciênc. Agrár. 48:161-173; 3 × 2 m; ~650 mm). Dentro da faixa, abaixo da média. ELD: sem dado
  publicado de produtividade localizado (não independente de qualquer forma).
- TCC v. 31/10 noite: 49 p., 9 figuras, 13 tabelas. Novas seções 3.12 (compensação e calibração), 3.13 (biomas),
  4.10, 4.11 (Tabelas 10 e 11); plataforma → 3.14/4.12; limitações → 4.13 (b) e (j)/(k) revistas; objetivos (+2),
  introdução, resumo/abstract, palavras-chave, conclusões (+2), siglas e símbolos, 5 referências novas (Alves 2007,
  IBGE 2024, McNabb e Wadouski 1999, OpenStreetMap, Silva, Mauro e Almeida 2019), Apêndice B. Auditoria: 336/336.
- Missão 07 (auditoria científica e cienciométrica), concluída em 31/10: revisao_07/. Parecer B (encaminhar com ressalvas).
  Correções: o urocam passou de "validação" a "teste do mesmo experimento"; Bertulio deixou de ser descrito como único
  experimento; precedentes 3PG.d (Rua et al., 2020) e CABALA (Pinkard 2011/2014); evidência contrária de Matrangolo (2010):
  o módulo subestima perdas após desfolha total precoce por fator de 6 a 34; Quentin (2011): γ ≈ 1; U sensível ao prior
  (1,21 com limite 1,6); limitações (a)–(o); Apêndice C (busca). TCC com 53 p., 14 tabelas; auditoria 363/363.
- Plataforma v8 (31/10): diferenciais em relação ao 3PG.d — compensação calibrada com incerteza, 6 biomas, outros danos com catálogo, perda por produto, domínio de validade; JS = Python (7 cenários, 1,4e-14). TCC rev08 com 3.14/4.12 atualizados; auditoria 367/367.
- TCC rev09 (31/10): todo o trabalho descrito no texto (plataforma didática, cubagem e toras, perda por produto, reprodutibilidade e auditorias). 55 p.; auditoria 379/379.
- TCC rev10 (31/10): seções 3.15/4.13 — possibilidades do módulo (ganho raro, recuperação de folhas ≠ de volume, aditividade) e validação cruzada (k-fold do metamodelo; LOO da calibração). 59 p.; auditoria 461/461.
## Falta (em ordem)
1. OpenAlex: rodar revisao_07/busca/openalex_busca.py após o reset do limite e atualizar a cienciometria.
3. Revisão do texto pelo autor e envio aos orientadores (1ª semana de novembro).
4. Defesa: documento de preparação e slides.
- 02/11: ressalvas do parecer reduzidas a 1 (persistência das perdas após desfolha total precoce, Matrangolo). TCC VERSÃO FINAL v2, 35 p.; auditoria 506/506.
- 02/11 (tarde): VERSÃO FINAL v3 (37 p.) — dossel corrigido, U de curta duração, teste independente que separa as versões; auditoria 528/528. Ressalva única: persistência das perdas após desfolha total precoce (Matrangolo).
- 02/11 (16h): VERSÃO FINAL v4 com perspectivas na conclusão; passagem de bastão para o Astra (PASSAGEM_ASTRA.md).

- 14/11/2026 — Auditoria 03 (fork/branch de trabalho): revisão de 24 registros numéricos e confronto externo pontual Oliveira; resultados aritméticos coerentes no CSV/JSON existente; distinção corrigida Bertulio (calibração e teste do mesmo experimento) vs Oliveira/Matrangolo (confrontos externos). Criados auditor de evidências, testes unitários e workflow CI. Pipeline não publica em `main` por padrão nem com `--publish`.
- Pendente da Auditoria 03: confirmar o workflow GitHub Actions no PR, reexecutar pipeline científico completo no checkout, reconferir as tabelas dos artigos originais, corrigir a persistência em longo prazo apenas com mecanismo e fonte sustentados, harmonizar TCC v8 com código/memória do fork, regenerar passagem de bastão.

- 14/11/2026 — Em branch isolada, acrescentada ferramenta **operacional**: motor existente roda 12 combinações e eventos de danos adicionais, entrega evolução mensal, resultados a 84 meses, diferenças para histórico/controle e interação tripla genótipo×solo×clima; parser CLIMBra por GCM e extrator/normalizador Earth Engine. Interface permite preparar configuração, carregar CSV reais e filtrar resultados/fenotipagem. Testes automatizados só com clima/solo artificiais **como fixtures de software**, não resultados científicos. Falta aplicar em dados reais da LD, avaliação de precisão contra inventário e checagem com r3PG em R.


## Atualização de progresso — 14/11/2026
### Feito nesta etapa documental
- Elaborado `planejamento/MAPA_MESTRE_TCC_AKADEMIA.md`, mapa mestre com pergunta integradora, objetivos, arquitetura, desenho 2×2×3, pacotes P0–P11, dependências, riscos e critérios de aceite.
- Aberto PR #4: https://github.com/tomdeatj-commits/Akademia/pull/4. Branch: `docs/mapa-mestre-tcc-akademia`. Commit do mapa: `4fd2d13331aa2b4cd5636eab321066db0e10093b`.
- Atualização é de planejamento/documentação. Não houve alteração de equações, parâmetros, dados de entrada, resultados ou motor científico. Nenhuma nova simulação foi executada nesta etapa.
### Falta — ordem de execução revisada
1. Revisar e mesclar PR #4 somente após auditoria do autor.
2. Fazer checkout completo e executar `python3 ferramentas/pipeline.py verificar`; confirmar CI e reexecutar testes/pipeline conforme instruções do AGENTS.md.
3. Regenerar passagem e contexto empacotado com `python3 ferramentas/gerar_passagem.py` no checkout completo; confirmar o conteúdo produzido e registrar commit/log.
4. Fechar P1: reconciliação das fontes primárias, auditoria de evidências e matriz observado×previsto; preservar ressalva de persistência de longo prazo após desfolha total precoce.
5. Fechar P2: busca recente e fichas de Stape/Hélio Garcia Leite; identificar genótipos contrastantes e verificar disponibilidade de parâmetros 3-PG comparáveis.
6. Fechar P3/P4: definir ponto regional sem alegar talhão da LD; extrair solo/água e CLIMBra/histórico com metadados, unidades, resolução e incerteza.
7. Executar P5: 12 combinações, horizonte de sete anos, somente após congelar entradas e protocolo.
8. Acrescentar P6/P7/P8 como módulos separados e documentados; avaliar em P9 com observações independentes apropriadas.
9. Consolidar P10/P11 apenas com funcionalidades e resultados efetivamente verificados.
### Bloqueios e limites
- Dados privados da LD, clones, inventários e parcelas: não disponíveis/presumidos; escopo territorial público apenas.
- Dados reais CLIMBra, genótipos, CAD/solo e observações GEDI/Sentinel precisam de extração e auditoria antes de simular.
- Fixtures sintéticas usadas nos testes existentes não constituem evidência científica nem validação do modelo.