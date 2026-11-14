# Mapa mestre — TCC II e Akademia Florestal
**Versão:** 1.0  
**Data:** 14/11/2026  
**Responsável científico:** Bernardo Teixeira de Castro  
**Instituição:** Engenharia Florestal — UFU  
**Orientação:** Álvaro Augusto Vieira Soares  
**Coorientação:** Gabriela Cristina Costa Silva

> Documento de planejamento e auditoria. Não representa resultados concluídos, validação biológica, parceria de fornecimento de dados ou disponibilidade de infraestrutura.

## 1. Propósito e regra de escopo

Organizar o TCC II e a evolução da Akademia em uma arquitetura coerente, integrando o módulo de desfolha no 3-PG com o experimento complementar genótipo × solo × clima, danos bióticos, fenotipagem e dados geoespaciais.

**Recorte territorial:** região publicamente documentada de atuação da LD Celulose, no Triângulo Mineiro. A empresa é referência territorial, não fornecedora presumida. Não presumir acesso a talhões, inventários, clones, parâmetros internos, análises de solo ou estações meteorológicas. Dados eventualmente recebidos no futuro serão adicionados somente após identificação de origem, autorização, metadados e avaliação de compatibilidade.

**Regra central:** distinguir sempre:
- verificação computacional: código executa corretamente e reproduz equações/referências;
- calibração: parâmetros ajustados a um conjunto de dados;
- avaliação interna ou teste no mesmo experimento: desempenho sem independência;
- confronto externo pontual: comparação com estudo independente, mas possivelmente limitado;
- validação externa: avaliação com dados independentes e representativos do domínio de uso;
- cenário exploratório: simulação condicional, não observação nem previsão validada.

## 2. Pergunta integradora

Como a disponibilidade hídrica e térmica, a textura e a profundidade do solo, as características genéticas e os danos por pragas modulam o crescimento, a alocação de carbono, a área foliar e a produção de madeira de eucalipto ao longo de uma rotação, e até que ponto um modelo 3-PG ampliado consegue representar essas respostas quando confrontado com evidências independentes?

## 3. Objetivos

### Objetivo geral
Desenvolver e avaliar uma estrutura reproduzível de simulação e apoio à decisão para analisar a interação entre genótipo, solo, clima e danos bióticos em plantios de eucalipto, combinando o 3-PG com dados ambientais, observações remotas e métodos de análise florestal.

### Objetivos específicos
1. Preservar e documentar o módulo de desfolha e compensação fisiológica do TCC II, explicitando seu domínio de validade e limitações.
2. Revisar e selecionar parâmetros fisiológicos/alométricos e materiais genéticos contrastantes com suporte em fontes primárias recentes.
3. Preparar um experimento fatorial de 12 combinações: 2 genótipos × 2 classes texturais × 3 condições climáticas (histórico, SSP2-4.5, SSP5-8.5).
4. Quantificar biomassa lenhosa, volume, biomassa foliar, IAF/LAI, sobrevivência e variáveis intermediárias disponíveis no modelo durante sete anos.
5. Quantificar contrastes relativos entre genótipos, solos e cenários, incluindo a interação tripla.
6. Acrescentar cenários de danos por pragas como análises de sensibilidade claramente separados da ocorrência observada de pragas.
7. Construir uma camada de fenotipagem e caracterização estrutural usando fontes como GEDI e Sentinel-2, respeitando resolução, temporalidade e variável efetivamente observada.
8. Confrontar saídas com medições independentes disponíveis na literatura ou em bases abertas; não chamar sensoriamento remoto regional de validação de clone.
9. Comparar implementações e resultados com r3PG em R e/ou referências de implementação, registrando tolerâncias e divergências.
10. Entregar uma plataforma didática, auditável e útil para preparar cenários, visualizar resultados e documentar incertezas.

## 4. Arquitetura integrada — a sequência causal

