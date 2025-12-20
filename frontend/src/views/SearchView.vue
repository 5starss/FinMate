<template>
    <div>
      <h2>비디오 검색</h2>
      
      <div style="margin-bottom: 20px;">
        <input 
          v-model="keyword" 
          @keyup.enter="onSearch"
          type="text" 
          placeholder="검색어를 입력하세요"
          style="padding: 5px; width: 200px;"
        >
        <button @click="onSearch" style="padding: 5px 10px;">검색</button>
      </div>
  
      <div v-if="loading">잠시만 기다려주세요...</div>
      
      <div v-else class="video-list">
        <div v-if="videos.length === 0 && searched">
          검색 결과가 없습니다. 다른 검색어를 입력해보세요.
        </div>
  
        <div 
          v-for="video in videos" 
          :key="video.id.videoId" 
          class="video-card"
          @click="goToDetail(video.id.videoId)"
        >
          <img :src="video.snippet.thumbnails.medium.url" alt="thumbnail" style="width: 100%; border-radius: 8px;">
          <div class="info">
            <h4 style="margin: 10px 0 5px;">{{ video.snippet.title }}</h4>
            <p style="color: gray;">{{ video.snippet.channelTitle }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  
  const route = useRoute()
  const router = useRouter()
  
  const keyword = ref('') 
  const videos = ref([])   
  const loading = ref(false)
  const searched = ref(false) 
  
  const API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY
  const API_URL = 'https://www.googleapis.com/youtube/v3/search'

  const goToDetail = (videoId) => {
    if (videoId) {
        router.push({ 
        name: 'detail', 
        params: { id: videoId } 
        })
    } else {
        console.error('비디오 ID가 없습니다.')
    }
  }
  
  const onSearch = () => {
    if (keyword.value.trim()) {
      router.push({ query: { q: keyword.value } })
    }
  }
  
  const fetchVideos = async (query) => {
    if (!query) return
  
    loading.value = true
    searched.value = true
    
    try {
      const response = await axios.get(API_URL, {
        params: {
          key: API_KEY,
          part: 'snippet',
          q: query,
          type: 'video',
          maxResults: 12
        }
      })
      videos.value = response.data.items
    } catch (error) {
      console.error(error)
      alert('API 호출 횟수 초과 혹은 에러 발생!')
    } finally {
      loading.value = false
    }
  }
  
  onMounted(() => {
    const query = route.query.q
    if (query) {
      keyword.value = query 
      fetchVideos(query)
    }
  })
  
  watch(() => route.query.q, (newQuery) => {
    if (newQuery) {
      fetchVideos(newQuery)
    }
  })
  </script>
  
  <style scoped>
  </style>