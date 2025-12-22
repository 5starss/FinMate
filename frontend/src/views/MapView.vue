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

      <hr style="margin: 20px 0; border: 0; border-top: 1px solid #ddd;">

      <div class="route-mode-box">
        <label class="switch-label">
          <input type="checkbox" v-model="isRouteMode" @change="onModeChange">
          <span class="mode-text">길찾기</span>
        </label>
        <p class="mode-desc">
          {{ isRouteMode ? 'ON: 마커를 누르면 경로가 표시됩니다.' : 'OFF: 마커를 누르면 정보만 표시됩니다.' }}
        </p>
      </div>
    </div>

    <div id="map" class="map-area"></div>
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
let currentPolyline = null // 현재 그려진 경로선
let userLocation = null    // 내 위치 저장용 (경로 탐색 시작점)

// 시/군/구 목록 계산
const availableDistricts = computed(() => {
  if (!selectedCity.value) return []
  // mapInfo에서 선택된 도시 객체를 찾음
  const cityData = mapInfo.value.find(c => c.name === selectedCity.value)
  
  return cityData ? (cityData.countries || cityData.districts) : []
})

// 이벤트 핸들러
const onCityChange = () => {
  selectedDistrict.value = '' // 도시가 바뀌면 구 선택 초기화
}

// 길찾기 모드 변경 시 기존 경로 제거
const onModeChange = () => {
  if (!isRouteMode.value) {
    removeRoute()
  }
}

onMounted(async () => {
  // JSON 데이터 불러오기
  await loadData()

  // 카카오맵 로드
  if (window.kakao && window.kakao.maps) {
    initMap()
  } else {
    loadKakaoScript()
  }
})

// data.json 불러오는 함수
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

  const geoOptions = {
    enableHighAccuracy: true, // 정확도 우선 모드 켜기
    maximumAge: 0,            // 캐시된 위치값 쓰지 않고 매번 새로 찾기
    timeout: 10000            // 10초 안에 못 찾으면 에러 처리
  }

  // 내 위치 저장
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude
        const lon = position.coords.longitude
        userLocation = { lat, lon } // 내 위치 저장
        
        const locPosition = new window.kakao.maps.LatLng(lat, lon)
        map.setCenter(locPosition)

        // 내 위치 마커 표시
        const myMarker = new window.kakao.maps.Marker({
          map: map,
          position: locPosition,
          title: '내 위치',
          image: new window.kakao.maps.MarkerImage(
            'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_red.png', // 빨간색 마커로 구분
            new window.kakao.maps.Size(30, 40)
          ),
          draggable: true // 마커를 움직일 수 있게 함
        })

        // 마커를 옮기면 옮긴 위치를 '내 위치'로 다시 저장
        window.kakao.maps.event.addListener(myMarker, 'dragend', () => {
          const newPos = myMarker.getPosition()
          userLocation = { lat: newPos.getLat(), lon: newPos.getLng() }
          console.log("내 위치가 사용자에 의해 수정됨:", userLocation)
        })
      },
      (err) => {
        console.error("위치 정보 에러:", err)
        alert("위치 정보를 가져올 수 없습니다. 기본 위치로 설정합니다.")
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
  console.log("검색 키워드:", keyword)
  
  removeMarkers() // 기존 마커 제거
  removeRoute()   // 기존 경로 제거

  ps.keywordSearch(keyword, placesSearchCB)
}

const placesSearchCB = (data, status) => {
  if (status === window.kakao.maps.services.Status.OK) {
    searchExecuted.value = true // 안내 문구 표시
    // alert("마커를 클릭하면 현재 위치로부터 경로를 출력합니다.") // 알림창

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

    // 길찾기 모드일 경우 길찾기(경로 탐색) 실행
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
// 자동차 경로 찾기 (Kakao Mobility API)
const getCarDirection = async (start, end) => {
  // 기존 경로 지우기
  removeRoute()

  // 카카오 모빌리티 API는 "경도(x),위도(y)" 순서로 파라미터를 받음
  const origin = `${start.lon},${start.lat}`
  const destination = `${end.lon},${end.lat}`

  try {
    // 프록시(/navi)를 통해 요청
    const response = await axios.get('/navi/v1/directions', {
      params: { origin, destination },
      headers: {
        Authorization: `KakaoAK ${KAKAO_REST_KEY}` // REST API 키 사용
      }
    })

    if (response.data.routes && response.data.routes.length > 0) {
      const linePath = []
      const sections = response.data.routes[0].sections

      // 경로 데이터 파싱 (vertexes는 [x, y, x, y...] 형태로 들어옴)
      sections.forEach(section => {
        section.roads.forEach(road => {
          for (let i = 0; i < road.vertexes.length; i += 2) {
            linePath.push(new window.kakao.maps.LatLng(
              road.vertexes[i + 1], // 위도 (y)
              road.vertexes[i]      // 경도 (x)
            ))
          }
        })
      })

      // 지도에 경로 그리기 
      currentPolyline = new window.kakao.maps.Polyline({
        path: linePath,
        strokeWeight: 5,
        strokeColor: '#0000FF',
        strokeOpacity: 0.7,
        strokeStyle: 'solid'
      })

      currentPolyline.setMap(map)
      
      // 인포윈도우로 거리/시간 표시
      const distance = response.data.routes[0].summary.distance // 미터 단위
      const duration = Math.round(response.data.routes[0].summary.duration / 60) // 분 단위
      alert(`경로 탐색 완료! 약 ${duration}분 소요 (${distance}m)`)
      
    } else {
      alert("경로를 찾을 수 없습니다.")
    }

  } catch (error) {
    console.error("경로 찾기 실패:", error)
    alert("경로 데이터를 불러오는 데 실패했습니다. REST API 키를 확인해주세요.")
  }
}

// 경로선 제거 함수
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

<style scoped>
.route-mode-box {
  background-color: #e9ecef;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
}

.switch-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-weight: bold;
  font-size: 16px;
}

.switch-label input {
  width: 18px;
  height: 18px;
  margin-right: 8px;
  cursor: pointer;
}

.mode-desc {
  font-size: 12px;
  color: #666;
  margin: 5px 0 0 0;
}
.info-text {
  margin-top: 15px;
  padding: 10px;
  background-color: #e7f1ff;
  border-radius: 5px;
  font-size: 14px;
  color: #0d6efd;
  font-weight: bold;
}
.bank-container { display: flex; height: calc(100vh - 70px); }
.search-panel { width: 300px; padding: 20px; background-color: #f8f9fa; border-right: 1px solid #ddd; overflow-y: auto; }
.map-area { flex-grow: 1; width: 100%; height: 100%; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: bold; }
.form-control { width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
.search-btn { width: 100%; padding: 10px; margin-top: 10px; background-color: #0d6efd; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
.search-btn:hover { background-color: #0b5ed7; }
</style>