**Clima → solo/água → genótipo → estado fisiológico → dano biótico → recuperação → crescimento/alocação → estrutura e produtos → observação/fenotipagem → avaliação e decisão.**

A ordem é conceitual; processos podem atuar simultaneamente. Não assumir que a mera conexão de módulos prova causalidade biológica.

| Camada | Entradas | Processo/saída | Papel na Akademia |
|---|---|---|---|
| Clima | histórico e projeções por GCM/SSP, variáveis e período | temperatura, precipitação, radiação, VPD e extremos | forçante do modelo |
| Solo e água | textura, profundidade efetiva, CAD/ASW, atributos públicos | armazenamento e limitação hídrica | condicionante do sítio |
| Genótipo | parâmetros publicados com origem, unidade e domínio | respostas fisiológicas e alometria específicas | contraste genético documentado |
| 3-PG | clima, solo, parâmetros | APAR, PPB/PPL, partição, biomassa, IAF, volume | motor ecofisiológico |
| Danos | tipo, intensidade, frequência, época, duração | remoção foliar, perda de eficiência, mortalidade, recuperação conforme evidência | módulo de cenários de estresse |
| Fenotipagem | GEDI, Sentinel-2 e medições disponíveis | estrutura do dossel, altura/biomassa proxy, índices espectrais e anomalias | caracterização e monitoramento |
| Inventário/alometria | DAP, altura, densidade, equações | volume, biomassa, distribuição diamétrica e produtos | ponte para mensuração florestal |
| Avaliação | observações independentes e incertezas | viés, RMSE/RQEM, cobertura de intervalos, domínio de validade | auditoria científica |
| Interface | configuração, proveniência e resultados | cenários, gráficos, tabelas, exportações e relatórios | apoio à decisão/ensino |

## 5. Pacotes de trabalho e critérios de conclusão

Os estados abaixo são uma fotografia inicial baseada no conteúdo/documentação atualmente presente no repositório, e não uma certificação independente de execução científica.

### P0 — Governança científica, reprodutibilidade e rastreabilidade
**Estado inicial:** parcialmente documentado; precisa de harmonização entre README, memória, passagem de bastão e TCC.
- [ ] Atualizar contexto ativo, progresso, decisões e passagem de bastão após cada entrega.
- [ ] Criar inventário de dados com arquivo, variável, unidade, período, escala, origem, licença, transformação e hash.
- [ ] Criar registro de parâmetros com nome, símbolo, unidade, valor, fonte primária, página/tabela/equação, espécie/clone, método e incerteza.
- [ ] Registrar versão de R, r3PG, Python, dependências, JavaScript, GEE e scripts.
- [ ] Separar saída demonstrativa/sintética de saída científica real.
- [ ] Definir critérios de aceite para cada experimento e artefato.
**Aceite:** uma terceira pessoa consegue reconstruir cada número citado e identificar sua proveniência.

### P1 — Auditoria e fechamento do módulo original de desfolha
**Estado inicial:** código e documentação existentes; auditoria científica ainda exige reconciliação com documentos originais.
- [ ] Reexecutar pipeline completo em checkout limpo.
- [ ] Reconciliar cada parâmetro e equação com a fonte primária.
- [ ] Conferir o papel de Bertulio (calibração/teste no mesmo experimento) e separar dados independentes.
- [ ] Reexaminar confronto externo Oliveira et al. e discrepância de persistência apontada por Matrangolo.
- [ ] Testar época, intensidade, frequência, duração, recuperação e domínio de extrapolação.
- [ ] Quantificar incerteza dos parâmetros e propagá-la às saídas.
- [ ] Comparar Python, JavaScript e r3PG em cenários controlados.
- [ ] Manter comportamento legado quando compensação opcional estiver desativada.
**Aceite:** matriz observado × previsto com observação, previsão, erro, unidade, fonte, independência e limitação; nenhum dado de calibração rotulado como validação.

