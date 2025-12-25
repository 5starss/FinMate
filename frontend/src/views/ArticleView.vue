<template>
  <div class="view-container">
    <div class="header-section animate-fade-in">
      <div class="text-content">
        <span class="badge">Community 💬</span>
        <h1 class="page-title">자유 게시판</h1>
        <p class="subtitle">금융 꿀팁부터 소소한 일상까지, FinMate들과 이야기 나눠보세요.</p>
      </div>
      <button @click="router.push({ name: 'ArticleCreateView' })" class="write-btn">
        <i class="bi bi-pencil-fill me-2"></i> 새 글 쓰기
      </button>
    </div>

    <div v-if="store.articles.length > 0" class="article-grid animate-slide-up">
      <div 
        v-for="article in store.articles" 
        :key="article.id" 
        class="article-card" 
        @click="goDetail(article.id)"
      >
        <div class="card-body">
          <div class="meta-top">
            <div class="author-info">
              <div class="avatar-circle">
                <img 
                  v-if="article.user_image" 
                  :src="getImageUrl(article.user_image)" 
                  class="profile-img" 
                  alt="프로필" 
                />
                <i v-else class="bi bi-person-fill"></i>
              </div>
              <div class="text-info">
                <span class="username">{{ article.user_nickname || '익명' }}</span>
                <span class="date">{{ formatDate(article.created_at) }}</span>
              </div>
            </div>
          </div>
          
          <h3 class="article-title">{{ article.title }}</h3>
          <p class="article-preview">{{ article.content }}</p>
        </div>

        <div class="card-footer">
          <div class="stats">
            <span class="stat-item heart">
              <i class="bi bi-heart-fill"></i> {{ article.like_users?.length || 0 }}
            </span>
            <span class="stat-item comment">
              <i class="bi bi-chat-dots-fill"></i> {{ article.comment_count || 0 }}
            </span>
          </div>
          <span class="read-more">더 읽기 <i class="bi bi-arrow-right"></i></span>
        </div>
      </div>
    </div>

    <div v-else class="empty-state animate-slide-up">
      <div class="icon-box">📝</div>
      <h3>아직 등록된 글이 없어요.</h3>
      <p>첫 번째 게시글의 주인공이 되어보세요!</p>
      <button @click="router.push({ name: 'ArticleCreateView' })" class="write-btn small">
        첫 글 작성하기
      </button>
    </div>
  </div>
</template>

<script setup>
  import { onMounted } from 'vue'
  import { useArticlesStore } from '@/stores/articles'
  import { useRouter } from 'vue-router'
  import { useAccountStore } from '@/stores/accounts' // API URL 가져오기 위해 추가
  
  const store = useArticlesStore()
  const accountStore = useAccountStore()
  const router = useRouter()
  
  onMounted(() => {
    store.getArticles()
  })
  
  const goDetail = (id) => {
    router.push({ name: 'ArticleDetailView', params: { id: id } })
  }
  
  const formatDate = (dateStr) => {
    if (!dateStr) return ''
    const date = new Date(dateStr)
    return `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()}`
  }
  
  // [추가] 이미지 URL 처리 함수
  const getImageUrl = (path) => {
    if (!path) return ''
    if (path.startsWith('http')) return path
    return `${accountStore.API_URL}${path}`
  }
  </script>

