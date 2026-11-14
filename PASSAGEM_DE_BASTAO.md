# PASSAGEM DE BASTÃO — TCC II (5948 tokens, estimativa (caracteres ÷ 3,6); gerado em 02/11/2026 16:09)

Documento gerado automaticamente por `ferramentas/gerar_passagem.py`. Serve para qualquer IA continuar o trabalho.
Para o código completo, use `CONTEXTO_EMPACOTADO.md` (24776 tokens, estimativa (caracteres ÷ 3,6)).

# AGENTS.md — instruções para qualquer IA que trabalhe neste projeto (Claude, ChatGPT/Codex, Gemini, Cursor)

Projeto: TCC II de Bernardo Teixeira de Castro (Engenharia Florestal, UFU). Módulo de desfolha (pragas e doenças)
no modelo ecofisiológico 3-PG (r3PG v0.1.7, 3-PGpjs, porta Python verificada) para eucalipto. Defesa: dez/2026.

## Antes de qualquer coisa
1. Leia `memoria/contexto_ativo.md` (o que está sendo feito agora) e `memoria/progresso.md` (feito × falta).
2. Leia `PASSAGEM_DE_BASTAO.md` se existir (gerado por `python3 ferramentas/gerar_passagem.py`).
3. Rode `python3 ferramentas/pipeline.py verificar` para conferir que o ambiente funciona.

## Regras inegociáveis
- Só dados secundários. NUNCA inventar dado, parâmetro, referência, DOI ou resultado. Sem fonte → escrever que não há.
- Distinguir verificação (código = equações), calibração (ajuste a dados) e validação (dados independentes).
- Todo número do TCC precisa ser recalculável: `auditoria_final/auditar_numeros.py` deve passar após qualquer mudança.
- O módulo original (v2) deve continuar reproduzível: `compensation=None` ⇒ resultados idênticos; testes em `modelo/testes`.
- Escrita: português do Brasil, estilo do TCC I, ABNT, frases claras e voz ativa.
- Tudo o que for entregue vai para o Google Drive, pasta 3-PG, com registro no Diário do TCC II.

## Ao terminar cada etapa
1. Atualize `memoria/contexto_ativo.md`, `memoria/progresso.md` e, se houve escolha, `memoria/decisoes.md`.
2. Rode `python3 ferramentas/gerar_passagem.py` (regenera PASSAGEM_DE_BASTAO.md e CONTEXTO_EMPACOTADO.md com contagem de tokens).
3. Faça commit com mensagem descritiva.

## Mapa
- `modelo/` 3-PG (threepg_pjs.py: v3 com compensação opcional) e testes.
- `experimentos/` matriz de simulações, indicadores, Random Forest, Morris, danos.
- `calibracao/` calibração bayesiana da compensação contra Bertulio et al. (2008).
- `biomas/` solo (SoilGrids + PTF-ZARC) e bioma (IBGE 2024) dos locais novos.
- `clima/power_api/` séries diárias NASA POWER.
- `tcc_docx/` texto (conteudo.js) e gerador do .docx (gerar.js).
- `auditoria_final/` auditoria dos números citados.
- `plataforma/` simulador web Akademia Florestal.
- `memoria/` banco de memória do projeto (padrão "memory bank").

---
# Projeto (estável)
- Autor: Bernardo Teixeira de Castro (UFU, Eng. Florestal). Orientador: Álvaro Augusto Vieira Soares. Coorientadora: Dra. Gabriela Cristina Costa Silva (UFRB). Banca: não definida (deixar em branco). Defesa: dezembro/2026.
- IC (frase do autor): a iniciação científica, ainda em andamento, foi a base; a partir dela auditamos, aprimoramos e corrigimos; a etapa atual é a calibração.
- Objetivo: estender o 3-PG com desfolha (e outros danos), simular intensidade, frequência e época em vários climas e solos, e quantificar o que pode e o que não pode ser afirmado sobre a validade biológica.
- Drive: pasta 3-PG https://drive.google.com/drive/folders/1GLR5Krx8FoJWjV9NM0OprTmUyA9JQP1L (o link vai no Apêndice B).
- Plataforma: https://claude.ai/artifact/UCFSe9dyzhXKkkNRpibFAc
- O autor trabalha pelo celular.

