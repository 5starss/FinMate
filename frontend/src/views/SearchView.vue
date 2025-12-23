<template>
  <div class="search-container">
    <h2 class="page-title">관심 종목 관련 영상 검색</h2>
    
    <div class="search-bar-wrapper">
      <div class="search-input-group">
        <input 
          v-model="keyword" 
          @keyup.enter="onSearch"
          type="text" 
          class="search-input"
          placeholder="검색어를 입력하세요"
        >
        <button @click="onSearch" class="search-btn">검색</button>
      </div>
    </div>

    <div v-if="loading" class="loading-msg">잠시만 기다려주세요...</div>
    
    <div v-else class="video-list-section">
      <div v-if="videos.length === 0 && searched" class="no-result">
        검색 결과가 없습니다. 다른 검색어를 입력해보세요.
      </div>

      <div class="video-grid">
        <div 
          v-for="video in videos" 
          :key="video.id.videoId" 
          class="video-card"
          @click="goToDetail(video.id.videoId)"
        >
          <div class="thumbnail-wrapper">
            <img :src="video.snippet.thumbnails.medium.url" alt="thumbnail">
          </div>
          <div class="info">
            <h4 class="video-title" v-html="video.snippet.title"></h4>
            <p class="channel-name">{{ video.snippet.channelTitle }}</p>
          </div>
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
.search-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  font-weight: 800;
  color: #333;
}

/* 검색창 스타일 */
.search-bar-wrapper {
  display: flex;
  justify-content: center;
  margin-bottom: 40px;
}

.search-input-group {
  display: flex;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border-radius: 50px;
  overflow: hidden;
  border: 1px solid #ddd;
}

.search-input {
  width: 300px;
  padding: 12px 20px;
  border: none;
  outline: none;
  font-size: 16px;
}

.search-btn {
  background-color: #2F65F6; /* 헤더와 깔맞춤 */
  color: white;
  border: none;
  padding: 0 24px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.search-btn:hover {
  background-color: #1a4cd2;
}

/* 그리드 레이아웃 */
.video-grid {
  display: grid;
  /* 반응형: 화면 크기에 따라 열 개수 자동 조절 (최소 260px) */
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 24px;
}

.video-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.video-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.12);
}

.thumbnail-wrapper {
  width: 100%;
  aspect-ratio: 16 / 9; /* 썸네일 비율 고정 */
  overflow: hidden;
}

.thumbnail-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.info {
  padding: 16px;
}

.video-title {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 8px 0;
  line-height: 1.4;
  color: #333;
  
  /* 2줄 이상 넘어가면 ... 처리 */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.channel-name {
  font-size: 14px;
  color: #888;
  margin: 0;
}

.loading-msg, .no-result {
  text-align: center;
  color: #666;
  margin-top: 50px;
}
</style>