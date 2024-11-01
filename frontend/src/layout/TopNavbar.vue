<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
      <a v-if="checkifadmin" class="navbar-brand nav-link" @click="admin" href="#">Admin site</a>
      <button type="button"
              class="navbar-toggler navbar-toggler-right"
              :class="{toggled: $sidebar.showSidebar}"
              aria-controls="navigation-index"
              aria-expanded="false"
              aria-label="Toggle navigation"
              @click="toggleSidebar">
        <span class="navbar-toggler-bar burger-lines"></span>
        <span class="navbar-toggler-bar burger-lines"></span>
        <span class="navbar-toggler-bar burger-lines"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end">

        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link" href="#">
              Cuenta
            </a>
          </li>
          <base-dropdown title="Acciones">
            <a class="dropdown-item" href="#">Acción 1</a>
            <a class="dropdown-item" href="#">Acción 2</a>
            <a class="dropdown-item" href="#">Acción 3</a>
            <a class="dropdown-item" href="#">Acción 4</a>
            <a class="dropdown-item" href="#">Acción 5</a>
            <a class="dropdown-item" href="#">Something</a>
            <div class="divider"></div>
            <a class="dropdown-item" href="#">Separated link</a>
          </base-dropdown>
          <li class="nav-item"><a @click="logout" href="#" class="nav-link"> Cerrar Sesión</a></li>
        </ul>
      </div>
    </div>
  </nav>
</template>
<script>
import axios from 'axios';

export default {
  data() {
    return {
      activeNotifications: false,
      checkifadmin: false  // Cambiado a data()
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    this.checkifadmin = await this.checkIfAdmin(token);  // Llamar a la función en el ciclo de vida
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
    async logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
    async admin() {
      window.location.href = 'http://localhost:8000/admin/';
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
  }
}
</script>

<style>

</style>