---
# Contexto ativo
- Feito (31/10 noite): Missão 07 — auditoria científica e cienciométrica; TCC revisado (53 p.); relatórios em revisao_07/.
- Próximo: OpenAlex (após 00h UTC) → atualizar a cienciometria; o autor lê o TCC revisado e envia aos orientadores com as 5 ressalvas do parecer.
- Arquivos grandes (PDFs, docx, mensal.csv.gz, zips) não vão para o GitHub: ficam no Drive.
- Drive (31/10, fim da noite): relatórios da Missão 07 em Docs na pasta 11; Diário recriado com a entrada da Missão 07; passagem atualizada. Autor arrasta TCC rev07 (pasta 08) e zip (pasta 11).
- Feito (31/10, 20h): plataforma v8 (artifact versão 8). Motor JS com compensação v3, perda de eficiência e mortalidade, conferido contra o Python em 7 cenários (dif. rel. máx 1,4e-14; plataforma/verificacao/comparar.py). Corrigido: volume registrado antes da mortalidade (como no r3PG). 6 locais por bioma; fisiologia original × calibrada; faixa de 90% com 200 amostras do posterior; catálogo de agentes; perda por produto; quadro de domínio de validade; prancha 'Precedentes' (3PG.d, CABALA). TCC rev08 (53 p.): 3.14, 4.12 e conclusão atualizados; auditoria 367/367.
- Feito (31/10, 21h): 'tudo no TCC' — TCC rev09 (55 p., 10 figuras, 14 tabelas): 3.14 descreve a biblioteca de 52 conceitos, modo explicar, cubagem (Smalian/Huber/Newton), taper e sortimentos; 4.12 traz a perda por produto (serraria −33,6%, celulose +5,9%, energia +36,8%) e a figura v8; Apêndice A com tutorial de 13 passos e figura das toras; Apêndice B com controle de versões, roteiro automatizado, auditorias numérica e científica, verificacao/, revisao_07/, ferramentas/. Auditoria 379/379. Pendente: perguntar ao autor sobre declaração de uso de IA.
- Feito (31/10, 21h30): espaço de possibilidades (experimentos/possibilidades.py, 7.584 cenários; 5.688 aptos) e validação cruzada da calibração (calibracao/validacao_cruzada.py: LOO k=5 RQEM 15,1→4,2 p.p.; k=2 C5→A1 19,1→6,4; A1→C5 11,7→4,3). RF k-fold 10×3 R² 0,991; LOSO 0,912; classificador ganho×perda 98,3% (bal. 93,7%). Ganho sobre o controle em 1,9% (orig.) e 3,1% (calib.) dos cenários, quase sempre com 25% de desfolha. TCC rev10: 3.15, 4.13 (Tabelas 12–13), Limitações → 4.14; 59 p.; auditoria 461/461.
- Feito (31/10, 22h): declaração de uso de IA (3.16) e referência ANTHROPIC (2026); TCC rev11, 60 p.; auditoria 461/461.

