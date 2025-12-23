<template>
  <div class="detail-page">
    <div v-if="loading" class="status-msg">영상 정보를 불러오는 중입니다...</div>
    
    <div v-else-if="video" class="content-wrapper">
      <div class="nav-area">
        <button @click="$router.back()" class="back-btn">
          &larr; 목록으로 돌아가기
        </button>
      </div>
  
      <div class="video-container">
        <iframe 
          class="responsive-iframe"
          :src="videoUrl" 
          title="YouTube video player" 
          frameborder="0" 
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
          allowfullscreen
        ></iframe>
      </div>
  
      <div class="video-info">
        <h2 class="video-title" v-html="video.snippet.title"></h2>
        
        <div class="video-meta">
          <span class="channel-name">{{ video.snippet.channelTitle }}</span>
          <span class="upload-date">{{ publishedDate }}</span>
        </div>
        
        <div class="description-box">
          <p class="description-text">{{ video.snippet.description }}</p>
        </div>
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
.detail-page {
  padding: 40px 20px;
  background-color: white; 
  min-height: 100vh;
}

.content-wrapper {
  max-width: 1000px; /* 너무 넓어지지 않게 제한 */
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.nav-area {
  margin-bottom: 20px;
}

.back-btn {
  background: none;
  border: none;
  color: #666;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0;
  font-weight: 600;
}

.back-btn:hover {
  color: #2F65F6;
  text-decoration: underline;
}

/* 반응형 비디오 컨테이너 */
.video-container {
  position: relative;
  width: 100%;
  /* 16:9 비율 유지 */
  padding-bottom: 56.25%; 
  background: #000;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 30px;
}

.responsive-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.video-info {
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.video-title {
  font-size: 24px;
  font-weight: 800;
  color: #111;
  margin-bottom: 10px;
  line-height: 1.3;
}

.video-meta {
  display: flex;
  gap: 12px;
  color: #666;
  font-size: 14px;
  margin-bottom: 24px;
}

.channel-name {
  font-weight: 700;
  color: #333;
}

.description-box {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  color: #333;
}

.description-text {
  white-space: pre-wrap; /* 줄바꿈 유지 */
  font-size: 15px;
  line-height: 1.6;
  color: #444;
  margin: 0;
}

.status-msg {
  text-align: center;
  margin-top: 100px;
  font-size: 18px;
  color: #666;
}
</style>