### P2 — Revisão de literatura e seleção dos genótipos
**Estado inicial:** referências-alvo identificadas; seleção final e extração de parâmetros pendentes.
- [ ] Fazer busca atualizada em Google Scholar, OpenAlex, Crossref, Semantic Scholar, Scopus/WoS se houver acesso, patentes e repositórios.
- [ ] Revisar Stape e colaboradores: fisiologia, fluxo e partição de carbono, resposta a seca/calor, água no solo e produtividade clonal.
- [ ] Revisar Hélio Garcia Leite e colaboradores: calibração 3-PG, redes neurais para parâmetros, classificação de sítios, alometria, altura, volume e prognose.
- [ ] Ler fontes primárias completas; registrar DOI, ano, população, desenho, variáveis, unidades e páginas.
- [ ] Identificar dois genótipos com contraste hídrico/térmico demonstrado experimentalmente.
- [ ] Verificar se parâmetros necessários ao 3-PG estão publicados para ambos; não criar parâmetros por extrapolação sem análise de identificabilidade.
- [ ] Documentar diferenças entre genótipo, clone, espécie e material experimental.
- [ ] Comparar parâmetros transferidos e locais; definir incertezas e análises de sensibilidade.
**Aceite:** ficha comparativa de genótipos baseada em fontes primárias e um dicionário parametrizado, completo ou explicitamente marcado como lacuna.

### P3 — Caracterização territorial e solos públicos
**Estado inicial:** protocolo regional documentado; ponto representativo e extrações finais pendentes.
- [ ] Definir um ponto/coordenada de referência reproduzível dentro do recorte territorial público; não alegar que representa talhão específico sem evidência.
- [ ] Descrever método de escolha do ponto e análise de representatividade.
- [ ] Extrair textura, frações granulométricas e atributos relevantes do SoilGrids, registrando profundidade, resolução e incerteza.
- [ ] Estimar capacidade de água disponível por método publicado/adequado, registrando PTF, equações e limitações.
- [ ] Definir classes arenosa e argilosa por critérios numéricos explícitos e amostras representativas da base.
- [ ] Incluir profundidade efetiva e água disponível como variáveis separadas quando a fonte permitir.
- [ ] Avaliar necessidade de topografia, lençol freático ou restrição física; só incluir com fonte confiável.
- [ ] Documentar que classe textural não substitui caracterização completa do perfil.
**Aceite:** tabela e mapas com valores, profundidade, resolução, incerteza, fonte e procedimento reproduzível.

### P4 — Clima histórico e cenários futuros
**Estado inicial:** parser/estrutura de integração mencionados no repositório; dados reais e configuração científica a confirmar.
- [ ] Selecionar conjunto CLIMBra e versões dos GCMs; documentar período histórico e janelas futuras.
- [ ] Confirmar convenção SSP2-4.5 e SSP5-8.5, unidades, calendário e resolução.
- [ ] Extrair variáveis necessárias ao 3-PG e conferir lacunas, calendário, agregação e consistência física.
- [ ] Definir método de perturbação: anomalias absolutas/relativas, período de referência, correção de viés e preservação de sazonalidade.
- [ ] Comparar histórico modelado e referência observada independente (por exemplo NASA POWER/INMET, quando apropriado).
- [ ] Avaliar múltiplos GCMs ou justificar seleção; evitar tratar um GCM como consenso.
- [ ] Construir cenários em escala mensal compatível com o modelo e preservar dados brutos.
- [ ] Quantificar dispersão entre GCMs e cenários.
**Aceite:** clima histórico e futuro em arquivos rastreáveis, scripts reexecutáveis, estatísticas de controle de qualidade e comparação histórica.

