<template>
  <div v-if="movie">
    <h1>
      <v-text-field v-if="isEditing" v-model="editedMovie.title" label="Title" />
      <span v-else>{{ movie.title }}</span>
    </h1>
    
    <v-rating 
      :value="editedMovie.grade" 
      :readonly="!isEditing" 
      half-increments
      v-if="!isEditing" 
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
          v-model="editedMovie.actors.find(a => a.id === actor.id).first_name"
          label="First Name"
          class="mr-2"
        />
        <v-text-field
          v-if="isEditing"
          v-model="editedMovie.actors.find(a => a.id === actor.id).last_name"
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
              max="5"
            />
            <span v-else>{{ review.grade }}</span>
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>

    <p>
      <strong>Average Grade:</strong> {{ movie.average_grade }}
    </p>
    
    <v-btn @click="toggleEdit">
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
    movie: { reviews: [] },
    showAddReviewForm: false,
    isEditing: false,
    editedMovie: {},
  }),
  computed: {
    averageRating() {
    if (this.movie && this.movie.reviews && this.movie.reviews.length > 0) {
      const total = this.movie.reviews.reduce((sum, review) => sum + review.grade, 0);
      return (total / this.movie.reviews.length).toFixed(1); 
    }
    return 'N/A';
  },
  },
  methods: {
    ...mapActions('movies', ['fetchMovie', 'fetchReviews', 'updateMovie']),
    async loadMovie() {
      const id = this.$route.params.id;
      this.movie = await this.fetchMovie(id);
      if (this.movie) {
        this.movie.reviews = await this.fetchReviews(id) || []; 
        this.editedMovie = JSON.parse(JSON.stringify(this.movie)); 
      }
    },
    async saveChanges() {
      const id = this.$route.params.id;
      await this.updateMovie({ movieId: id, editedMovie: this.editedMovie });
      this.movie = JSON.parse(JSON.stringify(this.editedMovie)); 
      this.isEditing = false;
    },
    toggleEdit() {
      if (this.isEditing) {
        this.saveChanges();
      } else {
        this.isEditing = true;
      }
    },
    onReviewAdded() {
      this.showAddReviewForm = false;
      this.loadMovie();
    },
  },
  created() {
    this.loadMovie();
  },
}
</script>
