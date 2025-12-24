<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold mb-0">
        <i class="bi bi-chat-dots text-primary"></i> 커뮤니티
      </h2>
      <RouterLink :to="{ name: 'ArticleCreateView' }" class="btn btn-primary rounded-pill px-4">
        <i class="bi bi-pencil-fill me-1"></i> 글쓰기
      </RouterLink>
    </div>

    <div v-if="store.articles.length > 0" class="row g-4">
      <div v-for="article in store.articles" :key="article.id" class="col-md-6 col-lg-4">
        <div class="card h-100 border-0 shadow-sm hover-card" @click="goDetail(article.id)">
          <div class="card-body p-4">
            <div class="d-flex align-items-center mb-3">
              <div class="bg-secondary-subtle rounded-circle p-2 me-2">
                <i class="bi bi-person text-secondary"></i>
              </div>
              <div>
                <h6 class="mb-0 fw-bold">{{ article.username || '익명' }}</h6>
                <small class="text-muted">{{ formatDate(article.created_at) }}</small>
              </div>
            </div>
            
            <h5 class="card-title fw-bold text-truncate">{{ article.title }}</h5>
            <p class="card-text text-muted text-overflow-3">
              {{ article.content }}
            </p>
          </div>
          <div class="card-footer bg-white border-top-0 p-4 pt-0 d-flex gap-3 text-muted small">
            <span><i class="bi bi-heart me-1"></i> {{ article.like_users?.length || 0 }}</span>
            <span><i class="bi bi-chat-left-text me-1"></i> {{ article.comment_count || 0 }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5 my-5 text-muted">
      <i class="bi bi-journal-x fs-1 opacity-25"></i>
      <p class="mt-3">아직 등록된 게시글이 없습니다.<br>첫 번째 이야기를 들려주세요!</p>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useArticlesStore } from '@/stores/articles'
import { useRouter } from 'vue-router'

const store = useArticlesStore()
const router = useRouter()

onMounted(() => {
  store.getArticles()
})

const goDetail = (id) => {
  router.push({ name: 'ArticleDetailView', params: { id: id } })
}

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`
}
</script>

<style scoped>
.hover-card {
  transition: transform 0.2s ease, shadow 0.2s ease;
  cursor: pointer;
}
.hover-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,.1) !important;
}
.text-overflow-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>