# Escopo público da LD Celulose — protocolo de execução sem dados empresariais
**Decisão metodológica:** 14/11/2026. **TCC II:** desenvolvimento e avaliação do módulo de desfolha do 3-PG.

## Regra de escopo
A LD Celulose é **referência territorial de silvicultura no Triângulo Mineiro**, não fonte confirmada de inventários, materiais genéticos, análises de solo, arquivos operacionais ou acessos físicos. Não presumir parceria, colaboração de dados, polígonos empresariais, identidade de clones ou autorização de ingresso.

Fonte territorial: [Plano de Manejo Florestal — Resumo Público, revisão 007 (15/09/2025)](https://ldcelulose.com.br/fileadmin/user_upload/resumo_publico_plano_de_manejo_florestal.pdf), p. 4, que identifica atuação em nove municípios (Indianópolis, Araguari, Estrela do Sul, Romaria, Nova Ponte, Uberlândia, Prata, Monte Alegre de Minas e Campina Verde). O mapa publicado **não** fornece, por si, coordenadas de talhões utilizáveis como inventário científico.

- Selecionar e registrar uma **coordenada regional de referência** dentro de um município da área de atuação, com fonte independente.
- Não usar nomes como `ld_celulose_talhao` para uma geometria de origem municipal.
- O fatorial aprovado 2 genótipos × 2 texturas × 3 climas = 12 controles sem dano será executado com **dados secundários públicos**, não com parâmetros atribuídos à LD.
- Os conjuntos A1 e C5 atualmente disponíveis são referências de Caldeira (2020) e Borges (2009); **não são, automaticamente, dois genótipos de tolerância hídrica/térmica comprovadamente contrastante**.
- Critério para classes genéticas: evidência experimental de diferença fisiológica; ausência de fonte implica apenas códigos `G1`/`G2` não classificados.
- Solo: fontes públicas com textura, CAD e profundidade do perfil; não inferir CAD por textura isoladamente.
- Clima: histórico NASA POWER e alterações SSP2-4.5/SSP5-8.5 do CLIMBra (Ballarin et al., 2023, DOI: 10.1038/s41597-023-01956-z), registrando modelos, períodos, grid, versão e deltas.
- Pragas: eventos programados e fontes distintas; a ocorrência regional de um agente **não** identifica intensidade no ponto de estudo nem prevê surtos.
- GEDI/Sentinel-2: polígonos públicos de referência, quando disponíveis, caracterizam o ambiente regional. RH98 ≠ altura média; PAI ≠ IAF apenas foliar; AGBD ≠ volume comercial. Se a identidade dos clones/talhões for desconhecida, deixar metadados vazios e classificar como `area_referencia_sem_identidade_genetica`.
- Precedência científica: módulo histórico de desfolha do TCC II **já analisado**; estudo genótipo × solo × clima **proposto/aprovado, ainda sem resultados reais incorporados ao TCC**.
- A opção futura de adicionar dados da LD exige autorização e novo protocolo de uso, sem reclassificar retrospectivamente dados públicos como empresariais.

## Trabalho existente
- Manuscrito do TCC II: versão integral v8 (04/11/2026) no Google Drive, preservada.
- Versão de trabalho v09 (14/11/2026): protocolo complementar no Apêndice C, mantendo resultados históricos; o arquivo DOCX deve ser conferido com os orientadores antes de nova edição.
- Orquestrador: `experimentos/integrado/executar.py` e `cenarios.py`. A execução de demonstração usa dados **sintéticos apenas para testar código**.
- Earth Engine: `sensoriamento/earthengine/extrair_gedi_sent2_talhoes.js` requer polígonos; não implica acesso a áreas da empresa.

## Antes de alegar resultados
1. Fixar a unidade espacial regional pública e sua fonte.
2. Escolher dois conjuntos de parâmetros rastreáveis e testar o contraste fisiológico.
3. Preparar as duas classes de textura/CAD e o recorte CLIMBra.
4. Comparar resultados da porta Python com r3PG em R (método aprovado).
5. Executar 12 condições e só então apresentar os contrastes; pragas são análise adicional.
6. Publicar a matriz observado × previsto apenas quando houver variáveis correspondentes, períodos, escala e independência documentados.

Referências consultadas: LD Celulose (2025), Ballarin et al. (2023), catálogos GEDI L2A/L2B/L4A do Google Earth Engine. Sem confirmação de dados empresariais.
