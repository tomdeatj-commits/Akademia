# Auditoria 03 — Integridade científica e integração segura (14/11/2026)

## Objetivo
Ampliar a rastreabilidade sem substituir o núcleo 3-PG nem modificar parâmetros biológicos.
Esta etapa opera no fork `tomdeatj-commits/Akademia`, branch
`audit/rastreabilidade-integracao-2026-11`, e **não** modifica `main`.

## Constatações verificadas no repositório
- O histórico do fork e sua passagem de bastão ainda refletem em grande parte a versão de 02/11/2026;
  existe no Drive uma redação integral v8, de 04/11/2026. Não há sincronização automática entre elas.
- `ferramentas/pipeline.py` anteriormente realizava `git push origin HEAD:main` em etapas aprovadas;
  o novo comportamento é **sem publicação por padrão** e impede explicitamente publicação em main/master.
- `revisao/dados_tratamentos_observados_verificado.csv`: 24 registros (12 Bertulio, 12 Matrangolo).
  Os percentuais registrados e os ajustes de linha de base conferem aritmeticamente
  com os pares controle/tratamento disponíveis no próprio arquivo.
- `calibracao/saida/teste_oliveira2014.json`: para T1, volume publicado 35,4% e previsto
  (mediana do conjunto histórico) 33,0%: desvio de **−2,4 pontos percentuais**.
- `revisao/extrair_pares_observados.py` e o CSV passaram a classificar Bertulio corretamente:
  os dados usados na calibração e no teste do mesmo experimento **não** são validação externa independente.
- A série Matrangolo (2010) continua sendo confronto externo de longo prazo, com
  discrepância de persistência relevante. Nenhuma reparametrização foi feita nesta etapa.

## Arquivos novos e alterados
- `ferramentas/auditar_evidencias.py`: conferência matemática com relatório JSON opcional;
  reconhece classificação e limites de cada estudo.
- `ferramentas/test_auditar_evidencias.py`: testes de aritmética, erro Oliveira e proteção de branches.
- `ferramentas/pipeline.py`: etapa `evidencias`; publicação somente com opt-in `--publish`,
  recusando a branch `main`.
- `revisao/extrair_pares_observados.py` e
  `revisao/dados_tratamentos_observados_verificado.csv`: correção **editorial** da classificação
  de Bertulio, sem alterar entradas quantitativas.

## Execução
```bash
python3 ferramentas/pipeline.py verificar
python3 ferramentas/pipeline.py evidencias
python3 ferramentas/auditar_evidencias.py --output auditoria_final/relatorio_evidencias.json

# Opcional, com checkout da branch de auditoria e revisão do git status:
python3 ferramentas/pipeline.py --publish evidencias
```

O `--publish` não é necessário para testar; ao publicá-lo em checkout local, ele usa
a branch atual e não permite enviar para `main` ou `master`.

## Critérios e limites
- **Verificação matemática do CSV/JSON não é validação biológica**.
- A fonte primária de Bertulio precisa seguir sob conferência de transcrição e protocolo.
- Oliveira é um confronto externo pontual (curto prazo), não validação em múltiplos sítios.
- Matrangolo expõe discrepância de longo prazo; não omitir em resumo e discussão.
- Campo experimental com 100% de desfolha não equivale sem ressalva a 95% no simulador.
- Ainda faltam o recálculo completo da calibração, a comparação r3PG×Python×JavaScript e
  a harmonização entre o TCC v8 e a versão do repositório.
- O gerador `ferramentas/gerar_passagem.py` deve ser executado no checkout completo após
  a reconciliação da memória; não declarar atualização da passagem antes disso.

**Situação desta etapa:** inspeção da origem e checagem aritmética dos registros existentes,
proteção do pipeline e testes unitários; sem afirmação de validação ampla.