<style scoped>
  /* [필수] 박스 크기 기준 통일 */
  * { box-sizing: border-box; }
  
  /* 애니메이션 */
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  
  .animate-fade-in { animation: fadeIn 0.8s ease-out; }
  .animate-slide-up { animation: slideUp 0.8s ease-out forwards; opacity: 0; }
  
  .view-container {
    /* [핵심 수정] 픽셀 고정이 아니라 화면 비율로 설정 */
    width: 90%;        /* 화면의 96%를 사용하여 꽉 차게 만듭니다 */
    max-width: none;   /* 최대 너비 제한을 해제합니다 */
    margin: 40px auto; /* 중앙 정렬 */
    padding: 0 10px;   /* 좌우 내부 여백을 줄여 콘텐츠 공간 확보 */
    min-height: 800px;
  }
  
  .header-section {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 1px solid #eee;
  }
  .text-content {
    flex: 1;
  }
  .badge { background: #eef4ff; color: #2F65F6; padding: 6px 12px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; margin-bottom: 10px; display: inline-block; }
  .page-title { font-size: 2.2rem; font-weight: 800; color: #333; margin-bottom: 10px; }
  .subtitle { color: #666; font-size: 1.1rem; }
  
  .write-btn {
    background: #2F65F6; color: white; border: none; padding: 12px 25px;
    border-radius: 12px; font-weight: 700; font-size: 1rem; cursor: pointer;
    transition: all 0.2s; box-shadow: 0 4px 15px rgba(47, 101, 246, 0.3);
    display: flex; align-items: center; white-space: nowrap; /* 버튼 텍스트 줄바꿈 방지 */
  }
  .write-btn:hover { background: #1c50d8; transform: translateY(-2px); }
  .write-btn.small { padding: 10px 20px; font-size: 0.95rem; margin-top: 20px; }
  
  /* 게시글 그리드 */
  .article-grid {
    display: grid;
    /* 카드가 너무 작아지지 않도록 최소 너비를 350px로 설정하고 화면 꽉 채움 */
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 30px; /* 카드 사이 간격 */
  }
  
  .article-card {
    background: white;
    border-radius: 20px;
    border: 1px solid #f0f0f0;
    overflow: hidden;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 5px 15px rgba(0,0,0,0.03); /* 기본 그림자 추가 */
  }
  .article-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    border-color: #2F65F6; /* 호버 시 테두리 포인트 */
  }
  
  .card-body { padding: 30px; /* 내부 여백 시원하게 */ }
  
  .meta-top { margin-bottom: 15px; }
  .author-info { display: flex; align-items: center; gap: 10px; }

  
  /* [수정] 아바타 스타일 보완 */
  .avatar-circle {
    width: 40px; height: 40px; 
    background: #f5f7fa; border-radius: 50%;
    display: flex; align-items: center; justify-content: center; 
    color: #adb5bd;
    overflow: hidden; /* 이미지가 원 밖으로 나가는 것 방지 */
    border: 1px solid #eee; /* 얇은 테두리 추가 */
  }

  /* [추가] 이미지 꽉 차게 */
  .profile-img {
    width: 100%; height: 100%;
    object-fit: cover;
  }
  .text-info { display: flex; flex-direction: column; }
  .username { font-weight: 700; font-size: 0.95rem; color: #333; }
  .date { font-size: 0.85rem; color: #999; }
  
  .article-title {
    font-size: 1.4rem; font-weight: 800; color: #333; margin-bottom: 12px;
    line-height: 1.4;
    overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 1; -webkit-box-orient: vertical;
  }
  
  .article-preview {
    color: #666; font-size: 1rem; line-height: 1.6; margin: 0;
    overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  }
  
  .card-footer {
    padding: 20px 30px;
    background: #fcfcfc;
    border-top: 1px solid #f8f8f8;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .stats { display: flex; gap: 15px; }
  .stat-item { font-size: 0.95rem; color: #888; display: flex; align-items: center; gap: 5px; }
  .stat-item.heart i { color: #ff6b6b; }
  .stat-item.comment i { color: #2F65F6; }
  
  .read-more { font-size: 0.95rem; color: #2F65F6; font-weight: 700; opacity: 0; transform: translateX(-10px); transition: all 0.2s; }
  .article-card:hover .read-more { opacity: 1; transform: translateX(0); }
  
  .empty-state { text-align: center; padding: 80px 0; background: #f8f9fa; border-radius: 20px; }
  .icon-box { font-size: 4rem; margin-bottom: 20px; opacity: 0.5; }
  .empty-state h3 { font-size: 1.5rem; font-weight: 700; color: #333; margin-bottom: 10px; }
  .empty-state p { color: #888; }
  
  /* 모바일 반응형 */
  @media (max-width: 768px) {
    .view-container { width: 100%; padding: 0 15px; }
    .header-section { flex-direction: column; align-items: flex-start; gap: 20px; }
    .write-btn { width: 100%; justify-content: center; }
    .article-grid { grid-template-columns: 1fr; } /* 모바일은 1열 */
  }
  </style>