### P5 — Experimento fatorial genótipo × solo × clima
**Estado inicial:** bancada e desenho fatorial descritos; execução com parâmetros e entradas reais pendente.
- [ ] Congelar protocolo dos 12 tratamentos (2 × 2 × 3) e horizonte de sete anos.
- [ ] Definir condições iniciais, densidade, manejo, idade, local e unidade experimental simulada.
- [ ] Executar primeiro o r3PG de referência sem extensão de danos.
- [ ] Executar versões/parametrizações dos genótipos de forma rastreável.
- [ ] Executar combinações de solo arenoso/argiloso sem confundir classe com um valor arbitrário de água.
- [ ] Produzir séries mensais e resultados em idade/rotação comum.
- [ ] Calcular biomassa de madeira, volume, biomassa foliar, IAF e sobrevivência apenas quando a variável for representada pelo modelo ou por extensão documentada.
- [ ] Calcular contrastes absolutos e relativos contra histórico e entre genótipos.
- [ ] Estimar interação genótipo × solo × clima e intervalos de incerteza.
- [ ] Realizar sensibilidade e incerteza de parâmetros/forçantes.
**Aceite:** 12 cenários reproduzíveis, arquivos de entrada e saída, contraste triplo, intervalos/limitações e script de auditoria.

### P6 — Pragas, doenças e danos bióticos
**Estado inicial:** módulo de desfolha existente; integração com experimento aprovado ainda requer validação de premissas.
- [ ] Definir agentes e modos de dano a partir de fontes; separar desfolha, perda de eficiência, mortalidade e danos não foliares.
- [ ] Parametrizar época, duração, intensidade, frequência e distribuição dos eventos.
- [ ] Não assumir que todos os agentes causam o mesmo dano fisiológico.
- [ ] Usar módulos específicos somente quando mecanismo e parâmetros forem sustentados.
- [ ] Tratar ocorrência como cenário hipotético quando não houver série observacional de pragas na região.
- [ ] Comparar sem dano × danos controlados e calcular efeito adicional sobre os 12 cenários, sem misturar os fatores no desenho central sem justificativa.
- [ ] Testar aditividade/interações e possíveis limites de extrapolação.
- [ ] Avaliar persistência de perdas, recuperação foliar e reservas/mortalidade apenas conforme mecanismo disponível.
**Aceite:** biblioteca de cenários com fonte e mecanismo; nenhuma simulação apresentada como mapa de infestação ou ocorrência real.

### P7 — Fenotipagem, GEDI, Earth Engine e sensoriamento remoto
**Estado inicial:** script de extração e importador presentes na documentação; execução, licenças, disponibilidade e validação de cada produto precisam ser auditadas.
- [ ] Inventariar produtos GEDI disponíveis para local e período; distinguir L2A (altura/estrutura), L2B (cobertura/estrutura) e L4A (biomassa acima do solo estimada).
- [ ] Conferir footprints, qualidade, flags, incerteza, data de aquisição e densidade amostral.
- [ ] Integrar Sentinel-2 (reflectância/índices) com máscara de nuvens e composição temporal consistente.
- [ ] Considerar Landsat e Sentinel-1 somente se acrescentarem informação para lacunas temporais/estruturais.
- [ ] Usar AlphaEarth Foundations como representação geoespacial complementar, não como medição direta de clone, praga ou produtividade.
- [ ] Considerar MapBiomas, IBGE e dados de uso/cobertura para contexto territorial.
- [ ] Documentar escala do pixel/footprint e incompatibilidade entre observações orbitais e variável mensal do 3-PG.
- [ ] Criar variáveis fenotípicas observáveis e proxies; declarar o que não pode ser inferido.
- [ ] Fazer checagem de qualidade, harmonização temporal e espacial, máscara, nuvens e amostragem.
- [ ] Não atribuir fenótipo a um clone sem identificação independente.
- [ ] Não usar GEDI/Sentinel como validação de produtividade sem referência independente compatível.
**Aceite:** pipeline GEE reproduzível, tabela de observações com qualidade/incerteza, documentação de proxies e limites inferenciais.