- Feito (01/11, madrugada): TCC enxugado de 60 para 40 páginas (rev12). Corpo 12.924 → 4.362 palavras; métodos 3.1–3.8, resultados 4.1–4.7; resumo 244 palavras; conclusão 6 parágrafos; plataforma detalhada no Apêndice A; Apêndice D novo (efeito do solo, recuperação × água, Morris). Corrigida a Tabela de verificação (308 controles, 28.277 registros; antes 260/23.873). Tabela 1 com os seis locais. Auditoria 489/489. Versão de 60 p. guardada (conteudo_v11_60p_antes_enxugar.js; entregas/rev11).
- Feito (01/11, 3h): regra do autor — 'tudo que chama atenção fica no TCC (gráficos); tudo que ocupa espaço mental vai para a Akademia'. TCC rev13 (34 p.): linguagem acessível; 12 figuras (3 novas: N1 calibração/validação cruzada, N2 biomas, N3 possibilidades); 1 tabela no corpo (locais); 7 quadros 'Na Akademia' com QR code (plataforma/qr, decodificado e conferido); apêndices A (reprodutibilidade) e B (busca). Akademia v9: 'Material do TCC' com 16 tabelas completas extraídas de gerar.js (extrair_material_tcc.js + material_tcc.py). Auditoria 489/489.
- Feito (02/11): acabamento e VERSÃO FINAL para o Álvaro (34 p.). Título atualizado para 'NOS BIOMAS BRASILEIROS'; referências conferidas nos dois sentidos (5 citações restauradas, incl. SILVA 2021; Souza et al. 2016 e Soares et al. 2003 incluídas, DOIs via Crossref); siglas e símbolos refeitos; lista de ilustrações corrigida (et al.); Apêndice A → B corrigido. Auditoria 489/489; 57 testes.
- Feito (02/11, tarde): ressalvas do parecer resolvidas, sobra 1. (5) γ calibrado com Quentin et al. (2011): γ = 1 (calibracao/calibrar_gamma.py); erro corrigido: calibrar.py ajustava U e a com γ = 0, e as simulações usavam 0,5. Recalibrado com γ = 1: U 1,22 (1,03–1,34), a 0,475; teste urocam 20,3→7,4 p.p.; LOO 15,1→4,1; k=2 19,1→7,2 e 11,7→4,9. Tudo refeito (biomas, possibilidades, RF, Morris). (3) busca complementada no Semantic Scholar (revisao_07/busca/semantic_busca.py: 469 no núcleo combinado; nenhum experimento brasileiro novo). (4) leituras: Battaglia 2011 (fonte primária do CABALA), Turnbull 2007; Collett e Neumann 2002 inacessível. (1) teste independente com Oliveira et al. (2014), Mucuri-BA (calibracao/teste_oliveira2014.py): desfolha total aos 6 meses, perda de volume 8 meses depois 35,4% observada; calibrado 29,2% (26,4–33,5), original 38,7%; parciais ≤1,5%, como no campo (n.s.). (2) Matrangolo vira a única ressalva: o módulo acerta a perda de curto prazo, mas não a persistência por anos (sem reservas nem morte de ramos; o CABALA falha igual, Battaglia 2011).
- TCC VERSÃO FINAL v2 (02/11, 35 p.): entregas/TCC_II_Bernardo_Castro_VERSAO_FINAL_v2_02-11-2026. Auditoria 506/506; 49 testes; referências 0 sem citação. Akademia reconstruída (Material do TCC e domínio de validade com Oliveira).
- Atenção: converter o PDF com --outdir (o PDF em tcc_docx/ fica bloqueado) e rodar `node gerar.js paginas.json` para o sumário ter páginas.


- Feito (02/11, ~12h30): cascata "sem falhas escondidas" → TCC VERSÃO FINAL v3 (37 p.). Dossel de Borges corrigido (γF e pFS2 da TECHS; IAF 2,4–5,6); U só no mês do ataque (u_meses = 1). Recalibração: U 1,18 (não identificado em desfolha total, vem da literatura), a 0,625, γ = 1 (razão 1,000). Urocam 20,3→7,5 p.p.; LOO 15,7→4,3; Oliveira (independente): original 77,6%, calibrado 33,0% (28,1–45,8) contra 35,4% medido (erro 34,3→3,2 p.p.). Matrangolo segue fora (4–32% contra 38–80%). Recuperação da copa calibrada ≤ 2 meses, perto das 12 semanas de Eyles et al. (2016). Ganho sobre o controle: original 1 caso (0,1%); calibrado 1,3% (máx 5,2%). Biomas: nenhum ganho na faixa de 90%; no Pampa a reação aumenta a perda anual (5,9→8,3%). Morris nos biomas: k no topo em 5 locais. Defeitos achados e corrigidos: matriz principal lia os 6 locais; controles sem script; tabelas digitadas à mão (agora tcc_docx/tabelas_dados.py); plataforma com tabelas digitadas (atualizadas). Auditoria 528/528; conferidor texto×auditoria ok; 49 testes; JS = Python em 8 cenários.
- Feito (02/11, 16h): VERSÃO FINAL v4 (37 p.) com 5.1 Perspectivas na conclusão (persistência, validação, clones atuais, RESILIA/clima futuro, ensino). PASSAGEM_ASTRA.md escrita (passagem para o Astra). Auditoria 528/528; 49 testes; referências ok.

---
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

