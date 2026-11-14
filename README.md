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
