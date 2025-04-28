<template>
  <div class="chat-container">
    <div class="message-history">
      <div v-for="(msg, index) in history" :key="index" 
           :class="['message', msg.role]">
        <div class="content">{{ msg.content }}</div>
        <div v-if="msg.sources" class="sources">
          来源文档: {{ msg.sources.join(', ') }}
        </div>
      </div>
    </div>
    
    <div class="input-area">
      <FileUpload @file-uploaded="handleFileUpload" />
      <input v-model="inputText" @keyup.enter="sendMessage" />
      <button @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/stores/chat'

const chatStore = useChatStore()
const inputText = ref('')

const sendMessage = async () => {
  if (!inputText.value.trim()) return
  
  await chatStore.sendMessage({
    question: inputText.value,
    history: chatStore.history
  })
  
  inputText.value = ''
}

const handleFileUpload = (file) => {
  chatStore.uploadDocument(file)
}
</script>