---
## Calibração (lido de calibracao/saida/calibracao_d0999.json)
- U: mediana 1.18 (IC90% 1.01–1.34); a: mediana 0.625 (IC90% 0.225–0.975).
- Ajuste C5 — observado: CAP 24.2, altura 19.1, volume 52.9 | original: volume 66.6, CAP 29.7, altura 36.1 | calibrado: volume 50.9, CAP 20.5, altura 25.2.
- Teste A1/urocam (mesmo experimento; não é validação independente) — observado: volume 59.0, CAP 22.9 | original: volume 79.3, CAP 40.7 | calibrado: volume 66.5, CAP 30.6 (IC90% volume 59.6, CAP 25.9 a volume 76.9, CAP 38.4).

---
# Registro de decisões (mais recente no fim)
- 30/10: ampliar de Indianópolis para 3 locais; solo local do TECHS onde houver; FR em níveis ordinais.
- 31/10: incluir outros danos (eficiência, mortalidade) com fontes.
- 31/10: plataforma acessível a não especialistas (conceitos, modo explicar, cubagem, taper com Souza et al., 2016).
- 31/10: fazer calibração de verdade ("trabalhoso, defendo fácil"): compensação v3 calibrada contra Bertulio et al. (2008), urograndis (C5); teste com urocam (A1).
- 31/10: um local por bioma onde há eucalipto: Almeirim-PA (Amazônia), Araripina-PE (Caatinga), Eldorado do Sul-RS (Pampa); Pantanal excluído (sem plantio comercial; 3-PG não representa alagamento). Imperatriz é Cerrado (IBGE 2024).
- 31/10: mecanizar o ambiente: AGENTS.md, banco de memória, pipeline único e passagem de bastão gerada automaticamente; GitHub como fonte da verdade quando a conta for conectada.
- 31/10: Missão 07 — auditoria integrada. Parecer B. Recomendação aos orientadores: discutir γ (literatura indica ≈ 1) e o domínio de uso (sem desfolha total no 1º ano).
- 31/10: diferenciar a plataforma do 3PG.d (Rua et al., 2020) sem alegar pioneirismo: incerteza propagada, compensação calibrada, outros danos, perda por produto e domínio de validade explícito. A comparação usa só a descrição pública do 3PG.d.
- 31/10: comprovar com validação cruzada: LOO (k=5) e por clone (k=2) na calibração (dado real, mesmo experimento) e k-fold do metamodelo no espaço de possibilidades (mede regularidade do modelo, não acerto em campo).
- 01/11: o autor pediu um TCC realista: corpo enxuto (~19 p.), detalhes nos apêndices e no pacote; nenhum resultado removido do trabalho, só do corpo.
- 01/11: TCC para qualquer leitor entender; gráficos no TCC, tabelas densas replicadas no 'Material do TCC' da Akademia; quadros com QR code levam à plataforma. Sem apêndice de plataforma nem de resultados complementares.
- 02/11: γ deixa de ser escolha (0,5) e passa a ser calibrado com experimento independente (Quentin et al., 2011): γ = 1; U e a recalibrados com γ fixo. Oliveira et al. (2014) usado só como teste independente, nunca no ajuste. Krause 2025 e Kautz 2018 fora da tabela de precedentes (conteúdo não conferido).
- 02/11 (tarde): cascata "sem falhas escondidas". (1) Dossel dos clones de Borges corrigido: γF1, γF0 e pFS2 trocados pelos da TECHS (Caldeira et al., 2020a), porque os de Borges davam IAF 8–11 contra 3,0–3,8 medidos; TCC_DOSSEL=borges reproduz a versão anterior. (2) U só no mês do ataque (u_meses = 1; Turnbull et al., 2007; Quentin et al., 2012): as regras testadas deram ajuste equivalente, escolhida a sustentada pela fisiologia; em desfolha total o U não é identificado e vem da faixa da literatura. (3) Matriz principal fixada nos 3 locais (SITIOS_MATRIZ), pois passara a ler os 6 locais. (4) Tabelas completas geradas dos resultados (tcc_docx/tabelas_dados.py), sem números digitados. (5) controles_solo_local.csv ganhou script (experimentos/controles.py). (6) Pipeline com todas as etapas (calibração completa, biomas, possibilidades, tabelas, plataforma).