### P8 — Mensuração, alometria, DAP, altura, volume e produtos
**Estado inicial:** referências e funções didáticas no histórico do projeto; integração com o novo experimento precisa de especificação.
- [ ] Revisar modelos de altura–DAP, volume, biomassa e taper aplicáveis à região/material.
- [ ] Avaliar contribuição de Hélio Garcia Leite e colaboradores sobre prognose e classificação de sítio.
- [ ] Separar equações por espécie, clone, idade, região e finalidade.
- [ ] Implementar estimativas somente com equações e domínio documentados.
- [ ] Relacionar biomassa do 3-PG a estimativas diamétricas sem inventar distribuição de árvores.
- [ ] Se converter produção por hectare em árvores/diâmetros, exigir estrutura de povoamento ou modelo de distribuição validado.
- [ ] Explorar sortimentos e produtos (celulose, energia, serraria) apenas com taper, dimensões comerciais e regras explícitas.
**Aceite:** cadeia de transformação biomassa → volume/estrutura/produtos com fontes, unidades e incerteza visíveis.

### P9 — Avaliação, confronto e validação
**Estado inicial:** há testes de software e confrontos publicados documentados; validação externa representativa continua pendente.
- [ ] Construir matriz observado × previsto por variável, idade, local, tratamento e fonte.
- [ ] Relatar n, unidade, viés, RMSE/RQEM, R² quando adequado, cobertura de intervalos e distribuição dos resíduos.
- [ ] Separar calibração, avaliação no mesmo experimento, validação externa e plausibilidade.
- [ ] Evitar validação aleatória com vazamento de talhões/tempos; preferir separação espacial/temporal/por clone quando viável.
- [ ] Comparar com modelo de referência e baseline simples.
- [ ] Comparar r3PG R com motor Python/JS; registrar versão, parâmetros e tolerância.
- [ ] Testar transferibilidade para local/clone/clima não usado no ajuste, quando existirem dados.
- [ ] Publicar limitações, casos de falha e domínio de validade.
**Aceite:** relatório de desempenho com dados independentes identificados; sem independência, nomear corretamente como teste/confronto.

### P10 — Akademia Florestal: produto operacional e didático
**Estado inicial:** plataforma e bancada integrada estão no repositório; auditoria funcional, científica e de usabilidade pendente.
- [ ] Preservar tela principal e motor existente; implementar em módulos e branches.
- [ ] Criar cadastro de experimentos e cenários com proveniência completa.
- [ ] Permitir configuração dos 12 tratamentos e módulos adicionais sem misturar seus fatores.
- [ ] Criar painel observado × simulado e análise de resíduos.
- [ ] Visualizar série temporal, contrastes, intervalos de incerteza e indicadores.
- [ ] Exibir mapa/localização somente quando a geometria e o papel territorial estiverem documentados.
- [ ] Criar painel GEDI/Sentinel com data, footprint/pixel, flag e incerteza.
- [ ] Criar exportação CSV/JSON e relatório com parâmetros, versão do motor e fontes.
- [ ] Criar documentação/tutorial, definições de conceitos e limitações.
- [ ] Testar acessibilidade, responsividade, estados vazios, unidades e mensagens de erro.
- [ ] Não representar dados sintéticos como resultados reais; sinalizar exemplos.
**Aceite:** um usuário consegue definir cenário, executar, rastrear entradas, interpretar limites e exportar resultados reproduzíveis.

