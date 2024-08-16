<template>
  <v-card>
    <v-card-title>Add Review</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="submitReview">
        <v-rating v-model="review.rating"></v-rating>
        <v-text-field
          v-model.number="review.grade"
          label="Grade"
          type="number"
          min="0"
          max="5"
          step="1"
          :rules="[value => value >= 0 && value <= 5 || 'Grade must be between 0 and 5']"
        ></v-text-field>
        <v-btn type="submit" color="primary">Submit</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'AddReview',
  props: ['movieId'],
  data: () => ({
    review: {
      grade: 0,
    },
  }),
  methods: {
    ...mapActions('movies', ['addReview']),
    async submitReview() {
      if (this.review.grade < 0 || this.review.grade > 5) {
        alert('Grade must be between 0 and 5');
        return;
      }
      await this.addReview({ movieId: this.movieId, grade: this.review.grade });
      this.$emit('review-added');
    },
  },
}
</script>
