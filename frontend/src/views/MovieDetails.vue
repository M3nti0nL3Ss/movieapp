<template>
    <div v-if="movie">
      <h1>
        <v-text-field v-if="isEditing" v-model="editedMovie.title" label="Title" />
        <span v-else>{{ movie.title }}</span>
      </h1>
      
      <v-rating 
        :value="editedMovie.average_rating" 
        :readonly="!isEditing" 
        half-increments
        v-if="!isEditing" 
      />
      <v-rating 
        v-if="isEditing"
        v-model="editedMovie.average_rating"
        half-increments
      />
      
      <p>
        <v-textarea 
          v-if="isEditing" 
          v-model="editedMovie.description" 
          label="Description"
        />
        <span v-else>{{ movie.description }}</span>
      </p>
      
      <h2>Actors</h2>
      <ul>
        <li v-for="actor in movie.actors" :key="actor.id">
          <v-text-field
            v-if="isEditing"
            v-model="actor.first_name"
            label="First Name"
            class="mr-2"
          />
          <v-text-field
            v-if="isEditing"
            v-model="actor.last_name"
            label="Last Name"
          />
          <span v-else>{{ actor.first_name }} {{ actor.last_name }}</span>
        </li>
      </ul>
      
      <h2>Reviews</h2>
      <v-list>
        <v-list-item v-for="review in movie.reviews" :key="review.id">
          <v-list-item-content>
            <v-list-item-title>Rating:</v-list-item-title>
            <v-list-item-subtitle>
              <v-text-field
                v-if="isEditing"
                v-model="review.grade"
                type="number"
                min="0"
                max="10"
              />
              <span v-else>{{ review.grade }}</span>
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      
      <v-btn @click="isEditing = !isEditing">
        {{ isEditing ? 'Save' : 'Edit' }}
      </v-btn>
  
      <v-btn v-if="!isEditing" @click="showAddReviewForm = true">Add Review</v-btn>
  
      <v-dialog v-model="showAddReviewForm" max-width="500px">
        <add-review :movie-id="movie.id" @review-added="onReviewAdded"></add-review>
      </v-dialog>
    </div>
  </template>
  
  <script>
  import { mapActions } from 'vuex';
  import AddReview from './AddReview.vue';
  
  export default {
    name: 'MovieDetails',
    components: {
      AddReview,
    },
    data: () => ({
      movie: null,
      showAddReviewForm: false,
      isEditing: false,
      editedMovie: {},
    }),
    methods: {
      ...mapActions('movies', ['fetchMovie', 'fetchReviews', 'updateMovie']),
      async loadMovie() {
        const id = this.$route.params.id;
        this.movie = await this.fetchMovie(id);
        this.movie.reviews = await this.fetchReviews(id);
        this.editedMovie = { ...this.movie }; // Initialize editedMovie with current movie data
      },
      async saveChanges() {
        const id = this.$route.params.id;
        await this.updateMovie(id,this.editedMovie);
        this.movie = { ...this.editedMovie }; // Update the original movie data
        this.isEditing = false;
      },
      onReviewAdded() {
        this.showAddReviewForm = false;
        this.loadMovie();
      },
    },
    created() {
      this.loadMovie();
    },
    watch: {
      isEditing(newVal) {
        if (!newVal) {
          this.saveChanges();
        }
      },
    },
  }
  </script>
  