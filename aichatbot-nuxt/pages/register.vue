<template>
    <div class="header-logo"/>
    <div class="register-container">
      <h1>Welcome to our Dashboard</h1>
      <label class="label">
        <span class="label-text">Username:</span>
      </label>
      <input type="text" placeholder="Type here" class="input input-bordered  w-full" v-model="username"/>
      
      <label class="label">
        <span class="label-text">Password:</span>
      </label>
      <input type="password" placeholder="Type here" class="input input-bordered  w-full" v-model="password"/>
      <input type="password" placeholder="Type here again" class="input input-bordered w-full" v-model="passwordConfirmation"
      @keyup.enter="register"/>
      <button @click="register">Sign up</button>
      <div class="helper-texts">
        <router-link to="login">Do you have an account? Log in</router-link>
      </div>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </div>
</template>
  
<script lang="ts" setup>
  import { ref } from 'vue';
  import axios from 'axios';
  const router = useRouter();

  const username = ref('');
  const password = ref('');
  const passwordConfirmation = ref('');
  const baseUrl = 'http://127.0.0.1:5000/api'; // Replace with your actual base URL
  const errorMessage = ref(''); // Variable to hold the error message 

  const register = async () => {
    try {
      const response = await axios.post(`${baseUrl}/register`, {
        name: username.value,
        password: password.value,
        passwordConfirmation: passwordConfirmation.value
      });
      console.log(response.data);
      // Handle success - you can redirect or show a success message
      router.push('/login');

    } catch (error) {
      console.error(error);
      // Handle errors - you can show error messages to the user
      errorMessage.value = 'An error occurred during registration. Please try again later.';
    }
  };

</script>

<style scoped>
  h1 {
    font-size: 30px;
    color: #4caf50;
  }
  .register-container{
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

  input[type="text"], input[type="password"], input[type="passwordConfirmation"], button {
    display: block;
    width: 100%;
    margin: 10px 0;
    padding: 10px;
    border-radius: 5px;
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
  