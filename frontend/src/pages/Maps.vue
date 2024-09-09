<!--<template>
  <gmap-map
    id="map"
    :center="center"
    :zoom="13"
    :options="options"
    map-type-id="terrain"
  >
    <gmap-marker :position="center">
    </gmap-marker>
  </gmap-map>
</template>-->
<template>
  <div id="map" ref="map" />
</template>
<!--<script>
  import {API_KEY} from './Maps/API_KEY'
  import Vue from 'vue'
  import * as VueGoogleMaps from 'vue2-google-maps'
  Vue.use(VueGoogleMaps, {
    load: {
      key: API_KEY
    }
  })
  export default {
    data () {
      return {
        center: {
          lat: 40.748817,
          lng: -73.985428
        },
        options: {
          styles: [{
            'featureType': 'water',
            'stylers': [{'saturation': 43}, {'lightness': -11}, {'hue': '#0088ff'}]
          }, {
            'featureType': 'road',
            'elementType': 'geometry.fill',
            'stylers': [{'hue': '#ff0000'}, {'saturation': -100}, {'lightness': 99}]
          }, {
            'featureType': 'road',
            'elementType': 'geometry.stroke',
            'stylers': [{'color': '#808080'}, {'lightness': 54}]
          }, {
            'featureType': 'landscape.man_made',
            'elementType': 'geometry.fill',
            'stylers': [{'color': '#ece2d9'}]
          }, {
            'featureType': 'poi.park',
            'elementType': 'geometry.fill',
            'stylers': [{'color': '#ccdca1'}]
          }, {
            'featureType': 'road',
            'elementType': 'labels.text.fill',
            'stylers': [{'color': '#767676'}]
          }, {
            'featureType': 'road',
            'elementType': 'labels.text.stroke',
            'stylers': [{'color': '#ffffff'}]
          }, {'featureType': 'poi', 'stylers': [{'visibility': 'off'}]}, {
            'featureType': 'landscape.natural',
            'elementType': 'geometry.fill',
            'stylers': [{'visibility': 'on'}, {'color': '#b8cb93'}]
          }, {'featureType': 'poi.park', 'stylers': [{'visibility': 'on'}]}, {
            'featureType': 'poi.sports_complex',
            'stylers': [{'visibility': 'on'}]
          }, {'featureType': 'poi.medical', 'stylers': [{'visibility': 'on'}]}, {
            'featureType': 'poi.business',
            'stylers': [{'visibility': 'simplified'}]
          }]
        }
      }
    }
  }
</script>
<style>
  #map {
    min-height: calc(100vh - 123px);
  }
</style>-->
<script>
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

export default {
  data() {
    return {
      center: {
        lat: 40.748817,
        lng: -73.985428
      },
      map: null
    };
  },
  mounted() {
    this.lat = this.$route.params.lat; // Obtener latitud de los parámetros de la ruta
    this.lng = this.$route.params.lng; // Obtener longitud de los parámetros de la ruta
    this.initMap();
  },
  methods: {
    initMap() {
      // Inicializa el mapa
      this.map = L.map(this.$refs.map).setView([this.center.lat, this.center.lng], 13);

      // Añade la capa de OpenStreetMap
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);
      // Crear un icono personalizado (opcional)
    const markerIcon = L.icon({
      iconUrl: require('leaflet/dist/images/marker-icon.png'), // Asegúrate de que la ruta sea correcta
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
      shadowSize: [41, 41]
    });

      // Añade un marcador en el centro
      L.marker([this.center.lat, this.center.lng], { icon: markerIcon }).addTo(this.map);
    }
  }
};
</script>

<style>
#map {
  height: 100vh; /* Ajusta la altura según sea necesario */
}
</style>
