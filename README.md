# Akademia

Repositório privado do TCC II de Bernardo Teixeira de Castro (Engenharia Florestal, UFU): **módulo de desfolha
(pragas e doenças) no modelo ecofisiológico 3-PG para eucalipto**, com calibração bayesiana da compensação
fisiológica, seis localidades de cinco biomas brasileiros (duas no Cerrado) e a plataforma web **Akademia Florestal**.

- Regras do projeto e mapa de pastas: [`AGENTS.md`](AGENTS.md) (vale para qualquer IA).
- Estado atual: [`memoria/contexto_ativo.md`](memoria/contexto_ativo.md) e [`memoria/progresso.md`](memoria/progresso.md).
- Passagem de bastão: [`PASSAGEM_DE_BASTAO.md`](PASSAGEM_DE_BASTAO.md) (gerada por `python3 ferramentas/gerar_passagem.py`).
- Rodar tudo: `python3 ferramentas/pipeline.py tudo` (ou uma etapa: `testes`, `calibracao`, `experimentos`, …).

Só dados secundários. PDFs de artigos e arquivos grandes ficam no Google Drive (pasta 3-PG), não aqui.

## Auditoria e segurança de execução

- Conferir entradas/saídas observadas: `python3 ferramentas/pipeline.py evidencias`.
- Conferir pré-requisitos: `python3 ferramentas/pipeline.py verificar`.
- Por padrão, o pipeline **não publica no GitHub**; para publicar explicitamente, use `--publish`
  somente em uma branch de trabalho. O envio para `main` ou `master` é bloqueado.
- Relatório e limites: [Auditoria 03](docs/AUDITORIA_03_RASTREABILIDADE.md).
- Distinga sempre verificação de código, calibração, confronto externo pontual e validação biológica.

## Novo módulo operacional — genótipo × solo × clima + pragas + fenotipagem

- [Experimento integrado: execução e entradas científicas](experimentos/integrado/README.md)
- [Bancada web para configurar e analisar resultados](plataforma/integrado.html)
- [Extrator Earth Engine (GEDI L2A, L2B, L4A; Sentinel-2)](sensoriamento/earthengine/extrair_gedi_sent2_talhoes.js)
- [Importador GEDI e Sentinel-2](sensoriamento/importar_gee.py)

O núcleo aprovado tem 12 cenários (2 genótipos × 2 solos × histórico/SSP2-4.5/SSP5-8.5);
dano/desfolha são simulações de sensibilidade opcionais, nunca evidência de ocorrência de praga.
A análise produz o contraste triplo genótipo × solo × clima e sua modulação por ataques,
com rastreabilidade. **Não há parâmetros, clima futuro nem fenotipagem reais da LD Celulose
presumidos na demonstração.**

## Recorte territorial da proposta aprovada
O estudo genótipo × solo × clima usa a **região publicamente documentada de atuação da LD Celulose**, sem presumir talhões, clones, análises de solo ou inventários da empresa. Ver [protocolo territorial e de dados secundários](docs/ESCOPO_TCC_LD_REGIONAL.md). A fenotipagem regional sem identificação genética é tratada como contexto, não validação.


## Planejamento e auditoria do projeto

- [Mapa mestre do TCC II e da Akademia](docs/PLANO_MESTRE_TCC_AKADEMIA.md) — objetivos, frentes, sequência crítica, dependências e critérios de conclusão.
- [Matriz de auditoria](docs/MATRIZ_AUDITORIA.md) — evidência exigida por frente, bloqueios conhecidos, estados e modelo de registro.
