import { createStore } from 'vuex'
import axios from 'axios'

axios.defaults.baseURL = process.env.VUE_APP_API_URL

export default createStore({
  modules: {
    movies: {
      namespaced: true,
      state: {
        movies: [],
        totalPages: 0,
      },
      mutations: {
        SET_MOVIES(state, movies) {
          state.movies = movies;
        },
        SET_TOTAL_PAGES(state, totalPages) {
          state.totalPages = totalPages;
        },
      },
      actions: {
        async fetchMovies({ commit }, page = 1) {
          console.log(page);
          try {
            const response = await axios.get(`/api/movies/?page=${page}`);
            commit('SET_MOVIES', response.data.results);
            commit('SET_TOTAL_PAGES', Math.ceil(response.data.count / response.data.results.length));
          } catch (error) {
            console.error('Error fetching movies:', error);
          }
        },
        async fetchMovie(_, id) {
          try {
            const response = await axios.get(`/api/movies/${id}/`);
            return response.data;
          } catch (error) {
            console.error('Error fetching movie details:', error);
          }
        },
        async fetchReviews(_, id) {
          try {
            const response = await axios.get(`/api/movies/${id}/reviews/`);
            return response.data.results;
          } catch (error) {
            console.error('Error fetching reviews:', error);
          }
        },
        async addReview(_, { movieId, grade }) {
          try {
            await axios.post(`/api/movies/${movieId}/reviews/`, { movie: movieId, grade: grade });
          } catch (error) {
            console.error('Error adding review:', error);
          }
        },
        async updateMovie(_, { movieId, editedMovie }) {
          try {
            await axios.put(`/api/movies/${movieId}/`, editedMovie);
          } catch (error) {
            console.error('Error editing movie:', error);
          }
        }
      },

    }
  }
})