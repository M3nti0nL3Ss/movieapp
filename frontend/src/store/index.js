// src/store/index.js
import { createStore } from 'vuex';
import ClientAPI from '@/api/ClientAPI';

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
            const data = await ClientAPI.fetchMovies(page);
            commit('SET_MOVIES', data.results);
            commit('SET_TOTAL_PAGES', Math.ceil(data.count / data.results.length));
          } catch (error) {
            console.error('Error fetching movies:', error);
          }
        },
        async fetchMovie(_, id) {
          try {
            return await ClientAPI.fetchMovie(id);
          } catch (error) {
            console.error('Error fetching movie details:', error);
          }
        },
        async fetchReviews(_, id) {
          try {
            return await ClientAPI.fetchReviews(id);
          } catch (error) {
            console.error('Error fetching reviews:', error);
          }
        },
        async addReview(_, { movieId, grade }) {
          try {
            await ClientAPI.addReview(movieId, grade);
          } catch (error) {
            console.error('Error adding review:', error);
          }
        },
        async updateMovie({ commit }, { movieId, editedMovie }) {
          try {
            const updatedMovie = await ClientAPI.updateMovie(movieId, editedMovie);
            commit('UPDATE_MOVIE', updatedMovie);
          } catch (error) {
            console.error('Error editing movie:', error);
          }
        }
      },
    }
  }
});
