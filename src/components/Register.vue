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
        <img :src="imageSrc" alt="Uploaded image preview">
      </div>
      <button type="submit" class="register-button">Register</button>
    </form>
  </div>
</template>

<script lang="ts">
import { getCsrfToken } from '../services/cstfService';

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
      const csrfToken = getCsrfToken();
      // console.log(csrfToken)
      const formData = { ...this.formData };
      delete formData.photo; // Remove photo from JSON data

      // Convert image file to Base64
      const photoFile = this.formData.photo;
      const base64Photo = await this.convertToBase64(photoFile);
      formData.photo = base64Photo;

      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': csrfToken,
          },
          body: JSON.stringify(formData),
          credentials: 'include'  // Ensure cookies are included
        });

        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
          const result = await response.json();
          if (response.ok) {
            alert('Registration successful!');
            console.log(result);
          } else {
            console.error('Registration failed:', result);
            alert('Registration failed. See console for errors.');
          }
        } else {
          console.error('Unexpected non-JSON response:', await response.text());
          alert('An error occurred. Please check the console for details.');
        }
      } catch (error) {
        console.error('Error submitting form:', error);
      }
    },
    convertToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
      });
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
