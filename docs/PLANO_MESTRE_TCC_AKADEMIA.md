# Mapa mestre do TCC II e da Akademia

**Versão:** 1.0 — 14/11/2026  
**Repositório:** [tomdeatj-commits/Akademia](https://github.com/tomdeatj-commits/Akademia)  
**Branch desta proposta:** `docs/mapa-mestre-tcc-akademia-2026-11`  
**Base:** `main` no commit `e5656639551b0fadd1444aad5484360567ef0bd2`

Este documento é o quadro de controle do trabalho. Cada item deve ser atualizado com evidência verificável (arquivo, commit, teste, relatório, fonte ou decisão). “Implementado” não significa “cientificamente validado”.

## 1. Objetivo geral e arquitetura

Construir e documentar um fluxo reproduzível para avaliar crescimento e vulnerabilidade de plantios de eucalipto, mantendo o 3-PG como núcleo ecofisiológico, integrando solo, clima, genótipos, danos bióticos e fenotipagem, sem confundir simulação, calibração e validação.

### Camadas conectadas

1. **Ambiente:** clima histórico/futuro, água disponível, textura e profundidade do solo.
2. **Material genético:** conjuntos de parâmetros de genótipos com proveniência e evidência de contraste.
3. **Fisiologia e crescimento:** 3-PG/r3PG, partição de carbono, dossel, água e produtividade.
4. **Danos bióticos:** desfolha, redução de eficiência e mortalidade como mecanismos distintos; ocorrência de praga só com evidência própria.
5. **Fenotipagem e observação:** inventário de campo quando disponível; GEDI, Sentinel-2 e outras fontes remotas como observações/proxies com escalas e incertezas próprias.
6. **Prognose e mensuração:** biomassa, volume, DAP/altura, estrutura diamétrica, sortimentos e indicadores.
7. **Decisão e comunicação:** comparações, incerteza, limites de validade e visualização na Akademia.

## 2. Frentes de trabalho

### F0 — Governança, rastreabilidade e reprodutibilidade
**Meta:** toda mudança, entrada, número e afirmação rastreável.

- [ ] F0.1 Definir branch de trabalho por entrega e manter `main` estável.
- [ ] F0.2 Confirmar estado real dos PRs #1 e #2 e registrar SHAs de merge.
- [ ] [ ] F0.3 Atualizar memória ativa, progresso, decisões, passagem de bastão e diário sem apagar histórico.
- [ ] F0.4 Reconciliar TCC v8 (Drive, 04/11), TCC v09 de trabalho e documentação/código atual.
- [ ] F0.5 Fazer inventário de fontes, arquivos, scripts, outputs e versões.
- [ ] F0.6 Automatizar auditoria de números do TCC e testes de regressão.
- [ ] F0.7 Gerar manifesto por execução: hash de entradas, versões, parâmetros, coordenada, datas, GCM, semente, saídas e logs.
- [ ] F0.8 Separar status: código verificado / calibrado / confronto externo pontual / validado com dados independentes.

**Aceite:** checkout limpo e reproduzível; relatórios rastreáveis; nenhuma publicação automática para `main`; sem inconsistência entre texto e resultados.

### F1 — TCC II principal: módulo de desfolha no 3-PG
**Meta:** fechar e defender o trabalho que já possui resultados, sem misturar a extensão prospectiva como se estivesse concluída.

- [ ] F1.1 Conferir versão editorial vigente do TCC e alinhar a versão-base com orientadores.
- [ ] F1.2 Conferir transcrição dos artigos primários (Bertulio 2008, Oliveira 2014, Matrangolo 2010 e demais fontes utilizadas) contra os arquivos/figuras originais.
- [ ] F1.3 Reexecutar calibração bayesiana com ambiente, dependências e sementes registrados.
- [ ] F1.4 Reproduzir resultados históricos de referência e confrontar r3PG em R × porta Python × JavaScript.
- [ ] F1.5 Preservar explicitamente a limitação de persistência pós-desfolha total precoce observada em Matrangolo; não ajustar sem mecanismo e dados que sustentem.
- [ ] F1.6 Produzir matriz observado × simulado: variável, unidade, sítio, idade, tratamento, fonte, n, observado, previsto, erro, incerteza e papel científico.
- [ ] F1.7 Rodar auditoria completa de números, figuras, tabelas, citações e referências.
- [ ] F1.8 Harmonizar discussão, limitações e conclusão com o domínio real de validade.
- [ ] F1.9 Preparar pacote de defesa, slides, roteiro oral e respostas a perguntas da banca.

**Aceite:** qualquer número citado recalculável; toda comparação identifica independência e escala; r3PG e implementações paralelas comparados; limitações explícitas; documento e anexos regeneráveis.

### F2 — Experimento aprovado: genótipo × solo × clima
**Meta:** executar as 12 combinações centrais no recorte regional publicamente documentado da LD Celulose, usando exclusivamente dados secundários até que outra fonte seja autorizada e entregue.

- [ ] F2.1 Selecionar coordenada regional representativa com fonte cartográfica/documental independente; não chamar de talhão LD.
- [ ] F2.2 Selecionar dois materiais/genótipos com parametrizações completas compatíveis com o modelo.
- [ ] F2.3 Demonstrar com literatura experimental que os materiais têm tolerância contrastante ao estresse hídrico/térmico; se não demonstrado, reportar G1/G2 sem rótulos “tolerante/sensível”.
- [ ] F2.4 Auditar os 82 parâmetros de cada material, origem, espécie/clonalidade, unidades, idade de referência e compatibilidade entre estudos.
- [ ] F2.5 Obter classes arenosa/argilosa com fonte pública; estimar CAD por método explícito (textura, profundidade efetiva, água disponível) e análise de sensibilidade.
- [ ] F2.6 Definir clima histórico observacional, período, grade e agregação mensal.
- [ ] F2.7 Obter CLIMBra original e normalizar por GCM/SSP; arquivar DOI, versão, grade, célula, períodos e checksum.
- [ ] F2.8 Revisar a transformação de variáveis climáticas para entradas do 3-PG. Em particular, radiação líquida CLIMBra não é radiação incidente: justificar, testar ou substituir transformação.
- [ ] F2.9 Decidir tratamento de CO₂, extremos térmicos e geadas; se ausentes, declarar como limitações e não sugerir cenário integral.
- [ ] F2.10 Harmonizar plantio, inicialização, densidade, fertilidade FR, água inicial e demais condições de contorno entre cenários.
- [ ] F2.11 Executar matriz de 12 controles (2 × 2 × 3), sem danos.
- [ ] F2.12 Calcular mudanças futuras vs histórico e interação tripla G × solo × clima, com definição algébrica e incerteza/sensibilidade.
- [ ] F2.13 Confrontar implementação Python com r3PG em R para todos os controles selecionados.
- [ ] F2.14 Fazer análises de sensibilidade para CAD, parâmetros genéticos, GCMs, transformação climática e condições de contorno.
- [ ] F2.15 Redigir resultados somente depois das execuções reproduzíveis.

**Aceite:** 12 simulações com entradas reais e fontes documentadas; comparação com R; interação calculada e auditável; sem classificar genótipos sem evidência.

### F3 — Pragas, doenças e danos fisiológicos
**Meta:** conectar danos com fisiologia, mantendo ocorrência epidemiológica separada de cenários impostos.

- [ ] F3.1 Construir biblioteca de agentes: hospedeiro, órgão afetado, mecanismo, janela temporal, intensidade, frequência e fonte.
- [ ] F3.2 Separar desfolha, redução de eficiência fotossintética e mortalidade; impedir dupla contagem.
- [ ] F3.3 Definir cenário de ataque hipotético vs cenário sustentado pela literatura.
- [ ] F3.4 Relacionar ataque a genótipo/ambiente somente quando houver evidência de interação.
- [ ] F3.5 Incluir recuperação foliar e efeitos persistentes apenas com mecanismo e parâmetros sustentados.
- [ ] F3.6 Avaliar interação dano × genótipo × solo × clima como expansão fatorial secundária, sem confundir com as 12 condições centrais aprovadas.
- [ ] F3.7 Não inferir ocorrência/severidade de praga apenas de NDVI/NDRE ou anomalia sazonal.
- [ ] F3.8 Comparar impactos em biomassa, volume, sobrevivência e sortimentos, reportando incerteza.

**Aceite:** cada evento tem fonte/classificação; cenário hipotético está marcado; nenhum diagnóstico automático de praga; efeitos adicionais identificáveis.

### F4 — Fenotipagem e sensoriamento remoto
**Meta:** usar dados remotos para observação de estrutura e condição espectral, sem atribuir propriedades que os sensores não medem diretamente.

- [ ] F4.1 Escolher unidades espaciais públicas e legais para análise regional; guardar origem e geometria.
- [ ] F4.2 GEDI L2A: QA/QC e métricas de altura relativa (ex.: RH98), cobertura temporal e amostragem footprint.
- [ ] F4.3 GEDI L2B: PAI/estrutura do dossel, deixando claro que não equivale diretamente a LAI foliar.
- [ ] F4.4 GEDI L4A: AGBD como produto modelado com incerteza, não biomassa medida diretamente.
- [ ] F4.5 Sentinel-2: mascarar nuvens/sombra, compor por período, NDVI/NDRE e índices adicionais apenas com justificativa.
- [ ] F4.6 Verificar período real de cobertura GEDI (não retroprojetar para o ciclo 2015–2022).
- [ ] F4.7 Definir agregação espacial/temporal e número mínimo de observações válidas.
- [ ] F4.8 Comparar com inventário/parcelas apenas quando houver variável, unidade, escala e data compatíveis.
- [ ] F4.9 Separar observação regional sem identidade genética de observação associada a G1/G2.
- [ ] F4.10 Investigar anomalias espectrais como alerta para inspeção, nunca como identificação causal de praga.
- [ ] F4.11 Avaliar GEDI × Sentinel-2 × 3-PG com validação espacial/temporal sem vazamento.

**Aceite:** manifesto Earth Engine; QA/QC documentado; sem preenchimento artificial de ausência; incertezas e proxies claramente rotulados.

### F5 — Solo, hidrologia e sítio
**Meta:** tornar o fator solo mecanístico, não apenas dois rótulos texturais.

- [ ] F5.1 Compilar textura, densidade aparente, carbono, pedregosidade quando disponíveis, profundidade efetiva e retenção de água.
- [ ] F5.2 Avaliar SoilGrids e bases brasileiras/regionais, resoluções e profundidade dos produtos.
- [ ] F5.3 Calcular CAD por camada e perfil, com método de pedotransferência validado para contexto tropical quando disponível.
- [ ] F5.4 Incluir profundidade radicular/água acessível com evidência; comparar CAD fixa e dinâmica.
- [ ] F5.5 Avaliar lençol freático, relevo e posição topográfica somente se a escala e a fonte sustentarem.
- [ ] F5.6 Fazer análise de incerteza da CAD e das classes de solo.
- [ ] F5.7 Harmonizar parametrização com classes de água do 3-PG/r3PG.

**Aceite:** solo representado por parâmetros físicos rastreáveis; CAD não inferida apenas de “arenoso/argiloso”; incerteza propagada.

### F6 — Parametrização fisiológica e literatura (Stape, Hélio Garcia Leite e colaboradores)
**Meta:** atualizar fundamentos e parâmetros a partir de trabalhos recentes e rastrear sua transferibilidade.

- [ ] F6.1 Fazer revisão sistemática cronológica de trabalhos de Stape e coautores (não usar somente artigo clássico).
- [ ] F6.2 Fazer revisão de Hélio Garcia Leite e coautores: modelos, alometria, classificação de sítios, crescimento, IA e mensuração.
- [ ] F6.3 Construir tabela parâmetro × definição × valor × unidade × fonte × espécie/clone × idade × método.
- [ ] F6.4 Distinguir parâmetros medidos, calibrados, assumidos, derivados e não identificados.
- [ ] F6.5 Comparar versões e implementações 3-PG/r3PG, incluindo partição de carbono, VPD, água e alometria.
- [ ] F6.6 Avaliar redes neurais/ML para estimativa de parâmetros como benchmark, sem substituir fisiologia sem evidência.
- [ ] F6.7 Selecionar apenas parâmetros que correspondam a genótipos com identidade/evidência comprovadas.
- [ ] F6.8 Documentar conflitos entre fontes e fazer análise de transferibilidade para Triângulo Mineiro.

**Aceite:** caderno de parâmetros completo; cada valor auditável; nenhum clone rotulado por suposição; artigo recente não aceito apenas por ser recente.

### F7 — Mensuração, alometria, DAP, altura, taper e sortimentos
**Meta:** conectar a simulação ecofisiológica a indicadores comerciais mensuráveis.

- [ ] F7.1 Inventariar equações alométricas por espécie/material, sítio, idade e compartimento.
- [ ] F7.2 Confrontar DAP e altura simulados com equações/observações compatíveis.
- [ ] F7.3 Integrar modelos hipsométricos e volumétricos com fonte e domínio.
- [ ] F7.4 Avaliar taper e cubagem (Smalian, Huber, Newton) com diâmetros ao longo do fuste quando disponíveis.
- [ ] F7.5 Traduzir volume em sortimentos apenas com especificação dimensional e comercial documentada.
- [ ] F7.6 Propagar incerteza do DAP/altura/volume/alometria.
- [ ] F7.7 Manter resultados comerciais separados de biomassa/volume ecofisiológicos quando não comparáveis.

**Aceite:** variável comercial rastreável e compatível; validação independente ou designação explícita como estimativa exploratória.

### F8 — Métodos quantitativos e inteligência artificial
**Meta:** usar métodos de análise para responder perguntas específicas, não como adorno.

- [ ] F8.1 Definir estimandos e contrastes antes de escolher algoritmo.
- [ ] F8.2 Fazer análise de sensibilidade global (Morris/Sobol) dos parâmetros dominantes.
- [ ] F8.3 Usar RF/ML como metamodelo ou estimador auxiliar com validação agrupada por local/tempo.
- [ ] F8.4 Prevenir vazamento por parcelas, clones, locais, janelas temporais e GCM.
- [ ] F8.5 Comparar modelos simples, híbridos e 3-PG puro.
- [ ] F8.6 Quantificar intervalos preditivos e incerteza paramétrica/estrutural/climática.
- [ ] F8.7 Não reportar R² alto em dados simulados como validação externa.

**Aceite:** algoritmo tem papel definido, benchmark, validação sem vazamento e ganho mensurável sobre baseline.

### F9 — Akademia: ferramenta executável e didática
**Meta:** tornar o sistema útil, transparente, reproduzível e auditável.

- [ ] F9.1 Preservar simulador 3-PG existente e regressões da versão original.
- [ ] F9.2 Separar abas: motor base, experimento integrado, dados observados, fenotipagem, danos, auditoria e documentação.
- [ ] F9.3 Mostrar entradas, fontes, unidades, parâmetros, condições de contorno e limites.
- [ ] F9.4 Executar os mesmos casos em Python e r3PG R; guardar saídas e tolerâncias.
- [ ] F9.5 Criar importação validada para CSVs de clima, solo, inventário, GEDI e Sentinel-2.
- [ ] F9.6 Gerar gráficos de séries temporais, cenários, contrastes, incerteza e resíduos.
- [ ] F9.7 Criar matriz observado × previsto com métricas apropriadas e metadados.
- [ ] F9.8 Exportar CSV/JSON e relatório de execução com manifesto.
- [ ] F9.9 Implementar estados claros: aguardando entradas, pronto para executar, executado, auditado, confronto externo, validado.
- [ ] F9.10 Tutorial e compêndio conectados às equações e aos controles da interface.
- [ ] F9.11 Acessibilidade mobile, legendas/unidades e paletas legíveis.
- [ ] F9.12 Não publicar demonstrações sintéticas como resultados científicos.

**Aceite:** operação reproduzível, entradas auditadas, ausência de dados apresentada honestamente, interface móvel e nenhum resultado simulado confundido com medição.

### F10 — Manuscrito, comunicação e defesa
- [ ] F10.1 Definir hierarquia entre TCC II (módulo desfolha) e proposta complementar (genótipo × solo × clima).
- [ ] F10.2 Atualizar introdução, objetivos e métodos somente após decisão com orientadores.
- [ ] F10.3 Escrever resultados com números regenerados.
- [ ] F10.4 Apresentar interação genótipo × solo × clima e modulação por dano, se executadas.
- [ ] F10.5 Incluir fenotipagem como análise observacional apenas no período e local cobertos.
- [ ] F10.6 Preparar resumo, abstract, figuras, tabelas, referências ABNT e apêndices.
- [ ] F10.7 Preparar slides e roteiro de defesa de dezembro/2026.

## 3. Sequência crítica recomendada

1. **P0 — Congelar evidências do TCC principal:** reexecução, matriz observado × simulado, limites, auditoria e alinhamento com orientadores.
2. **P1 — Fechar entradas genótipo × solo × clima:** parâmetros completos de genótipos, contraste experimental, CAD, coordenada, CLIMBra e clima histórico.
3. **P2 — Verificar implementação:** Python × r3PG R, controles e testes de sensibilidade.
4. **P3 — Executar as 12 condições:** só após todas as entradas passarem pelo contrato.
5. **P4 — Danos/pragas:** biblioteca com fontes e cenários secundários; não confundir hipótese com ocorrência.
6. **P5 — Fenotipagem:** GEDI/Sentinel-2 em datas/áreas cobertas; observações como proxies com QA/QC.
7. **P6 — Alometria e mensuração:** conectar crescimento a DAP, altura, volume e sortimentos sem duplicar estimativas.
8. **P7 — Integração final no TCC e Akademia:** somente outputs auditados.
9. **P8 — Defesa e reprodutibilidade:** congelar versões, dados, scripts, manifesto e apresentação.

## 4. Fontes de dados previstas (a confirmar por variável e escala)

| Domínio | Fonte candidata | Uso pretendido | Limite que precisa ser auditado |
|---|---|---|---|
| Clima histórico | NASA POWER / outras bases observacionais | Forçantes históricas | Resolução espacial e variável |
| Clima futuro | CLIMBra / Ballarin et al. (2023) | SSP2-4.5 e SSP5-8.5 | GCM, período, grade, radiação líquida/incidente |
| Solo | SoilGrids e bases brasileiras | Textura, carbono, densidade e profundidade | CAD e PTF precisam de método e domínio |
| Fenotipagem | GEDI L2A/L2B/L4A | RH98, PAI, AGBD | Pegada, cobertura, qualidade e incerteza |
| Fenotipagem | Sentinel-2 | NDVI/NDRE e trajetória espectral | Nuvens, escala, sazonalidade e não especificidade |
| Modelagem | r3PG R / 3-PG original | Referência de implementação | Versão, parâmetros, unidades, tolerâncias |
| Genótipo | Artigos de Stape/Cunha e bases publicadas | Contraste de tolerância e parâmetros | Transferibilidade e identidade dos materiais |
| Crescimento/alometria | Hélio Garcia Leite e coautores; outras fontes primárias | DAP, altura, biomassa, volume | Espécie, idade, local, amostra e domínio |

As fontes são candidatas, não garantia de que contenham todas as variáveis necessárias.

## 5. Registro de decisões e limites

1. LD Celulose é apenas referência territorial pública. Não presumir parceria, acesso, talhões, clones, inventário ou autorização.
2. Dados empresariais, se futuramente fornecidos e autorizados pelo autor, entram em nova versão com proveniência e protocolo; não são requisito atual.
3. A proposta aprovada tem 12 cenários centrais sem dano. Danos/pragas são camada adicional.
4. A1 e C5 não podem ser rotulados como genótipos tolerante/sensível sem evidência experimental específica.
5. GEDI/Sentinel-2 caracterizam observações remotas; não medem automaticamente LAI exato, volume comercial nem incidência de praga.
6. O orquestrador atual usa a porta Python do 3-PGpjs. A comparação efetiva com r3PG em R segue pendente.
7. Fixtures sintéticas podem testar software, não produzir evidência ecológica.
8. A matriz observado × previsto só pode incluir correspondências na mesma variável, unidade, escala, idade e período; independência deve ser declarada.
9. O TCC II principal e a proposta complementar precisam ter resultados/cronologias claramente separados.
10. A versão TCC v8 no Drive (04/11/2026) e a v09 de trabalho devem ser reconciliadas antes de sobrescrever qualquer documento.

## 6. Quadro de auditoria por entrega

| ID | Evidência exigida antes de marcar concluído | Status inicial |
|---|---|---|
| F0 | commit, logs, manifestos, memória e teste | Em revisão |
| F1 | execução reproduzida + matriz de evidências + TCC auditado | Pendente |
| F2 | 12 execuções reais + inputs rastreados + conferência r3PG R | Pendente |
| F3 | biblioteca de danos citada + cenários documentados | Parcial |
| F4 | exportações GEE reais + QA/QC + comparação compatível | Ferramenta preparada; dados pendentes |
| F5 | perfil/água/CAD derivados com método e incerteza | Pendente |
| F6 | revisão cronológica + caderno de parâmetros e fontes | Pendente |
| F7 | equações/mensurações com domínio + erro | Parcial |
| F8 | análises com baseline e validação agrupada | Parcial |
| F9 | execução ponta a ponta + exportações + regressões + documentação | Parcial |
| F10 | manuscrito reconciliado + parecer orientadores + defesa | Pendente |

**Como auditar:** cada checkbox somente muda para concluído quando a evidência é anexada ou vinculada. Registrar data, autor, commit, comandos, resultado e limitações. Em caso de falha, abrir issue com etapa, reprodução mínima e critério de correção.
