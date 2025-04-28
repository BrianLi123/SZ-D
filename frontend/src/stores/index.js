import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', () => {
  const history = ref([])
  const isLoading = ref(false)
  const error = ref(null)

  async function uploadDocument(file) {
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await $http.post('/api/v1/documents', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      return response.data
    } catch (err) {
      error.value = err.message
      throw err
    }
  }

  return { history, isLoading, error, uploadDocument }
})