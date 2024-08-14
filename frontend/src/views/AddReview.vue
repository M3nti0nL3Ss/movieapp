<template>
    <v-card>
      <v-card-title>Add Review</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="submitReview">
          <v-rating v-model="review.rating"></v-rating>
          <v-text-field
            v-model="review.grade"
            label="Grade"
            type="number"
            min="0"
            step="1"
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
        await this.addReview({ movieId: this.movieId, grade: this.review.grade });
        this.$emit('review-added');
      },
    },
  }
  </script>