### P11 — Redação, defesa e disseminação
**Estado inicial:** TCC v8/v09 e versões de trabalho referidas fora do repositório; precisa de versão canônica alinhada.
- [ ] Definir versão canônica do TCC e congelar cópia de segurança.
- [ ] Alinhar texto, código, tabelas, figuras, apêndices e memória.
- [ ] Descrever objetivo aprovado sem afirmar fornecimento de dados pela LD.
- [ ] Diferenciar claramente módulo original de desfolha e experimento complementar de genótipo × solo × clima.
- [ ] Incluir revisão atual de Stape e Hélio, com estudos recentes e primários, não apenas clássicos.
- [ ] Inserir métodos de clima, solos, genótipos, GEDI/Sentinel, simulação e avaliação.
- [ ] Incluir somente resultados realmente executados e auditados.
- [ ] Relatar incerteza e limitações sem linguagem promocional.
- [ ] Conferir ABNT, DOI, referências cruzadas e auditoria numérica.
- [ ] Preparar apresentação, roteiro de defesa e demonstração da Akademia.
**Aceite:** todos os números rastreáveis, texto alinhado com código e ausência de alegações não sustentadas.

## 6. Desenho experimental central

| Fator | Níveis | Observação |
|---|---|---|
| Genótipo | 2 materiais contrastantes | contraste demonstrado por fonte experimental |
| Solo | arenoso; argiloso | caracterização quantitativa e método de água disponível |
| Clima | histórico; SSP2-4.5; SSP5-8.5 | GCM(s), período e método de perturbação documentados |
| Duração | 7 anos | passo mensal se compatível com o modelo |
| Tratamentos | 12 combinações | 2 × 2 × 3 |

**Saídas-alvo:** biomassa lenhosa, volume, biomassa foliar, área foliar/IAF e sobrevivência. Antes de relatar, verificar se cada saída é diretamente produzida pelo 3-PG, calculada por extensão ou não representada. Não usar mortalidade/sobrevivência se o mecanismo não estiver implementado e sustentado.

**Contrastes principais:**
- futuro vs histórico dentro de cada genótipo × solo;
- genótipo tolerante vs sensível em cada solo × clima;
- solo arenoso vs argiloso em cada genótipo × clima;
- interação tripla genótipo × solo × clima;
- incerteza entre GCMs e parâmetros.

**Pragas:** módulo adicional de sensibilidade, documentado em matriz separada. Só integrar como quarto fator experimental formal se houver justificativa, parâmetros e recursos para dimensionar o desenho.

## 7. Dados e fontes candidatas — sem pressupor disponibilidade

| Dado | Fonte candidata | Uso | Limite a verificar |
|---|---|---|---|
| Clima futuro | CLIMBra | cenários SSP | GCM, período, variáveis, resolução e licença |
| Clima histórico | NASA POWER; INMET quando aplicável | referência/forçante | grade, estação, viés e período |
| Solo | SoilGrids e PTF documentada | textura/atributos | resolução, profundidade e incerteza |
| Estrutura do dossel | GEDI L2A/L2B | altura e cobertura estrutural | footprints, flags e amostragem |
| Biomassa | GEDI L4A | estimativa de biomassa AGB | incerteza e calibração do produto |
| Resposta espectral | Sentinel-2 | índices e dinâmica temporal | nuvens, saturação e proxies |
| Contexto de uso | MapBiomas; IBGE | cobertura/fitofisionomia | legenda, resolução e data |
| Genótipos/fisiologia | artigos primários Stape/Cunha e demais estudos | contrastes/parâmetros | identidade do material e transferibilidade |
| Modelagem/alometria | trabalhos de Hélio Garcia Leite e coautores | parâmetros, altura, sítio, prognose | domínio amostral e equações |
| Inventário real | eventual parceiro, bases abertas ou artigos | avaliação externa | não disponível/presumido neste planejamento |
| Ocorrência de pragas | artigos/bases fitossanitárias abertas | cenários ou avaliação | cobertura espacial/temporal e identificação do agente |

## 8. Incertezas e riscos que devem permanecer visíveis

