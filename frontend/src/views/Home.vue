<template>
  <div>
    <h1>Movies</h1>
    <v-row>
      <v-col v-for="id in movieIds" :key="id" cols="12" sm="6" md="4">
        <v-card @click="goToMovie(id)">
          <v-card-title>{{ movies[id].title }}</v-card-title>
        </v-card>
      </v-col>
    </v-row>
    <v-pagination
      v-model="currentPage"
      :length="totalPages"
      @input="handlePageChange"
    ></v-pagination>
  </div>
</template>

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
      if (this.currentPage !== page) {
        this.currentPage = page;
        this.fetchMovies(page);
      }
    },
  },
  created() {
    this.fetchMovies(this.currentPage);
  },
}
</script>
