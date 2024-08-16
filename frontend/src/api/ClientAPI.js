import axios from 'axios';

axios.defaults.baseURL = process.env.VUE_APP_API_URL;

class ClientAPI {
    static async fetchMovies(page = 1) {
        try {
            const response = await axios.get(`/api/movies/?page=${page}`);
            return response.data;
        } catch (error) {
            console.error('Error fetching movies:', error);
            throw error;
        }
    }

    static async fetchMovie(id) {
        try {
            const response = await axios.get(`/api/movies/${id}/`);
            return response.data;
        } catch (error) {
            console.error('Error fetching movie details:', error);
            throw error;
        }
    }

    static async fetchReviews(id) {
        try {
            const response = await axios.get(`/api/movies/${id}/reviews/`);
            return response.data.results;
        } catch (error) {
            console.error('Error fetching reviews:', error);
            throw error;
        }
    }

    static async addReview(movieId, grade) {
        try {
            await axios.post(`/api/movies/${movieId}/reviews/`, { movie: movieId, grade });
        } catch (error) {
            console.error('Error adding review:', error);
            throw error;
        }
    }

    static async updateMovie(movieId, editedMovie) {
        try {
            const response = await axios.put(`/api/movies/${movieId}/`, editedMovie);
            return response.data;
        } catch (error) {
            console.error('Error editing movie:', error);
            throw error;
        }
    }
}

export default ClientAPI;
