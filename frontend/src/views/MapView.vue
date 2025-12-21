<template>
    <div class="bank-container">
      <div class="search-panel">
        <h3>은행</h3>
        
        <div class="form-group">
          <label>광역시/도</label>
          <select v-model="selectedCity" @change="onCityChange" class="form-control">
            <option value="">지역을 선택하세요</option>
            <option v-for="city in mapInfo" :key="city.name" :value="city.name">
              {{ city.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>시/군/구</label>
          <select v-model="selectedDistrict" :disabled="!selectedCity" class="form-control">
            <option value="">시/군/구를 선택하세요</option>
            <option v-for="district in availableDistricts" :key="district" :value="district">
              {{ district }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>은행</label>
          <select v-model="selectedBank" class="form-control">
            <option value="">은행을 선택하세요</option>
            <option v-for="bank in bankList" :key="bank" :value="bank">
              {{ bank }}
            </option>
          </select>
        </div>

        <button @click="searchPlaces" class="btn btn-primary search-btn">
          찾기
        </button>
      </div>

      <div id="map" class="map-area"></div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  import axios from 'axios'

  const KAKAO_KEY=import.meta.env.VITE_KAKAO_JS_KEY
  console.log('현재 카카오 키:', KAKAO_KEY)

  const mapInfo = ref([])
  const bankList = ref([])

  const selectedCity = ref('')
  const selectedDistrict = ref('')
  const selectedBank = ref('')

  let map = null
  let ps = null
  let infowindow = null
  let markers = []

  // 4. Computed: 시/군/구 목록 계산
  const availableDistricts = computed(() => {
    if (!selectedCity.value) return []
    // mapInfo에서 선택된 도시 객체를 찾음
    const cityData = mapInfo.value.find(c => c.name === selectedCity.value)
    
    // map.html 코드를 보니 속성명이 'countries' 였으므로 그것을 사용합니다.
    // 만약 json 파일 속성명이 'districts'라면 cityData.districts로 바꿔주세요.
    return cityData ? (cityData.countries || cityData.districts) : []
  })

  // 5. 이벤트 핸들러
  const onCityChange = () => {
    selectedDistrict.value = '' // 도시가 바뀌면 구 선택 초기화
  }

  // 6. 라이프사이클 (마운트 시 실행)
  onMounted(async () => {
    // 6-1. JSON 데이터 불러오기
    await loadData()

    // 6-2. 카카오맵 로드
    if (window.kakao && window.kakao.maps) {
      initMap()
    } else {
      loadKakaoScript()
    }
  })

  // [핵심] data.json 불러오는 함수
  const loadData = async () => {
    try {
      // public 폴더에 있는 data.json 요청
      const response = await axios.get('/data.json')
      const data = response.data
      
      // 가져온 데이터를 변수에 저장
      mapInfo.value = data.mapInfo
      bankList.value = data.bankInfo
      
      console.log("데이터 로드 완료:", mapInfo.value)
    } catch (error) {
      console.error("data.json 로드 실패:", error)
      alert("데이터 파일을 불러오지 못했습니다.")
    }
  }

  const loadKakaoScript = () => {
    const script = document.createElement('script')
    script.src = `//dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey=${KAKAO_KEY}&libraries=services`
    script.onload = () => window.kakao.maps.load(initMap)
    document.head.appendChild(script)
  }
  
  const initMap = () => {
    const container = document.getElementById('map')
    const options = {
      center: new window.kakao.maps.LatLng(37.49818, 127.027386), // 강남역
      level: 3
    }
    map = new window.kakao.maps.Map(container, options)
    ps = new window.kakao.maps.services.Places()
    infowindow = new window.kakao.maps.InfoWindow({ zIndex: 1 })
  }
  
  const searchPlaces = () => {
    if (!selectedCity.value || !selectedDistrict.value || !selectedBank.value) {
      alert("지역과 은행을 모두 선택해주세요.")
      return
    }
    const keyword = `${selectedCity.value} ${selectedDistrict.value} ${selectedBank.value}`
    console.log("검색 키워드:", keyword)
    
    removeMarkers()
    ps.keywordSearch(keyword, placesSearchCB)
  }

  const placesSearchCB = (data, status) => {
    if (status === window.kakao.maps.services.Status.OK) {
      const bounds = new window.kakao.maps.LatLngBounds()
      for (let i = 0; i < data.length; i++) {
        displayMarker(data[i])
        bounds.extend(new window.kakao.maps.LatLng(data[i].y, data[i].x))
      }
      map.setBounds(bounds)
    } else if (status === window.kakao.maps.services.Status.ZERO_RESULT) {
      alert("검색 결과가 없습니다.")
    } else if (status === window.kakao.maps.services.Status.ERROR) {
      alert("검색 중 오류가 발생했습니다.")
    }
  }

  const displayMarker = (place) => {
    const marker = new window.kakao.maps.Marker({
      map: map,
      position: new window.kakao.maps.LatLng(place.y, place.x)
    })
    markers.push(marker)
    window.kakao.maps.event.addListener(marker, 'click', () => {
      const content = `
        <div style="padding:10px; font-size:12px; width:200px;">
          <strong>${place.place_name}</strong><br>
          <span style="color:gray;">${place.address_name}</span><br>
          <a href="${place.place_url}" target="_blank" style="color:blue;">상세보기</a>
        </div>`
      infowindow.setContent(content)
      infowindow.open(map, marker)
    })
  }

  const removeMarkers = () => {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(null)
    }
    markers = []
  }
  </script>
  
  <style scoped>
  .bank-container { display: flex; height: calc(100vh - 70px); }
  .search-panel { width: 300px; padding: 20px; background-color: #f8f9fa; border-right: 1px solid #ddd; overflow-y: auto; }
  .map-area { flex-grow: 1; width: 100%; height: 100%; }
  .form-group { margin-bottom: 15px; }
  .form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
  .form-control { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
  .search-btn { width: 100%; padding: 10px; margin-top: 10px; background-color: #0d6efd; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
  .search-btn:hover { background-color: #0b5ed7; }
  </style>