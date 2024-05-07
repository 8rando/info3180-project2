<template>
  <div class="registration">
    <h1>Register</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="username">Username</label>
        <input v-model="formData.username" id="username" type="text" required>
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input v-model="formData.password" id="password" type="password" required>
      </div>
      <div class="form-group">
        <label for="firstname">First Name</label>
        <input v-model="formData.firstName" id="firstname" type="text" required>
      </div>
      <div class="form-group">
        <label for="lastname">Last Name</label>
        <input v-model="formData.lastName" id="lastname" type="text" required>
      </div>
      <div class="form-group">
        <label for="email">Email</label>
        <input v-model="formData.email" id="email" type="email" required>
      </div>
      <div class="form-group">
        <label for="location">Location</label>
        <input v-model="formData.location" id="location" type="text" required>
      </div>
      <div class="form-group">
        <label for="biography">Biography</label>
        <textarea v-model="formData.biography" id="biography"></textarea>
      </div>
      <div class="form-group">
        <label for="photo">Photo</label>
        <input id="photo" type="file" accept="image/jpeg,image/png" @change="handlePhotoUpload" required>
        <!-- Optional: display uploaded image -->
        <img :src="imageSrc" alt="Uploaded image preview">
      </div>
      <button type="submit" class="register-button">Register</button>
    </form>
  </div>
</template>

<script lang="ts">
export default {
  name: 'Register',
  data() {
    return {
      imageSrc: 'https://via.placeholder.com/350x550',
      formData: {
        username: '',
        password: '',
        firstName: '',
        lastName: '',
        email: '',
        location: '',
        biography: '',
        photo: null
      }
    };
  },
  methods: {
    handlePhotoUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.imageSrc = URL.createObjectURL(file);
        this.formData.photo = file;
      }
    },
    async submitForm() {
      const formData = new FormData();
      Object.keys(this.formData).forEach(key => {
        formData.append(key, this.formData[key]);
      });

      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/register', {
          method: 'POST',
          body: formData,
          headers: {
            // 'Content-Type': 'multipart/form-data' // not needed as FormData does it
          },
        });
        const result = await response.json();
        if (response.ok) {
          alert('Registration successful!');
          console.log(result);
        } else {
          console.error('Registration failed:', result);
          alert('Registration failed. See console for errors.');
        }
      } catch (error) {
        console.error('Error submitting form:', error);
      }
    }
  }
}
</script>

<style>
.registration {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"],
input[type="email"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.register-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #00cc00;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #009900;
}

img {
  margin-top: 10px;
  width: 100%; /* Adjust as needed */
  max-width: 350px; /* Adjust as needed */
}
</style>
