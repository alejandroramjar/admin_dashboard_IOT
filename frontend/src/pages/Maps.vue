<template>
  <div class="content">
    <div class="container-fluid">
      <card>
        <div class="row">
          <div class="col-md-12">
            <h5>Mapa de Ubicación</h5>
            <div id="map" ref="map"></div>
          </div>
        </div>
      </card>
    </div>
  </div>
</template>

<script>
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

export default {
  data() {
    return {
      center: {
        lat: null,
        lng: null
      },
      map: null,
      type: ['', 'info', 'success', 'warning', 'danger'],
    };
  },
  mounted() {
    const latParam = this.$route.params.lat;
    const lngParam = this.$route.params.lng;

    if (latParam && lngParam) {
      this.center.lat = parseFloat(latParam);
      this.center.lng = parseFloat(lngParam);
      this.initMap();
    } else {
      this.getCurrentLocation(); // Obtener ubicación actual si no hay parámetros
    }
  },
  methods: {
    getCurrentLocation() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            this.center.lat = position.coords.latitude;
            this.center.lng = position.coords.longitude;
            this.initMap();
            this.notify('success', 'Ubicación actualizada', 'Se ha actualizado a tu ubicación actual.');
          },
          (error) => {
            console.error('Error obteniendo la ubicación: ', error);
            this.center.lat = 22.98744183004848; // Ubicación predeterminada
            this.center.lng = -82.4658290633433; // Ubicación predeterminada
            this.initMap();
            this.notify('warning', 'Ubicación predeterminada', 'No se pudo obtener la ubicación, utilizando una ubicación predeterminada.');
          }
        );
      } else {
        console.error('Geolocalización no es soportada por este navegador.');
        this.center.lat = 22.98744183004848; // Ubicación predeterminada UCI
        this.center.lng = -82.4658290633433; // Ubicación predeterminada UCI
        this.initMap();
        this.notify('danger', 'Error', 'Geolocalización no soportada, usando ubicación predeterminada.');
      }
    },
    initMap() {
      this.map = L.map(this.$refs.map).setView([this.center.lat, this.center.lng], 20);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);

      const markerIcon = L.icon({
        iconUrl: require('leaflet/dist/images/marker-icon.png'),
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
        shadowSize: [41, 41]
      });

      L.marker([this.center.lat, this.center.lng], {icon: markerIcon}).addTo(this.map);
    },
    notify(type, title, message) {
      this.$notifications.notify({
        message: `<span><b>${title}</b> - ${message}</span>`,
        icon: 'nc-icon nc-app',
        horizontalAlign: 'center',
        verticalAlign: 'top',
        type: type
      });
    }
  }
};
</script>

<style>
#map {
  height: 100vh; /* Ajusta la altura según sea necesario */
}
</style>
