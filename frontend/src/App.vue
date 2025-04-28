<template>
    <div class="app-container">
      <nav class="navbar">
        <h1 class="logo">业务需求分析系统</h1>
        <file-upload class="upload-btn" />
      </nav>
      
      <router-view />
    </div>
  </template>
  
  <script setup>
  import FileUpload from '@/components/FileUpload.vue'
  </script>
  
  <style lang="scss">
  .app-container {
    height: 100vh;
    display: flex;
    flex-direction: column;
  
    .navbar {
      padding: 1rem;
      background: #2c3e50;
      display: flex;
      justify-content: space-between;
      align-items: center;
  
      .logo {
        color: white;
        margin: 0;
      }
  
      .upload-btn {
        width: 200px;
      }
    }
  }
  </style>