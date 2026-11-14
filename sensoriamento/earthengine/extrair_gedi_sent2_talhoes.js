// Akademia | Exportação operacional GEDI + Sentinel-2 por talhão (Google Earth Engine).
// Cole em https://code.earthengine.google.com/ e substitua o asset pelo SEU talhão.
// Executa 4 exportações CSV reais (L2A, L2B, L4A, Sentinel-2).
// Sem asset, sem autenticação Earth Engine ou sem observações, NÃO produz valores.
// GEDI footprint ≈ 25m e métricas observacionais não equivalem diretamente a saídas 3-PG.
// Catálogos oficiais:
// https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI02_A_002_MONTHLY
// https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI02_B_002_MONTHLY
// https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI04_A_002_MONTHLY
// https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED

var CONFIG = {
  assetTalhoes: 'INSIRA_SEU_ASSET_GEE',
  idCampo: 'talhao_id',
  genotipoCampo: 'genotipo',  // G1 ou G2, cadastrado no talhão (opcional)
  soloCampo: 'solo',          // arenoso ou argiloso, cadastrado no talhão (opcional)
  inicio: '2019-04-01',       // GEDI não cobre anos anteriores a 2019
  fimExclusivo: '2025-07-01',
  pastaDrive: 'Akademia_GEDI',
  maxPixelsPorTalhao: 1e9
};
if (CONFIG.assetTalhoes === 'INSIRA_SEU_ASSET_GEE') {
  throw new Error('Defina CONFIG.assetTalhoes com o asset dos talhões reais.');
}
var talhoes = ee.FeatureCollection(CONFIG.assetTalhoes).map(function(f) {
  return f.set({
    akademia_talhao_id: f.get(CONFIG.idCampo),
    akademia_genotipo: f.get(CONFIG.genotipoCampo),
    akademia_solo: f.get(CONFIG.soloCampo)
  });
});
var listaColunas = ['talhao_id','genotipo','solo','ano_mes','produto','variavel',
                    'valor','n_pixels_validos','unidade','origem','comparavel'];

function reduzirImagens(ic, band, produto, unidade, resolucao) {
  ic = ee.ImageCollection(ic).filterBounds(talhoes)
                            .filterDate(CONFIG.inicio, CONFIG.fimExclusivo)
                            .select([band]);
  var n = ic.size();
  var imgs = ic.toList(n);
  var grupos = ee.Algorithms.If(n.gt(0), ee.List.sequence(0, n.subtract(1)).map(function(j) {
    var im = ee.Image(imgs.get(j));
    var stats = im.select(band).reduceRegions({
      collection: talhoes,
      reducer: ee.Reducer.mean().combine({
        reducer2: ee.Reducer.count(), sharedInputs: true
      }),
      scale: resolucao,
      tileScale: 4
    });
    return stats.filter(ee.Filter.gt(band + '_count', 0)).map(function(f) {
      return ee.Feature(null, {
        talhao_id: f.get('akademia_talhao_id'),
        genotipo: f.get('akademia_genotipo'),
        solo: f.get('akademia_solo'),
        ano_mes: im.date().format('YYYY-MM'),
        produto: produto,
        variavel: band,
        valor: f.get(band + '_mean'),
        n_pixels_validos: f.get(band + '_count'),
        unidade: unidade,
        origem: produto,
        comparavel: 'nao'
      });
    });
  }),ee.List([]));
  return ee.FeatureCollection(ee.List(grupos)).flatten();
}

function enviar(colecao, nome) {
  Export.table.toDrive({
    collection: colecao,
    description: nome,
    folder: CONFIG.pastaDrive,
    fileFormat: 'CSV',
    selectors: listaColunas
  });
}

var L2A = ee.ImageCollection('LARSE/GEDI/GEDI02_A_002_MONTHLY')
  .map(function(im) {
    return im.updateMask(im.select('quality_flag').eq(1))
             .updateMask(im.select('degrade_flag').eq(0));
  });
var L2B = ee.ImageCollection('LARSE/GEDI/GEDI02_B_002_MONTHLY')
  .map(function(im) {
    return im.updateMask(im.select('l2b_quality_flag').eq(1))
             .updateMask(im.select('degrade_flag').eq(0));
  });
var L4A = ee.ImageCollection('LARSE/GEDI/GEDI04_A_002_MONTHLY')
  .map(function(im) {
    return im.updateMask(im.select('l4_quality_flag').eq(1))
             .updateMask(im.select('degrade_flag').eq(0));
  });

enviar(reduzirImagens(L2A, 'rh98', 'GEDI_L2A', 'm (altura relativa do dossel)',25),
       'AKADEMIA_GEDI_L2A_RH98');
enviar(reduzirImagens(L2B, 'pai', 'GEDI_L2B', 'm2/m2 (índice de área de plantas)',25),
       'AKADEMIA_GEDI_L2B_PAI');
enviar(reduzirImagens(L4A, 'agbd', 'GEDI_L4A', 'Mg/ha (biomassa aérea estimada)',25),
       'AKADEMIA_GEDI_L4A_AGBD');

// Sentinel-2: séries regulares de índices espectrais, sem atribuir causalidade a pragas.
var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(talhoes).filterDate(CONFIG.inicio, CONFIG.fimExclusivo)
  .filter(ee.Filter.lte('CLOUDY_PIXEL_PERCENTAGE',80))
  .map(function(im) {
    var scl = im.select('SCL');
    var mascara = scl.neq(3).and(scl.neq(8)).and(scl.neq(9))
                     .and(scl.neq(10)).and(scl.neq(11)).and(scl.neq(0));
    var b8 = im.select('B8'), b4 = im.select('B4'), b5 = im.select('B5');
    var ndvi=b8.subtract(b4).divide(b8.add(b4)).rename('ndvi');
    var ndre=b8.subtract(b5).divide(b8.add(b5)).rename('ndre');
    return ee.Image.cat(ndvi,ndre).updateMask(mascara)
             .copyProperties(im,['system:time_start']);
  });
var inicio=ee.Date(CONFIG.inicio);
var numeroMeses=ee.Number(ee.Date(CONFIG.fimExclusivo).difference(inicio,'month')).ceil();
var listaMensal=ee.List.sequence(0,numeroMeses.subtract(1)).map(function(m){
  var a=inicio.advance(m,'month'),b=a.advance(1,'month');
  var mes=s2.filterDate(a,b);
  return mes.median().set('system:time_start',a.millis()).set('quantidade_cenas',mes.size());
});
var sintese=ee.ImageCollection.fromImages(listaMensal)
  .filter(ee.Filter.gt('quantidade_cenas',0));
enviar(reduzirImagens(sintese,'ndvi','SENTINEL2_SR','índice sem unidade',20),
       'AKADEMIA_S2_NDVI');
enviar(reduzirImagens(sintese,'ndre','SENTINEL2_SR','índice sem unidade',20),
       'AKADEMIA_S2_NDRE');

Map.centerObject(talhoes,11);
Map.addLayer(talhoes,{color:'yellow'},'Talhões monitorados');
print('Talhões:',talhoes.size());
print('As tarefas de exportação estão em Tasks; clique Run para cada CSV.');
print('A ausência de GEDI válido em um talhão/mês não deve ser preenchida por extrapolação.');
