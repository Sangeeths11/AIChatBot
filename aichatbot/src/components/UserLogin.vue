<template>
    <div class="login-container">
      <h1>Welcome</h1>
      <img src="@/assets/logo.png" alt="Profile Image" class="profile-img">
      <input type="text" placeholder="Username">
      <input type="password" placeholder="Password">
      <button>Login</button>
      <div class="helper-texts">
        <a href="#">Forgot Username / Password?</a>
        <a href="#">Don't have an account? Sign up</a>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserLogin'
  }
  </script>
  
  <style scoped>
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
    background-color: #4CAF50;
    color: white;
    border: none;
  }
  
  .helper-texts a {
    display: block;
    margin: 10px 0;
    text-decoration: none;
    color: #333;
  }
  </style>
  