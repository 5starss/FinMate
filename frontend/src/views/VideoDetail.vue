<template>
    <div v-if="loading">영상 정보를 불러오는 중입니다...</div>
    
    <div v-else-if="video" class="detail-container">
      <button @click="$router.back()" style="margin-bottom: 20px;">
        &lt; 뒤로가기
      </button>
  
      <div class="video-wrapper">
        <iframe 
          width="100%" 
          height="500" 
          :src="videoUrl" 
          title="YouTube video player" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen
        ></iframe>
      </div>
  
      <div class="video-info" style="margin-top: 20px;">
        <h2>{{ video.snippet.title }}</h2>
        <p style="font-weight: bold; color: #555;">
          {{ video.snippet.channelTitle }} · {{ publishedDate }}
        </p>
        <hr>
        <div class="description">
          <p style="white-space: pre-wrap;">{{ video.snippet.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const video = ref(null)
  const loading = ref(true)
  
  const videoId = route.params.id
  
  const videoUrl = computed(() => {
    return `https://www.youtube.com/embed/${videoId}`
  })
  
  const publishedDate = computed(() => {
    if (!video.value) return ''
    const date = new Date(video.value.snippet.publishedAt)
    return date.toISOString().split('T')[0]
  })
  
  const fetchVideoDetail = async () => {
    const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
    const API_URL = 'https://www.googleapis.com/youtube/v3/videos'
  
    try {
      const response = await axios.get(API_URL, {
        params: {
          key: API_KEY,
          part: 'snippet',
          id: videoId
        }
      })
      
      video.value = response.data.items[0]
      console.log('상세 정보:', video.value)
    } catch (error) {
      console.error(error)
      alert('영상 정보를 가져오지 못했습니다.')
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    fetchVideoDetail()
  })
  </script>
  
  <style scoped>

  </style>