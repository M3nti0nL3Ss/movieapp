<template>
  <div>
    <h1>Movies</h1>
    <v-row>
      <v-col v-for="id in movieIds" :key="id" cols="12" sm="6" md="4">
        <v-card @click="goToMovie(id)">
          <v-card-title>{{ movies[id].title }}</v-card-title>
          <v-card-text class="d-flex align-center">
            <v-rating :value="movies[id].average_grade" readonly half-increments></v-rating>
            <span class="ml-2">{{ movies[id].average_grade.toFixed(1) }}</span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-pagination
      v-model="currentPage"
      :length="totalPages"
      @click="handlePageChange(currentPage)"
    ></v-pagination>
  </div>
</template>

<style scoped>
.v-card-text {
  padding: 10px 0;
}
</style>

<script>
import { mapState, mapActions } from 'vuex';

export default {
  name: 'HomePage',
  data() {
    return {
      currentPage: 1,
    };
  },
  computed: {
    ...mapState('movies', ['byId', 'totalPages']),
    movies() {
      return this.byId;
    },
    movieIds() {
      return Object.keys(this.movies);
    },
  },
  methods: {
    ...mapActions('movies', ['fetchMovies']),
    goToMovie(id) {
      this.$router.push({ name: 'MovieDetails', params: { id } });
    },
    handlePageChange(page) {
      console.log(page);
        this.currentPage = page;
        this.fetchMovies(page);
    },
  },
  created() {
    this.fetchMovies(this.currentPage);
  },
}
</script>
