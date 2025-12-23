<template>
  <div class="product-list">
    <div v-if="deposits.length === 0" class="no-data">
      조건에 맞는 상품이 없습니다.
    </div>

    <ul v-else class="list-wrapper">
      <li v-for="deposit in deposits" :key="deposit.id" class="product-item">
        <router-link :to="`/deposits/${deposit.id}`" class="product-link">
          
          <div class="bank-info">
            <div class="bank-icon">🏦</div> <span class="bank-name">{{ deposit.kor_co_nm }}</span>
          </div>

          <div class="product-info">
            <h3 class="product-name">{{ deposit.fin_prdt_nm }}</h3>
          </div>

          <div class="arrow-icon">
            ➜
          </div>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  deposits: {
    type: Array,
    required: true
  }
})
</script>

<style scoped>
.list-wrapper {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 카드 사이 간격 */
}

.product-item {
  background-color: white;
  border-radius: 12px;
  border: 1px solid #eee;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  transition: all 0.2s ease;
}

/* 마우스 올렸을 때 효과 */
.product-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(47, 101, 246, 0.15);
  border-color: #2F65F6;
}

.product-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 25px;
  text-decoration: none;
  color: inherit;
  width: 100%;
}

.bank-info {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 30%; /* 너비 고정 */
}

.bank-icon {
  width: 40px;
  height: 40px;
  background-color: #f0f4ff;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 20px;
}

.bank-name {
  font-size: 14px;
  color: #666;
  font-weight: 600;
}

.product-info {
  flex-grow: 1;
}

.product-name {
  font-size: 17px;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.arrow-icon {
  color: #ccc;
  font-size: 18px;
  transition: color 0.2s;
}

.product-item:hover .arrow-icon {
  color: #2F65F6;
}

.no-data {
  text-align: center;
  padding: 50px;
  color: #888;
  font-size: 16px;
}

/* 모바일 반응형 */
@media (max-width: 600px) {
  .product-link {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  .bank-info {
    width: 100%;
  }
  .arrow-icon {
    display: none; /* 모바일엔 화살표 숨김 */
  }
}
</style>