<template>
  <v-app>
    <v-app-bar app color="primary" dark @click="goHome">
    <v-toolbar-title>Movie App</v-toolbar-title>
  </v-app-bar>

    <v-main>
      <v-container>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data: () => ({
    //
  }),
  methods: {
    goHome() {
      this.$router.push('/'); // Navigates to the home page
    }
  }
}
</script>