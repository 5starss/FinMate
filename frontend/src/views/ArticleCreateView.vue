<template>
  <div class="view-container">
    <div class="write-card animate-slide-up">
      <div class="card-header">
        <h2 class="title">새 게시글 작성 ✍️</h2>
        <p class="subtitle">나누고 싶은 이야기를 자유롭게 적어주세요.</p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="title" class="label">제목</label>
          <input 
            type="text" 
            id="title" 
            v-model.trim="title" 
            class="custom-input title-input" 
            placeholder="제목을 입력하세요" 
            required
          >
        </div>

        <div class="form-group">
          <label for="content" class="label">내용</label>
          <textarea 
            id="content" 
            v-model.trim="content" 
            class="custom-input content-input" 
            rows="12" 
            placeholder="내용을 입력하세요. (예: 저축 꿀팁, 상품 후기 등)" 
            required
          ></textarea>
        </div>

        <div class="btn-group">
          <button type="button" @click="$router.go(-1)" class="cancel-btn">
            취소
          </button>
          <button type="submit" class="submit-btn">
            게시글 등록
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useArticlesStore } from '@/stores/articles'
import { useRouter } from 'vue-router'

const store = useArticlesStore()
const router = useRouter()

const title = ref('')
const content = ref('')

const handleSubmit = () => {
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  const payload = {
    title: title.value,
    content: content.value
  }
  
  store.createArticle(payload)
}
</script>

<style scoped>
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
.animate-slide-up { animation: slideUp 0.6s ease-out; }

.view-container {
  max-width: 800px; margin: 50px auto; padding: 0 20px;
}

.write-card {
  background: white; border-radius: 30px; padding: 50px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.05);
}

.card-header { text-align: center; margin-bottom: 40px; }
.title { font-size: 2rem; font-weight: 800; color: #333; margin-bottom: 10px; }
.subtitle { color: #666; }

.form-group { margin-bottom: 25px; }
.label { display: block; font-weight: 700; color: #444; margin-bottom: 8px; font-size: 0.95rem; }

.custom-input {
  width: 100%; padding: 16px 20px; border-radius: 12px;
  border: 1px solid #e0e0e0; background: #fcfcfc;
  font-size: 1rem; color: #333; outline: none; transition: all 0.2s;
}
.title-input { font-weight: 700; }
.content-input { resize: none; line-height: 1.6; }

.custom-input:focus {
  border-color: #2F65F6; background: white;
  box-shadow: 0 0 0 4px rgba(47, 101, 246, 0.1);
}
.custom-input::placeholder { color: #aaa; font-weight: 400; }

.btn-group {
  display: flex; gap: 15px; margin-top: 40px; justify-content: center;
}
.cancel-btn, .submit-btn {
  padding: 15px 40px; border-radius: 50px; font-weight: 700; font-size: 1.05rem;
  cursor: pointer; transition: all 0.2s; border: none;
}
.cancel-btn { background: #f1f3f5; color: #666; }
.cancel-btn:hover { background: #e9ecef; }

.submit-btn { background: #2F65F6; color: white; box-shadow: 0 5px 20px rgba(47, 101, 246, 0.3); }
.submit-btn:hover { background: #1c50d8; transform: translateY(-2px); }

@media (max-width: 600px) {
  .write-card { padding: 30px 20px; }
  .title { font-size: 1.5rem; }
  .btn-group { flex-direction: column; }
  .cancel-btn, .submit-btn { width: 100%; }
}
</style>