---
# Contexto técnico
- Python 3.11+ (numpy, pandas, scikit-learn, SALib opcional); Node 18+ com `docx` para gerar o TCC; LibreOffice para PDF.
- Modelo: `modelo/threepg_pjs.py`, `run_3pg_pjs(site, species, climate, params, defoliation_events=, efficiency_events=, mortality_events=, compensation=)`.
  - v1/v2: desfolha W_F·(1−d) no início do mês; perda de eficiência α·(1−r); mortalidade N·(1−m).
  - v3 (compensação, opcional): enquanto W_F < W_F,ref: U_ef = 1+(U−1)·f_SW sobre α; condutância ×(gC_ref/gC)^γ (teto 1/(1−0,45)); partição η_F' = η_F + a·déficit·(η_S+η_R).
- Convenção temporal: plantio 2015-01; A1 começa aos 12 meses (2016-01), materiais de Borges aos 3 (2015-04); fim 2023-01; "k" = mês da simulação de referência; rotação = k72 (84 meses de idade).
- Materiais: A1 (Caldeira et al., 2020); C5, C2, C4 (Borges, 2009). A1 em Imperatriz, Almeirim e Araripina = diagnóstico (f_T = 0 em vários meses).
- Locais: IND, TB, IMP (originais); ALM (Amazônia), ARA (Caatinga), ELD (Pampa). Bioma: IBGE 2024 (`biomas/bioma2024.csv`).

---
## Últimos commits
- 02/11 12:08 Cascata: dossel de Borges corrigido (TECHS), U só no mês do ataque, recalibração e reprocessamento completo; tabelas geradas dos resultados; pipeline completo; plataforma e capturas atualizadas; TCC VERSÃO FINAL v3 (37 p.), auditoria 528/528
- 02/11 12:02 pipeline: etapa plataforma concluída
- 02/11 12:02 pipeline: etapa tabelas concluída
- 02/11 11:42 pipeline: etapa danos concluída
- 02/11 11:42 pipeline: etapa analises concluída
- 02/11 11:31 pipeline: etapa indicadores concluída
- 02/11 11:31 pipeline: etapa experimentos concluída
- 02/11 11:19 Conferidor: números decimais do texto do TCC × itens da auditoria
- 02/11 11:15 Recalibração com γ = 1 (Quentin 2011), teste independente com Oliveira et al. (2014), busca no Semantic Scholar; TCC VERSÃO FINAL v2 (35 p.), auditoria 506/506
- 02/11 11:14 pipeline: etapa verificar concluída
- 02/11 10:43 Versão final do TCC (02/11): título, referências conferidas e completadas, siglas e símbolos, lista de ilustrações; auditoria 489/489
- 01/11 07:16 Akademia no GitHub Pages: docs/index.html gerado pelo construir.py
- 01/11 02:53 TCC rev13 acessível (34 p.): gráficos no texto, tabelas densas no 'Material do TCC' da Akademia, quadros com QR code; 3 gráficos novos; plataforma v9; auditoria 489/489
- 01/11 02:14 TCC rev12: enxugado de 60 para 40 páginas (corpo 4.362 palavras), apêndices A e D; Tabela 1 com seis locais; tabela de verificação corrigida (308/28.277); auditoria 489/489
- 31/10 21:05 TCC rev11: declaração de uso de inteligência artificial (3.16) e referência ANTHROPIC (2026)

## Para a IA que continuar
1. Sem execução de código: redija o texto, marcando [CONFERIR] em números ainda não gerados. Nunca invente resultados.
2. Com código: siga "Falta (em ordem)" e rode `python3 ferramentas/pipeline.py <etapa>`.
3. Ao fim de cada passo: atualize `memoria/`, rode este gerador e faça commit.


---
# ADENDO DE PASSAGEM DE BASTÃO — 14/11/2026

> **Nota de atualização:** o corpo histórico acima foi gerado em 02/11 e contém contexto antigo. Este adendo registra as mudanças verificadas em 14/11/2026. A regeneração integral pelo script oficial ainda está pendente de checkout completo; não tratar a contagem antiga de tokens como atual.

