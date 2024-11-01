<template>
  <card class="card-user">
    <img slot="image" src="https://ununsplash.imgix.net/photo-1431578500526-4d9613015464?fit=crop&fm=jpg&h=300&q=75&w=400" alt="..."/>
    <div class="author">
      <a href="#">
        <img class="avatar border-gray" src="" alt="..."/>

        <h4 class="title">{{user.first_name}} {{ user.last_name}}<br />
          <small>{{user.username}}</small>
        </h4>
      </a>
    </div>
    <p class="description text-center"> telefono: +53{{user.phone}} <br>
      correo: {{user.email}} <br>
      Municipio: {{municipio.nombre}}
    </p>
    <div slot="footer" class="text-center d-flex justify-content-center">
      <button href="#" class="btn btn-simple"><i class="fa fa-facebook-square"></i></button>
      <button href="#" class="btn btn-simple"><i class="fa fa-twitter"></i></button>
      <button href="#" class="btn btn-simple"><i class="fa fa-google-plus-square"></i></button>
    </div>
  </card>
</template>
<script>
  import Card from 'src/components/Cards/Card.vue'
  import axios from "axios";
  export default {
    components: {
      Card
    },
    data () {
      return {
        user: {
        username: '',
        carnet_identidad: '',
        phone: '',
        first_name: '',
        last_name: '',
        email: '',
        municipio: '',
      },
        municipio:'',
        details: [
          {
            title: '12',
            subTitle: 'Files'
          },
          {
            title: '2GB',
            subTitle: 'Used'
          },
          {
            title: '24,6$',
            subTitle: 'Spent'
          }
        ]
      }
    },
    created() {
    this.getUser();
    this.getMunicipio();
    },
    methods: {
      async getUser() {
      try {
        const response = await axios.get('http://localhost:8000/apis/userD/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.user = response.data;
        console.log(this.user);

        // Cargar municipios si se tiene una provincia
        if (this.user.provincia) {
          await this.fetchMunicipios();
        }
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
      async getMunicipio() {
      try {
        const response = await axios.get('http://localhost:8000/apis/userD/municipio', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.municipio = response.data;
        console.log(this.municipio);
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
      getClasses (index) {
        var remainder = index % 3
        if (remainder === 0) {
          return 'col-md-3 col-md-offset-1'
        } else if (remainder === 2) {
          return 'col-md-4'
        } else {
          return 'col-md-3'
        }
      }
    }
  }

</script>
<style>

</style>
