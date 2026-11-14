# Matriz de auditoria e critérios de aceite

Este arquivo operacionaliza o [Mapa mestre](PLANO_MESTRE_TCC_AKADEMIA.md). Não marque uma etapa como concluída apenas porque há código ou testes unitários.

| Frente | Unidade de auditoria | Evidência mínima | Bloqueio atual conhecido |
|---|---|---|---|
| F0 Governança | Branch, commit, execução | SHA, status CI, manifesto, memória atualizada | Passagem de bastão de 02/11; memória antiga |
| F1 TCC desfolha | Cada estudo/variável/idade | fonte primária, tabela transcrita, comando, resultado reproduzido | conferir artigos, recalibração, R/Python/JS |
| F1 Matriz observado × previsto | Cada par comparável | observação independente, previsão, unidade, idade, erro e incerteza | evidências existentes ainda são pontuais e heterogêneas |
| F2 Genótipos | Cada conjunto paramétrico | 82 parâmetros rastreáveis + evidência experimental de tolerância | A1/C5 não demonstram contraste de tolerância |
| F2 Solo | Cada classe/perfil | textura por camada, profundidade, CAD, fonte e PTF | CADs nulas na configuração |
| F2 Clima histórico | Célula e período | série mensal observacional, cobertura e checksum | coordenada e CSV reais pendentes |
| F2 CLIMBra | GCM × SSP × período | arquivo original, GCM, grade, período, versão, transformação validada | CSV real e hipótese de radiação líquida/incidente |
| F2 Execução | 12 cenários centrais | outputs mensais/finais, manifesto e confronto r3PG R | porta Python é a usada; R ainda pendente |
| F3 Danos | Agente × mecanismo × evento | fonte, hospedeiro, intensidade, tempo, classificação hipótese/literatura | cenários reais ainda não cadastrados |
| F4 GEDI | produto × footprint × período | QA, n válido, unidade, incerteza, geometria | asset/polígonos e exportações ainda dependentes de configuração |
| F4 Sentinel-2 | talhão × mês | máscara, cenas, composição, índices e QA | exportação real não confirmada |
| F5 Solo/hidrologia | perfil e camada | parâmetros físicos e incerteza | fontes/perfis regionais a selecionar |
| F6 Literatura | parâmetro × artigo × material | DOI/URL, página/tabela, valor/unidade, espécie/clone, domínio | revisão cronológica precisa ser executada |
| F7 Alometria | equação × compartimento | modelo, coeficientes, domínio, amostra e erro | harmonização com materiais do experimento |
| F8 IA/estatística | estimando e validação | baseline, separação de dados, métricas, incerteza e vazamento auditado | definir quais perguntas exigem ML |
| F9 Plataforma | fluxo de ponta a ponta | teste funcional com entradas reais, exportação e manifesto | interface prepara/configura; execução local ainda exige scripts |
| F10 TCC/defesa | afirmação × resultado | número regenerável, figura/tabela, citação, revisão | TCC v8 e v09 precisam reconciliação editorial |

## Regra de status

- **Não iniciado:** não há artefato executável ou evidência.
- **Em desenvolvimento:** há código/documento, mas faltam critérios de aceite.
- **Pronto para teste:** inputs, instruções e testes existem.
- **Testado tecnicamente:** testes de software passaram; não implica validade ecológica.
- **Confrontado externamente:** comparação com fonte/estudo independente específico, com limites explícitos.
- **Validado no domínio:** critérios de validação independente pré-definidos e atingidos.
- **Bloqueado por dado:** ferramenta pronta, mas a fonte de entrada não está disponível ou não é adequada.

## Registro obrigatório de cada conclusão

```yaml
id: F2.11
status: testado_tecnicamente
data: YYYY-MM-DD
responsavel: Bernardo
commit: SHA
comando: "comando reproduzível"
entradas:
  - caminho_ou_url
  - sha256
saidas:
  - caminho_ou_url
criterio_aceite: "critério mensurável"
resultado: "observado, sem extrapolação"
limitacoes:
  - "limitação ainda presente"
proximo_passo: "ação única"
```

## Questões abertas que exigem decisão metodológica

1. Seleção de dois genótipos: parâmetros completos e contraste publicado devem coexistir; não basta estudo fisiológico sem parametrização utilizável ou parâmetros sem evidência de tolerância.
2. CLIMBra: método para transformar radiação líquida em radiação incidente precisa de justificação e análise de sensibilidade; não reutilizar fator sem validação.
3. Ciclo de sete anos: GEDI começa em 2019; a cobertura não representa automaticamente todo o ciclo histórico de 2015–2022.
4. Solo: duas classes texturais precisam de CAD e profundidade efetiva, não apenas a classe SoilClass do modelo.
5. Escopo TCC: resultados de desfolha já produzidos são o núcleo atual; fatorial 2×2×3 é extensão aprovada que só entra como resultado após execução científica.
6. Campo/LD: qualquer dado empresarial depende de entrega, autorização e metadados documentados. Até lá, a referência é territorial e pública.
