<template>
  <div>
    <h1>Movies</h1>
    <v-row>
      <v-col v-for="movie in movies" :key="movie.id" cols="12" sm="6" md="4">
        <v-card @click="goToMovie(movie.id)">
          <v-card-title>{{ movie.title }}</v-card-title>
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
    ...mapState('movies', ['movies', 'totalPages']),
  },
  methods: {
    ...mapActions('movies', ['fetchMovies']),
    goToMovie(id) {
      this.$router.push({ name: 'MovieDetails', params: { id } });
    },
    handlePageChange(page) {
      console.log('Page changed to:', page); // Debug 
      //if (this.currentPage !== page) {
        this.currentPage = page;
        this.fetchMovies(page);
      //}
    }
  },
  created() {
    this.fetchMovies(this.currentPage);
  },
}
</script>
