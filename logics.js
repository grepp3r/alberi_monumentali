
function parseURLParameters(divName) {
  let params = new URLSearchParams(document.location.search);
  let value = params.get(divName);
  if (value == null) {
    return null
  }
  return value.toLowerCase();
}

function getOpenstreetmapUrl(lat, lng, zoom){
  return "https://www.openstreetmap.org/#map="+zoom+"/"+lat+"/"+lng+"&layers=C"
}

function parse_alberi(nome, alberi, map, filter){
  var markers = [];
  for (i = 0; i < alberi.length; i++){
    albero = alberi[i]
    var marker = L.marker([albero.lat, albero.lng])
      .bindPopup('<b>'+albero.n_com+'</b><br>'+
        albero.n_sc +
        '<br>circonferenza: '+albero.circ +
        '<br>altezza: '+albero.h +
        '<br>quota: '+albero.geo_altitude+'' +
        '<br><a href="'+getOpenstreetmapUrl(albero.lat, albero.lng, 17)+'">OSM</a>');
    if (
      (filter != null && 
        albero.n_com.toLowerCase().indexOf(filter) > -1) ||
      filter == null
    ){
      console.log(albero.n_com)
      markers.push(marker);
    }
  }
  var markers_layer = L.layerGroup(markers);
  map.addOverlay(markers_layer, nome);
}

var map = L.map('map').setView([45, 8], 9);

var layerControl = L.control.layers().addTo(map);
filter = parseURLParameters('filter');
console.log('--', filter);
parse_alberi('friuli', alberi_friuli, layerControl, filter);
parse_alberi('veneto', alberi_veneto, layerControl, filter);
parse_alberi('piemonte', alberi_piemonte, layerControl, filter);


L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(map);