1. Materiais genéticos contrastantes podem não ter conjunto completo de parâmetros 3-PG comparável.
2. Parâmetros de um experimento não são automaticamente transferíveis para Triângulo Mineiro.
3. Textura do solo, isoladamente, não define água disponível; profundidade, estrutura, pedregosidade e raízes interferem.
4. CLIMBra exige seleção de GCM, período, referência histórica e método de perturbação; cenários não são previsões pontuais.
5. GEDI tem amostragem por footprints e passagens; não fornece série contínua mensal de todas as áreas.
6. Sentinel-2 mede reflectância, não identifica diretamente clone nem agente causal de desfolha.
7. AlphaEarth é uma representação geoespacial complementar, não observação direta de produtividade/clones/pragas.
8. Danos por pragas sem histórico local são cenários hipotéticos, não mapas de ocorrência.
9. Simulação 3-PG sem inventário independente não prova produtividade real nem superioridade genética.
10. Sensibilidade estatística/ML com dados sintéticos não constitui validação empírica.
11. Referências e patentes exigem leitura de reivindicações e situação jurídica antes de qualquer afirmação de novidade ou patenteabilidade.
12. A região associada à LD não deve ser descrita como talhão da empresa sem evidência geográfica/autorização.

## 9. Ordem recomendada de execução

**Onda A — Fechar base científica antes de aumentar o software**
1. Congelar estado e fazer inventário do repositório.
2. Harmonizar TCC, memória, README e passagem de bastão.
3. Fechar P1: auditoria do módulo original e matriz observado × previsto.
4. Executar P2: revisão de Stape/Hélio e seleção de genótipos.
5. Executar P3 e P4: ponto regional, solos e clima real.
6. Só então congelar inputs e executar P5: 12 cenários.

**Onda B — Acrescentar biologia e observações**
7. P6: cenários de pragas com mecanismos sustentados.
8. P7: GEDI/Sentinel e fenotipagem de variáveis observáveis.
9. P8: ligação com mensuração, alometria, diâmetro e produtos.
10. P9: confronto independente e incertezas.

**Onda C — Consolidar produto e TCC**
11. P10: tornar a Akademia uma ferramenta útil para preparar, executar, auditar e explicar os experimentos.
12. P11: fechar redação e defesa apenas com resultados efetivamente produzidos.

## 10. Convenção de status para auditoria

Cada tarefa deve receber uma das etiquetas:
- **TODO** — ainda não iniciada.
- **DOING** — em execução, sem aceite.
- **IMPLEMENTED** — código/documento existe; ainda pode não ter sido executado com dados reais.
- **TESTED** — verificação técnica passou, não implica validação biológica.
- **EVIDENCE-READY** — dados/fontes e protocolo estão reunidos para análise.
- **SCIENTIFICALLY-EVALUATED** — desempenho confrontado com observações independentes apropriadas.
- **BLOCKED-DATA** — depende de dado externo/privado não disponível.
- **OUT-OF-SCOPE** — explicitamente adiado/excluído.

Não atribuir **DONE** a uma etapa científica sem critérios de aceite documentados e evidências anexadas.

## 11. Registro de auditoria do usuário

Para cada pacote, registrar:
- Data e responsável;
- arquivos/scripts/commit;
- fontes e versão dos dados;
- decisões e justificativas;
- comandos executados;
- logs e testes;
- resultado obtido;
- limitações;
- pendências;
- revisão do usuário/orientador.

## 12. Primeiras ações abertas

- [ ] Conferir branch main e confirmar que PR #1 e PR #2 estão incorporados.
- [ ] Abrir issue por pacote P0–P11, vinculando tarefas menores.
- [ ] Atualizar memória e passagem de bastão com o estado vigente de 14/11/2026.
- [ ] Confirmar qual arquivo de TCC é a versão canônica; não sobrescrever o Drive.
- [ ] Produzir matriz bibliográfica atualizada Stape × Hélio × genótipos × parâmetros.
- [ ] Não iniciar novas simulações científicas até verificar insumos reais e proveniência.

---
**Regra final:** a Akademia deve transformar dados em análises úteis e auditáveis, não apenas acumular módulos. Toda funcionalidade precisa responder a uma pergunta, ter entrada rastreável, produzir uma saída interpretável e declarar o que não consegue concluir.