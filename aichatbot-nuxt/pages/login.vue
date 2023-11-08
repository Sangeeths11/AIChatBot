<template>
    <div class="login-container">
      <h1 class="p-10">Welcome to our Dashboard</h1>
      <input type="text" placeholder="Username" v-model=loginName>
      <input type="password" placeholder="Password" v-model=loginPassword
      @keyup.enter="login"/>
      <button @click="login">Login</button>
      <div class="helper-texts">
        <router-link to="register">Don't have an account? Sign up</router-link>
      </div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</template>
  
<script lang="ts" setup>
  import { ref } from 'vue';
  import axios from 'axios';
  const router = useRouter();

  const loginName = ref('');
  const loginPassword = ref('');
  const errorMessage = ref(''); // Variable to hold the error message
  const baseUrl = 'http://127.0.0.1:5000/api'; // Replace with your actual base URL

  const login = async () => {
    try {
      const response = await axios.post(`${baseUrl}/login`, {
        name: loginName.value,
        password: loginPassword.value
      });
      const userID = response.data.userId;
      console.log(userID);
      router.push({ path: '/overview/' + userID});
      // Handle success - you can redirect or show a success message
    } catch (error) {
      errorMessage.value = 'An error occurred during login. Please try again later.';
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
.error-message {
    color: red;
    margin-top: 10px;
  }
</style>
  