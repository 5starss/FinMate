<template>
  <div class="map-page-wrapper">
    <div class="map-container">
      
      <div class="search-panel">
        <h2 class="panel-title">내 주변 은행 찾기</h2>
        
        <div class="form-container">
          <div class="form-group">
            <label class="form-label">광역시/도</label>
            <div class="select-wrapper">
              <select v-model="selectedCity" @change="onCityChange" class="custom-select">
                <option value="">지역을 선택하세요</option>
                <option v-for="city in mapInfo" :key="city.name" :value="city.name">
                  {{ city.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">시/군/구</label>
            <div class="select-wrapper">
              <select v-model="selectedDistrict" :disabled="!selectedCity" class="custom-select">
                <option value="">시/군/구를 선택하세요</option>
                <option v-for="district in availableDistricts" :key="district" :value="district">
                  {{ district }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">은행</label>
            <div class="select-wrapper">
              <select v-model="selectedBank" class="custom-select">
                <option value="">은행을 선택하세요</option>
                <option v-for="bank in bankList" :key="bank" :value="bank">
                  {{ bank }}
                </option>
              </select>
            </div>
          </div>

          <button @click="searchPlaces" class="search-btn">
            검색하기
          </button>
        </div>

        <div class="divider"></div>

        <div class="mode-card" :class="{ active: isRouteMode }">
          <div class="mode-header">
            <span class="mode-title">🚗 길찾기 모드</span>
            <label class="toggle-switch">
              <input type="checkbox" v-model="isRouteMode" @change="onModeChange">
              <span class="slider round"></span>
            </label>
          </div>
          <p class="mode-desc">
            {{ isRouteMode 
              ? '지도 위 마커를 클릭하면 경로가 표시됩니다.' 
              : '활성화 시 현재 위치부터의 경로를 안내합니다.' 
            }}
          </p>
        </div>
      </div>

      <div id="map" class="map-area"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

const KAKAO_KEY=import.meta.env.VITE_KAKAO_JS_KEY
const KAKAO_REST_KEY = import.meta.env.VITE_KAKAO_REST_KEY

const mapInfo = ref([])
const bankList = ref([])

const selectedCity = ref('')
const selectedDistrict = ref('')
const selectedBank = ref('')
const searchExecuted = ref(false)
const isRouteMode = ref(false)

let map = null
let ps = null
let infowindow = null
let markers = []
let currentPolyline = null 
let userLocation = null    

const availableDistricts = computed(() => {
  if (!selectedCity.value) return []
  const cityData = mapInfo.value.find(c => c.name === selectedCity.value)
  return cityData ? (cityData.countries || cityData.districts) : []
})

const onCityChange = () => {
  selectedDistrict.value = ''
}

const onModeChange = () => {
  if (!isRouteMode.value) {
    removeRoute()
  }
}

onMounted(async () => {
  await loadData()
  if (window.kakao && window.kakao.maps) {
    initMap()
  } else {
    loadKakaoScript()
  }
})

const loadData = async () => {
  try {
    const response = await axios.get('/data.json')
    const data = response.data
    mapInfo.value = data.mapInfo
    bankList.value = data.bankInfo
  } catch (error) {
    console.error("data.json 로드 실패:", error)
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
    center: new window.kakao.maps.LatLng(37.49818, 127.027386),
    level: 3
  }
  map = new window.kakao.maps.Map(container, options)
  ps = new window.kakao.maps.services.Places()
  infowindow = new window.kakao.maps.InfoWindow({ zIndex: 1 })

  const geoOptions = {
    enableHighAccuracy: true,
    maximumAge: 0,
    timeout: 10000
  }

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lon = position.coords.longitude
        userLocation = { lat, lon }
        
        const locPosition = new window.kakao.maps.LatLng(lat, lon)
        map.setCenter(locPosition)

        const myMarker = new window.kakao.maps.Marker({
          map: map,
          position: locPosition,
          title: '내 위치',
          image: new window.kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png',
            new window.kakao.maps.Size(35, 40)
          )
        })
      },
      (err) => {
        console.error(err)
      },
      geoOptions 
    )
  }
}

const searchPlaces = () => {
  if (!selectedCity.value || !selectedDistrict.value || !selectedBank.value) {
    alert("지역과 은행을 모두 선택해주세요.")
    return
  }
  const keyword = `${selectedCity.value} ${selectedDistrict.value} ${selectedBank.value}`
  
  removeMarkers()
  removeRoute()

  ps.keywordSearch(keyword, placesSearchCB)
}

