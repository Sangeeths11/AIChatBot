<template>
    <div class="login-container">
      <h1 class="p-10">Welcome to our Dashboard</h1>
      <input type="text" placeholder="Username" v-model=username>
      <input type="password" placeholder="Password" v-model=password>
      <button>Login</button>
      <div class="helper-texts">
        <router-link to="register">Don't have an account? Sign up</router-link>
      </div>
    </div>
</template>
  
<script lang="ts" setup>
  import { ref } from 'vue';
  import axios from 'axios';

  const username = ref('');
  const password = ref('');
  const baseUrl = 'http://example.com'; // Replace with your actual base URL

  const register = async () => {
    try {
      const response = await axios.post(`${baseUrl}/login`, {
        name: username.value,
        password: password.value,
      });
      console.log(response.data);
      // Handle success - you can redirect or show a success message
    } catch (error) {
      console.error(error);
      // Handle errors - you can show error messages to the user
    }
  };
</script>

<style scoped>

h1 {
  font-size: 30px;
  color: #4caf50;
}
.login-container {
  max-width: 400px;
  margin: 0 auto;
  text-align: center;
  padding: 20px;
}

.profile-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin: 20px 0;
}

input[type="text"], input[type="password"], button {
  display: block;
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  box-sizing: border-box;
}

button {
  background-color: #4caf50;
  color: white;
  border: none;
}

.helper-texts a {
  display: block;
  margin: 10px 0;
  text-decoration: none;
  color: #236925;
}
</style>
  