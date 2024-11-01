<template>
  <div class="wrapper">
    <side-bar>
      <mobile-menu slot="content"></mobile-menu>
      <sidebar-link to="/admin/overview">
        <i class="nc-icon nc-chart-pie-35"></i>
        <p>Monitoreo</p>
      </sidebar-link>
      <sidebar-link to="/admin/user">
        <i class="nc-icon nc-circle-09"></i>
        <p>User Profile</p>
      </sidebar-link>
      <sidebar-link to="/admin/table-list">
        <i class="nc-icon nc-vector"></i>
        <p>Mis dispositivos</p>
      </sidebar-link>
      <sidebar-link to="/admin/maps">
        <i class="nc-icon nc-pin-3"></i>
        <p>Mapa y Ubicaciones</p>
      </sidebar-link>
      <sidebar-link v-if="true" to="/admin/typography">
        <i class="nc-icon nc-paper-2"></i>
        <p>Listado de dispositivos</p>
      </sidebar-link>
    </side-bar>
    <div class="main-panel">
      <top-navbar></top-navbar>

      <dashboard-content @click="toggleSidebar">

      </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss">

</style>
<script>
  import TopNavbar from './TopNavbar.vue'
  import ContentFooter from './ContentFooter.vue'
  import DashboardContent from './Content.vue'
  import MobileMenu from './MobileMenu.vue'
  import axios from "axios";
  export default {
        data() {
    return {
      activeNotifications: false,
      checkifadmin: false
    };
  },
    components: {
      TopNavbar,
      ContentFooter,
      DashboardContent,
      MobileMenu
    },
      async created(){
    const token = localStorage.getItem('token');
    this.checkifadmin = await this.checkIfAdmin(token);
  },
    methods: {
          async checkIfAdmin(token) {
      try {
        const response = await axios.get('http://localhost:8000/apis/user/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        return response.data.is_admin;  // true si es admin, false en caso contrario
      } catch (error) {
        console.error('Error al verificar el rol del usuario:', error);
        return false;
      }
    },
      toggleSidebar () {
        if (this.$sidebar.showSidebar) {
          this.$sidebar.displaySidebar(false)
        }
      }
    }
  }

</script>