## Estado mais recente do trabalho
- Repositório: fork privado `tomdeatj-commits/Akademia`. A branch de documentação é `docs/mapa-mestre-tcc-akademia`.
- Mapa mestre: `planejamento/MAPA_MESTRE_TCC_AKADEMIA.md`, commit `4fd2d13331aa2b4cd5636eab321066db0e10093b`.
- PR #4 aberto, ainda não mesclado: https://github.com/tomdeatj-commits/Akademia/pull/4.
- Nesta atualização, o mapa foi registrado como planejamento. Não houve execução de código, nova simulação, calibração, alteração do motor, mudança de parâmetros ou geração de resultados científicos.

## Escopo consolidado
O estudo aprovado contempla 2 genótipos × 2 classes texturais de solo × 3 condições climáticas (histórico, SSP2-4.5 e SSP5-8.5), em sete anos. A região publicamente documentada de atuação da LD Celulose é referência territorial. **Não presumir dados, parcelas, inventários, clones, análises de solo, dados meteorológicos ou autorização da empresa.** Se dados forem obtidos posteriormente, registrar origem, autorização, metadados e compatibilidade.

Pragas/desfolha são inicialmente análises de sensibilidade separadas do fatorial central. Fenotipagem com GEDI, Sentinel-2 e Earth Engine deve respeitar qualidade, footprint/pixel, datas e incertezas. Essas fontes não identificam por si só clone, ocorrência de praga, IAF ou produtividade de talhão.

## Arquitetura e frentes
O mapa organiza 12 pacotes:
- P0 governança e rastreabilidade;
- P1 auditoria do módulo de desfolha;
- P2 literatura Stape/Hélio e seleção de genótipos;
- P3 território e solos;
- P4 clima histórico/futuro;
- P5 fatorial genótipo×solo×clima;
- P6 pragas e danos;
- P7 GEDI/Earth Engine/fenotipagem;
- P8 alometria, DAP, altura, volume e produtos;
- P9 avaliação e validação;
- P10 plataforma Akademia;
- P11 redação e defesa.

## Próximas ações obrigatórias
1. Revisar o PR #4 e mesclar somente após aprovação do autor.
2. Obter checkout completo do repositório e executar `python3 ferramentas/pipeline.py verificar`.
3. Executar `python3 ferramentas/gerar_passagem.py` para regenerar `PASSAGEM_DE_BASTAO.md` e `CONTEXTO_EMPACOTADO.md`; conferir diferenças e registrar commit. O gerador foi lido nesta etapa, mas não executado.
4. Retomar auditoria do módulo original e matriz observado×previsto, sem confundir calibração/teste interno com validação independente.
5. Atualizar revisão bibliográfica com trabalhos recentes de Stape e Hélio Garcia Leite; documentar fontes primárias, parâmetros, domínio e incertezas.
6. Selecionar genótipos contrastantes somente com evidência experimental e parâmetros compatíveis disponíveis.
7. Obter e auditar entradas públicas de solo/água e clima; depois congelar protocolo e executar os 12 cenários.
8. Integrar danos, fenotipagem e alometria em módulos separados, com critérios de aceite e observações independentes adequadas.

## Regras de interpretação
- TESTED significa teste técnico, não validação biológica.
- Fixtures sintéticas demonstram funcionamento do software, não produtividade real.
- GEDI/Sentinel são observações/proxies com limitações espaciais e temporais.
- Cenários de pragas sem série local são hipóteses simuladas, não mapas de infestação.
- Não alegar novidade, superioridade genética ou capacidade preditiva sem comparação apropriada e evidência independente.
- Preservar o motor e a reprodutibilidade do módulo legado; toda alteração científica exige fonte, teste e auditoria.

## Referências internas essenciais
- `AGENTS.md` — regras obrigatórias para agentes.
- `memoria/contexto_ativo.md` — contexto atual.
- `memoria/progresso.md` — feito, pendências e bloqueios.
- `planejamento/MAPA_MESTRE_TCC_AKADEMIA.md` — plano completo P0–P11.
- `experimentos/integrado/README.md` — experimento genótipo×solo×clima.
- `docs/ESCOPO_TCC_LD_REGIONAL.md` — delimitação territorial e de dados.
- `docs/AUDITORIA_03_RASTREABILIDADE.md` — auditoria de evidências.

