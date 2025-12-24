<template>
  <div class="view-container">
    <button @click="$router.go(-1)" class="back-btn">
      <i class="bi bi-arrow-left"></i> 목록으로
    </button>

    <div v-if="store.article" class="content-wrapper animate-slide-up">
      <article class="article-paper">
        <div class="article-header">
          <h1 class="title">{{ store.article.title }}</h1>
          
          <div class="meta-row">
            <div class="author-section">
              <div class="avatar">
                <i class="bi bi-person-fill"></i>
              </div>
              <div class="info">
                <span class="name">{{ store.article.username || '익명' }}</span>
                <span class="time">{{ formatDate(store.article.created_at) }}</span>
              </div>
            </div>
            <div class="view-count">
              <i class="bi bi-eye"></i> {{ store.article.views || 0 }}
            </div>
          </div>
        </div>

        <div class="article-body">
          {{ store.article.content }}
        </div>

        <div class="action-area">
          <button 
            @click="onLikeClick(store.article.id)" 
            class="like-btn"
            :class="{ active: false }" 
          >
            <i class="bi bi-heart-fill"></i>
            <span>좋아요 {{ store.article.like_users?.length || 0 }}</span>
          </button>
        </div>
      </article>

      <section class="comment-section">
        <h3 class="section-title">댓글 <span class="count">{{ store.article.comments?.length || 0 }}</span></h3>

        <div class="comment-form">
          <form @submit.prevent="submitComment">
            <textarea 
              v-model="commentContent" 
              class="comment-input" 
              placeholder="FinMate님, 따뜻한 의견을 남겨주세요."
            ></textarea>
            <div class="form-footer">
              <button type="submit" class="submit-btn">등록</button>
            </div>
          </form>
        </div>

        <div class="comment-list">
          <div v-if="store.article.comments?.length > 0">
            <div v-for="comment in store.article.comments" :key="comment.id" class="comment-item">
              <div class="comment-avatar">
                {{ comment.username?.[0] || 'U' }}
              </div>
              <div class="comment-bubble">
                <div class="bubble-header">
                  <span class="c-user">{{ comment.username }}</span>
                  <span class="c-time">{{ formatDate(comment.created_at) }}</span>
                </div>
                <p class="c-content">{{ comment.content }}</p>
              </div>
            </div>
          </div>
          <div v-else class="empty-comment">
            <p>아직 댓글이 없습니다. 첫 번째 대화를 시작해보세요! 💬</p>
          </div>
        </div>
      </section>
    </div>

    <div v-else class="loading-state">
      <div class="spinner"></div>
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
  store.likeArticle(articleId)
}

onMounted(() => {
  store.getArticleDetail(route.params.id)
})

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return `${date.getFullYear()}. ${date.getMonth() + 1}. ${date.getDate()} ${date.getHours()}:${String(date.getMinutes()).padStart(2, '0')}`
}

const submitComment = () => {
  if (!commentContent.value.trim()) return
  store.createComment(route.params.id, commentContent.value)
  commentContent.value = ''
}
</script>

<style scoped>
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-slide-up { animation: slideUp 0.6s ease-out; }

.view-container { max-width: 900px; margin: 40px auto; padding: 0 20px; }

/* 뒤로가기 버튼 */
.back-btn { background: none; border: none; color: #666; font-weight: 600; margin-bottom: 20px; cursor: pointer; display: flex; align-items: center; gap: 8px; font-size: 1rem; padding: 0; }
.back-btn:hover { color: #2F65F6; text-decoration: underline; }

/* 본문 영역 */
.article-paper {
  background: white; border-radius: 24px; padding: 50px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.05); margin-bottom: 40px;
}
.article-header { border-bottom: 1px solid #f0f0f0; padding-bottom: 30px; margin-bottom: 40px; }
.title { font-size: 2rem; font-weight: 800; color: #333; margin-bottom: 25px; line-height: 1.3; }

.meta-row { display: flex; justify-content: space-between; align-items: flex-end; }
.author-section { display: flex; align-items: center; gap: 12px; }
.avatar { width: 48px; height: 48px; background: #eef4ff; color: #2F65F6; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; }
.info { display: flex; flex-direction: column; }
.name { font-weight: 700; color: #333; font-size: 1rem; }
.time { font-size: 0.85rem; color: #999; }
.view-count { color: #888; font-size: 0.9rem; }

.article-body {
  font-size: 1.1rem; line-height: 1.8; color: #444; white-space: pre-wrap; margin-bottom: 50px; min-height: 200px;
}

.action-area { text-align: center; }
.like-btn {
  background: white; border: 2px solid #ff6b6b; color: #ff6b6b;
  padding: 12px 30px; border-radius: 50px; font-weight: 700; font-size: 1rem;
  cursor: pointer; transition: all 0.2s; display: inline-flex; align-items: center; gap: 8px;
}
.like-btn:hover { background: #fff0f0; transform: scale(1.05); }
/* 좋아요 눌렀을 때 스타일 (필요시 class 바인딩) */
.like-btn.active { background: #ff6b6b; color: white; }

/* 댓글 섹션 */
.section-title { font-size: 1.3rem; font-weight: 800; color: #333; margin-bottom: 20px; }
.section-title .count { color: #2F65F6; }

.comment-form { margin-bottom: 40px; background: #f8f9fa; padding: 20px; border-radius: 20px; }
.comment-input {
  width: 100%; border: 1px solid #e9ecef; border-radius: 12px; padding: 15px;
  font-size: 0.95rem; outline: none; resize: none; min-height: 80px; margin-bottom: 10px;
}
.comment-input:focus { border-color: #2F65F6; background: white; }
.form-footer { display: flex; justify-content: flex-end; }
.submit-btn { background: #2F65F6; color: white; border: none; padding: 8px 25px; border-radius: 20px; font-weight: 700; cursor: pointer; transition: 0.2s; }
.submit-btn:hover { background: #1c50d8; }

.comment-list { display: flex; flex-direction: column; gap: 20px; }
.comment-item { display: flex; gap: 15px; }
.comment-avatar {
  width: 40px; height: 40px; background: #eee; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: 800; color: #777; font-size: 0.9rem; flex-shrink: 0;
}
.comment-bubble {
  background: white; border: 1px solid #f0f0f0; border-radius: 0 16px 16px 16px;
  padding: 15px 20px; flex-grow: 1; box-shadow: 0 2px 10px rgba(0,0,0,0.02);
}
.bubble-header { display: flex; justify-content: space-between; margin-bottom: 5px; }
.c-user { font-weight: 700; font-size: 0.9rem; color: #333; }
.c-time { font-size: 0.8rem; color: #aaa; }
.c-content { font-size: 0.95rem; color: #555; line-height: 1.5; margin: 0; }

.empty-comment { text-align: center; color: #999; padding: 30px; background: #fdfdfd; border-radius: 15px; border: 1px dashed #eee; }

.loading-state { text-align: center; padding: 100px 0; }
.spinner { width: 40px; height: 40px; border: 4px solid #f3f3f3; border-top: 4px solid #2F65F6; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>