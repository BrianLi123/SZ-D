import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  const history = ref([])
  const isLoading = ref(false)
  
  async function sendMessage(payload) {
    isLoading.value = true
    try {
      const response = await fetch('/api/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
      
      const data = await response.json()
      history.value.push({
        role: 'user',
        content: payload.question
      }, {
        role: 'assistant',
        content: data.answer,
        sources: data.sources
      })
    } finally {
      isLoading.value = false
    }
  }
  
  return { history, isLoading, sendMessage }
})