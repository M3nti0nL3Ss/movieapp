import { createStore } from 'vuex'
import axios from 'axios'

axios.defaults.baseURL = process.env.VUE_APP_API_URL

export default createStore({
  modules: {
    movies: {
      namespaced: true,
      state: {
        byId: {}, // gives { id: movie }
        allIds: [], // gives [id1, id2, ...]
        totalPages: 0,
      },
      mutations: {
        SET_MOVIES(state, movies) {
          // Normalize movies array into byId object
          state.byId = movies.reduce((acc, movie) => {
            acc[movie.id] = movie;
            return acc;
          }, {});

          // Store all IDs for pagination
          state.allIds = movies.map(movie => movie.id);
        },
        SET_TOTAL_PAGES(state, totalPages) {
          state.totalPages = totalPages;
        },
        ADD_MOVIE(state, movie) {
          state.byId[movie.id] = movie;
          if (!state.allIds.includes(movie.id)) {
            state.allIds.push(movie.id);
          }
        },
        UPDATE_MOVIE(state, updatedMovie) {
          state.byId[updatedMovie.id] = updatedMovie;
        },
      },
      actions: {
        async fetchMovies({ commit }, page = 1) {
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
        async updateMovie({ commit }, { movieId, editedMovie }) {
          try {
            const response = await axios.put(`/api/movies/${movieId}/`, editedMovie);
            commit('UPDATE_MOVIE', response.data);
          } catch (error) {
            console.error('Error editing movie:', error);
          }
        }
      },
    }
  }
})
