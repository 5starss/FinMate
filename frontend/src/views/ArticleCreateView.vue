<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm border-0">
          <div class="card-body p-4">
            <h3 class="fw-bold mb-4">새 게시글 작성</h3>
            
            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="title" class="form-label fw-bold">제목</label>
                <input 
                  type="text" 
                  id="title" 
                  v-model.trim="title" 
                  class="form-control form-control-lg" 
                  placeholder="제목을 입력하세요" 
                  required
                >
              </div>

              <div class="mb-4">
                <label for="content" class="form-label fw-bold">내용</label>
                <textarea 
                  id="content" 
                  v-model.trim="content" 
                  class="form-control" 
                  rows="10" 
                  placeholder="지출 절약 팁이나 가계부 고민을 나누어보세요!" 
                  required
                ></textarea>
              </div>

              <div class="d-flex gap-2 justify-content-end">
                <button 
                  type="button" 
                  @click="$router.go(-1)" 
                  class="btn btn-outline-secondary px-4 rounded-pill"
                >
                  취소
                </button>
                <button 
                  type="submit" 
                  class="btn btn-primary px-4 rounded-pill"
                >
                  등록하기
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useArticlesStore } from '@/stores/articles' // 스토어 이름 's' 확인
import { useRouter } from 'vue-router'

const store = useArticlesStore()
const router = useRouter() // router 객체 직접 사용을 위해 추가

const title = ref('')
const content = ref('')

const handleSubmit = () => {
  // 디버깅용: 버튼 클릭 시 콘솔에 찍히는지 확인
  console.log('등록 버튼 클릭됨')
  
  if (!title.value || !content.value) {
    alert('제목과 내용을 모두 입력해주세요.')
    return
  }

  const payload = {
    title: title.value,
    content: content.value
  }
  
  // 스토어의 createArticle 호출
  console.log('Payload 전송 시도:', payload)
  store.createArticle(payload)
}
</script>

<style scoped>
.form-control:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.1);
}
textarea {
  resize: none;
}
</style>