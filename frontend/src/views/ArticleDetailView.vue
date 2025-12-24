<template>
  <div class="container mt-4 pb-5">
    <button @click="$router.go(-1)" class="btn btn-link text-muted p-0 mb-3 text-decoration-none">
      <i class="bi bi-arrow-left"></i> 목록으로 돌아가기
    </button>

    <div v-if="store.article" class="row justify-content-center">
      <div class="col-lg-9">
        <div class="card shadow-sm border-0 mb-4">
          <div class="card-body p-4">
            <h2 class="fw-bold mb-3">{{ store.article.title }}</h2>
            
            <div class="d-flex align-items-center justify-content-between mb-4 pb-3 border-bottom">
              <div class="d-flex align-items-center">
                <div class="bg-primary-subtle rounded-circle p-2 me-2">
                  <i class="bi bi-person-fill text-primary"></i>
                </div>
                <div>
                  <div class="fw-bold">{{ store.article.username || '익명' }}</div>
                  <small class="text-muted">{{ formatDate(store.article.created_at) }}</small>
                </div>
              </div>
              <div class="text-muted small">
                <i class="bi bi-eye me-1"></i> 조회수 {{ store.article.views || 0 }}
              </div>
            </div>

            <div class="article-content mb-5" style="white-space: pre-wrap; line-height: 1.8;">
              {{ store.article.content }}
            </div>
              
            <div class="text-center">
              <button 
                @click="onLikeClick(store.article.id)" 
                class="btn btn-outline-danger rounded-pill px-4"
              >
                <i class="bi bi-heart-fill me-2"></i> 
                좋아요 {{ store.article.like_users?.length || 0 }}
              </button>
            </div>
          </div>
        </div>

        <div class="comments-section">
          <h5 class="fw-bold mb-3">댓글 <span class="text-primary">{{ store.article.comments?.length || 0 }}</span></h5>
          
          <div class="card border-0 shadow-sm mb-4">
            <div class="card-body p-3">
              <form @submit.prevent="submitComment">
                <textarea 
                  v-model="commentContent" 
                  class="form-control border-0 bg-light mb-2" 
                  rows="2" 
                  placeholder="따뜻한 댓글을 남겨주세요."
                ></textarea>
                <div class="d-flex justify-content-end">
                  <button type="submit" class="btn btn-primary btn-sm px-3 rounded-pill">등록</button>
                </div>
              </form>
            </div>
          </div>

          <div v-if="store.article.comments?.length > 0">
            <div v-for="comment in store.article.comments" :key="comment.id" class="mb-3 ps-2 border-start border-3 border-light">
              <div class="d-flex justify-content-between align-items-start">
                <div class="fw-bold small">{{ comment.username }}</div>
                <small class="text-muted" style="font-size: 0.75rem;">{{ formatDate(comment.created_at) }}</small>
              </div>
              <p class="mb-1 small">{{ comment.content }}</p>
            </div>
          </div>
          <div v-else class="text-center py-4 text-muted small">
            첫 번째 댓글을 남겨보세요!
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
  
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'

const store = useArticlesStore()
const route = useRoute()
const commentContent = ref('')
const onLikeClick = (articleId) => {
  console.log('1. 좋아요 버튼 클릭됨! 게시글 ID:', articleId)
  store.likeArticle(articleId)
}

onMounted(() => {
  store.getArticleDetail(route.params.id)
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()} ${date.getHours()}:${date.getMinutes()}`
}

const submitComment = () => {
  if (!commentContent.value.trim()) return
  store.createComment(route.params.id, commentContent.value)
  commentContent.value = ''
}
</script>

<style scoped>
.article-content {
  min-height: 200px;
  font-size: 1.1rem;
}
</style>