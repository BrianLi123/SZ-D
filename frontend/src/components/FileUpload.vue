<template>
    <div class="file-upload">
      <input type="file" @change="handleFile" hidden ref="fileInput">
      <button @click="triggerUpload">上传业务文档</button>
      <span class="file-name">{{ fileName }}</span>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useChatStore } from '@/stores/chat'
  
  const fileInput = ref(null)
  const fileName = ref('')
  const chatStore = useChatStore()
  
  const triggerUpload = () => {
    fileInput.value.click()
  }
  
  const handleFile = async (e) => {
    const file = e.target.files[0]
    if (file) {
      fileName.value = file.name
      await chatStore.uploadDocument(file)
    }
  }
  </script>