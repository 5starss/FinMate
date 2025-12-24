import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useAccountStore } from './accounts'
import { useRouter } from 'vue-router'

export const useArticlesStore = defineStore('articles', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const articles = ref([])
  const article = ref(null)
  const accountStore = useAccountStore()
  const router = useRouter()

  // 1. 게시글 전체 목록 가져오기
  const getArticles = function () {
    axios({
      method: 'get',
      url: `${API_URL}/articles/`, // 백엔드 URL 패턴에 맞춰 수정하세요
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        articles.value = res.data
      })
      .catch((err) => console.log(err))
  }

  // 2. 게시글 상세 조회
  const getArticleDetail = function (articleId) {
    axios({
      method: 'get',
      url: `${API_URL}/articles/${articleId}/`,
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        article.value = res.data
      })
      .catch((err) => console.log(err))
  }
  

  // 3. 게시글 생성
  const createArticle = function (payload) {
    const { title, content } = payload
    axios({
      method: 'post',
      url: `${API_URL}/articles/`,
      data: { title, content },
      headers: {
        Authorization: `Token ${accountStore.token}`
      }
    })
      .then((res) => {
        router.push({ name: 'ArticleView' }) // 생성 후 목록 페이지로 이동
      })
      .catch((err) => console.log(err))
  }

  // 1. 댓글 생성 액션
const createComment = function (articleId, content) {
  axios({
    method: 'post',
    url: `${API_URL}/articles/${articleId}/comments/`, // articles 경로 반영
    data: { content },
    headers: { Authorization: `Token ${accountStore.token}` }
  })
    .then((res) => {
      // 댓글 작성 후 상세 데이터 새로고침
      getArticleDetail(articleId)
    })
    .catch((err) => console.log(err))
}

// 2. 좋아요 액션

const likeArticle = function (articleId) {
  console.log('2. 스토어 likeArticle 함수 진입. URL:', `${API_URL}/articles/${articleId}/like/`)
  
  axios({
    method: 'post',
    url: `${API_URL}/articles/${articleId}/like/`,
    headers: { Authorization: `Token ${accountStore.token}` }
  })
    .then((res) => {
      console.log('3. 서버 응답 성공:', res.status)
      getArticleDetail(articleId) // 상세 정보 갱신하여 하트 숫자 업데이트
    })
    .catch((err) => {
      console.error('4. 서버 응답 에러:', err.response)
    })
}

  return { 
    articles, 
    article, 
    getArticles, 
    getArticleDetail, 
    createArticle,
    createComment,
    likeArticle,
  }
})