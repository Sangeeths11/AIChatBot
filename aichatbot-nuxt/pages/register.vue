<template>
    <div class="register-container">
      <h1>Welcome to our Dashboard</h1>
      <label class="label">
        <span class="label-text">Upload your Profile</span>
      </label>
      <input type="text" placeholder="Type here" class="input input-bordered input-success w-full" />
      <label class="label">
        <span class="label-text">Username:</span>
      </label>
      <input type="text" placeholder="Type here" class="input input-bordered input-success w-full" />
      
      <label class="label">
        <span class="label-text">Password:</span>
      </label>
      <input type="password" placeholder="Type here" class="input input-bordered input-success w-full" />
      <input type="password" placeholder="Type here again" class="input input-bordered input-success w-full" />
      <button>Sign up</button>
      <div class="helper-texts">
        <router-link to="login">Do you have an account? Log in</router-link>
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
  </style>
  