const placesSearchCB = (data, status) => {
  if (status === window.kakao.maps.services.Status.OK) {
    searchExecuted.value = true
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
      <div style="padding:15px; width:220px; border-radius:8px;">
        <h4 style="margin:0 0 5px; font-size:15px; color:#333;">${place.place_name}</h4>
        <p style="margin:0 0 10px; font-size:13px; color:#666; white-space:normal;">${place.address_name}</p>
        <a href="${place.place_url}" target="_blank" style="
          display:inline-block; 
          padding:5px 10px; 
          background:#2F65F6; 
          color:white; 
          text-decoration:none; 
          font-size:12px; 
          border-radius:4px;">상세보기</a>
      </div>`

    infowindow.setContent(content)
    infowindow.open(map, marker)

    if (isRouteMode.value) {
      if (userLocation) {
        const destination = { lat: place.y, lon: place.x }
        getCarDirection(userLocation, destination)
      } else {
        alert("내 위치 정보를 찾을 수 없습니다.")
      }
    }
  })
}

const getCarDirection = async (start, end) => {
  removeRoute()
  const origin = `${start.lon},${start.lat}`
  const destination = `${end.lon},${end.lat}`

  try {
    const response = await axios.get('/navi/v1/directions', {
      params: { origin, destination },
      headers: { Authorization: `KakaoAK ${KAKAO_REST_KEY}` }
    })

    if (response.data.routes && response.data.routes.length > 0) {
      const linePath = []
      const sections = response.data.routes[0].sections

      sections.forEach(section => {
        section.roads.forEach(road => {
          for (let i = 0; i < road.vertexes.length; i += 2) {
            linePath.push(new window.kakao.maps.LatLng(road.vertexes[i + 1], road.vertexes[i]))
          }
        })
      })

      currentPolyline = new window.kakao.maps.Polyline({
        path: linePath,
        strokeWeight: 6,
        strokeColor: '#2F65F6',
        strokeOpacity: 0.8,
        strokeStyle: 'solid'
      })

      currentPolyline.setMap(map)
      
      const distance = response.data.routes[0].summary.distance
      const duration = Math.round(response.data.routes[0].summary.duration / 60)
      alert(`🚗 경로 탐색 완료!\n약 ${duration}분 소요 (${distance}m)`)
      
    } else {
      alert("경로를 찾을 수 없습니다.")
    }

  } catch (error) {
    console.error(error)
    alert("경로 데이터를 불러오는 데 실패했습니다.")
  }
}

const removeRoute = () => {
  if (currentPolyline) {
    currentPolyline.setMap(null)
    currentPolyline = null
  }
}

const removeMarkers = () => {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(null)
  }
  markers = []
}
</script>

<<style scoped>
/* [페이지 래퍼] 화면 전체 높이에서 헤더(70px)를 뺀 만큼만 사용 */
.map-page-wrapper {
  height: calc(100vh - 70px);
  width: 100%;
  padding: 30px; /* 카드 주변 여백 */
  box-sizing: border-box; /* 패딩을 포함해서 높이 계산 */
  background-color: white;
  
  /* 내용물 중앙 정렬 */
  display: flex;
  justify-content: center;
  align-items: center;

  /* 혹시 모를 1px 오차 등으로 생기는 스크롤을 강제로 숨김 */
  overflow: hidden; 
}

/* [지도 컨테이너] 부모가 준 공간(여백 뺀 나머지)을 100% 채움 */
.map-container {
  display: flex;
  width: 100%;
  height: 100%; /* [핵심] 고정 px 대신 %로 설정하여 창 크기 따라감 */
  max-width: 1400px;
  
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #eee;
  overflow: hidden; 
}

/* 왼쪽 검색 패널 */
.search-panel {
  width: 360px;
  min-width: 360px;
  height: 100%;
  background-color: white;
  z-index: 20;
  border-right: 1px solid #eee;
  padding: 25px;
  
  display: flex;
  flex-direction: column;
  overflow-y: auto; /* 패널 내부 스크롤 */
}

/* 스크롤바 디자인 */
.search-panel::-webkit-scrollbar { width: 5px; }
.search-panel::-webkit-scrollbar-thumb { background-color: #ddd; border-radius: 3px; }
.search-panel::-webkit-scrollbar-track { background-color: transparent; }

/* 폼 요소 스타일 (기존 유지) */
.panel-title { font-size: 22px; font-weight: 800; color: #333; margin-bottom: 25px; }
.form-container { display: flex; flex-direction: column; gap: 15px; }
.form-label { font-size: 14px; font-weight: 600; color: #666; margin-bottom: 6px; display: block; }
.select-wrapper { position: relative; }
.custom-select { width: 100%; padding: 10px 14px; font-size: 14px; border: 1px solid #ddd; border-radius: 8px; appearance: none; background-color: white; outline: none; cursor: pointer; background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23999' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e"); background-repeat: no-repeat; background-position: right 12px center; background-size: 16px; }
.custom-select:focus { border-color: #2F65F6; box-shadow: 0 0 0 3px rgba(47, 101, 246, 0.1); }
.custom-select:disabled { background-color: #f9f9f9; cursor: not-allowed; }
.search-btn { width: 100%; padding: 12px; margin-top: 10px; background-color: #2F65F6; color: white; border: none; border-radius: 8px; font-size: 15px; font-weight: 700; cursor: pointer; transition: background-color 0.2s; }
.search-btn:hover { background-color: #1c50d8; }
.divider { height: 1px; background-color: #eee; margin: 25px 0; }
.mode-card { background-color: #f8f9fa; border: 1px solid #eee; border-radius: 10px; padding: 15px; transition: all 0.3s; }
.mode-card.active { background-color: #eef4ff; border-color: #dbeafe; }
.mode-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.mode-title { font-size: 15px; font-weight: 700; color: #333; }
.mode-desc { font-size: 12px; color: #777; line-height: 1.4; margin: 0; }
.toggle-switch { position: relative; display: inline-block; width: 40px; height: 22px; }
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #ccc; transition: .4s; border-radius: 34px; }
.slider:before { position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px; background-color: white; transition: .4s; border-radius: 50%; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
input:checked + .slider { background-color: #2F65F6; }
input:checked + .slider:before { transform: translateX(18px); }

/* 지도 영역 */
.map-area {
  flex-grow: 1;
  height: 100%;
  background-color: #eee;
}

/* [반응형] 모바일 화면 처리 */
@media (max-width: 700px) {
  .map-page-wrapper {
    padding: 0;
    height: auto;
    min-height: calc(100vh - 70px);
    overflow: auto;
    display: block;
  }
  
  .map-container {
    border-radius: 0;
    border: none;
    flex-direction: column;
    height: auto;
    box-shadow: none;
  }
  
  .search-panel {
    width: 100%;
    min-width: 0;
    height: auto;
    border-right: none;
    border-bottom: 1px solid #eee;
  }
  
  .map-area {
    height: 60vh;
  }
}
</style>