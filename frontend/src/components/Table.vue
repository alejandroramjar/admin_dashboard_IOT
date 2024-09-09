<template>
  <table class="table">
    <thead>
      <slot name="columns">
        <tr>
          <th v-for="column in columns" :key="column">{{ column }}</th>
        </tr>
      </slot>
    </thead>
    <tbody>
      <tr v-for="(item, index) in data" :key="index">
        <slot :row="item">
          <td v-for="column in columns" :key="column" v-if="hasValue(item, column)">{{ itemValue(item, column) }}</td>
          <td><router-link :to="{ name: 'Maps', params: { lat: item.Latitud, lng: item.Longitud } }" class="btn btn-primary">Ver Ubicación
                    </router-link></td>
          <td><router-link :to="{ name: 'Overview', params: {selectedDevice: item.id} }" class="btn btn-outline-warning">Monitorear
                    </router-link></td>
        </slot>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: 'l-table',
  props: {
    columns: Array,
    data: Array
  },
  methods: {
    hasValue(item, column) {
      return item[column] !== undefined;
    },
    itemValue(item, column) {
      return item[column];
    }
  }
}
</script>

<style>
</style>
