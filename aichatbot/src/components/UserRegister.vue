<template>
    <div class="register-container">
      <h1>Welcome to our Dashboard</h1>
      <img src="@/assets/logo.png" alt="Profile Image" class="profile-img">
      <input type="text" placeholder="Username">
      <input type="password" placeholder="Password">
      <input type="passwordConfirmation" placeholder="Password Confirmation">
      <button>Sign up</button>
      <div class="helper-texts">
        <router-link href="/UserLogin">Do you have an account? Log In</router-link>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserRegister'
  }
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
  