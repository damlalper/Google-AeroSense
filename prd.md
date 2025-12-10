📂 **PROJECT MASTER FILE: AERO-SENSE**

**Project Name:** Aero-Sense: Intelligent Engine Health & MLOps Platform  
**Hackathon:** Google Cloud Partner Hackathon (Datadog & Confluent Challenges)  
**Tech Stack:** Google Cloud Native (Cloud Run, Vertex AI) + Polyglot (Go, Python, TypeScript)  
**Architectural Style:** Event-Driven Microservices  
**Date:** December 2025  

---

# 1. 📄 Product Requirements Document (PRD)

## 1.1. Problem Statement
Havacılık sektöründe motor arızaları (Engine Failures) maliyetli ve tehlikelidir. Mevcut sistemler genellikle reaktiftir (arıza olunca uyarır). Biz, **Google Vertex AI** gücünü kullanarak arızayı olmadan önce tahmin eden (Predictive Maintenance) ve arıza durumunda **Gemini ile mühendisler için teknik reçete oluşturan** “Otonom” bir sistem kuruyoruz.

## 1.2. Solution Overview
**"Aero-Sense"**, NASA'nın jet motoru verilerini (simülasyon) ve canlı hava durumu verilerini (OpenWeatherMap API) birleştiren bir IoT platformudur. Sistem, motorun **Kalan Ömrünü (RUL - Remaining Useful Life)** hesaplar ve tüm bu süreci **Datadog üzerinden canlı izler.**

## 1.3. Key Features
- **High-Performance Ingestion (Golang):** Yüksek frekanslı sensör verisini düşük gecikmeyle işler.  
- **Hybrid Data Stream (Confluent Kafka):** Statik sensör verisi + canlı hava durumu verisi.  
- **AI Core (Vertex AI & Gemini):**  
  - Custom XGBoost RUL Model  
  - Gemini 1.5 Pro ile teknik bakım çözüm önerileri  
- **Full Observability (Datadog):** Model Drift, API Latency, System Health takibi  

---

# 2. 🏗️ Technical Specifications & Architecture

## 2.1. System Architecture Diagram (Conceptual)

```mermaid
graph TD
    A[NASA Data Source] -->|HTTP Post| B(Ingestion Service - GO)
    W[OpenWeather API] -->|Get Weather| B
    B -->|Cache Weather| R[Google Memorystore - REDIS]
    B -->|Stream Data| K[Confluent Cloud - KAFKA]
    K -->|Consume Data| C(AI Core Service - PYTHON)
    C -->|Predict RUL| V[Vertex AI Endpoint]
    C -->|Analyze Context| G[Gemini 1.5 Pro]
    C -->|Log Metrics| D[Datadog Agent]
    C -->|Store Results| DB[BigQuery / Firestore]
    F[Frontend - Next.js] -->|Fetch Data| C
    F -->|Maps Visualization| M[Google Maps API]
```
## 2.2. Tech Stack Details

| Component  | Technology        | Google Cloud Service | Reason                          |
|------------|-------------------|-----------------------|----------------------------------|
| Ingestion  | Go (Golang)       | Cloud Run             | High throughput, low CPU         |
| Processing | Python (FastAPI)  | Cloud Run             | Rich AI ecosystem                |
| ML Model   | XGBoost           | Vertex AI Training    | Strong for tabular sensor data   |
| GenAI      | Gemini 1.5 Pro    | Vertex AI Studio      | Multimodal reasoning             |
| Streaming  | Kafka             | Confluent Cloud       | Reliable event streaming         |
| Cache      | Redis             | Memorystore           | Reduces API latency              |
| Frontend   | Next.js           | Cloud Run             | SSR + modern UI                  |
| Infra      | Terraform         | —                     | IaC                               |
| Monitoring | Datadog           | —                     | Full observability                |

---

# 3. 🧩 Microservices Specification

## **Service A: ingestion-engine (Golang)**

**Role:** Data Producer  
**Responsibilities:**  
- NASA CMAPSS dataset'i satır satır okur  
- Redis’ten hava durumu kontrol eder; yoksa API’dan çeker  
- SensorData + WeatherData → Kafka’ya gönderir  

**Key Libraries:**  
`sarama`, `redigo`, `gin`

---

## **Service B: ai-core (Python)**

**Role:** Data Consumer & Intelligence  
**Responsibilities:**  
- Kafka’dan `telemetry.enriched` mesajlarını tüketir  
- Vertex AI RUL modeline gönderip tahmin alır  
- Eğer **Predicted_RUL < 20** ise Gemini’ye teknik teşhis prompt’u yollar  
- Datadog custom metrics push eder  

**Key Libraries:**  
`confluent-kafka`, `google-cloud-aiplatform`, `datadog`, `fastapi`

---

## **Service C: dashboard-ui (Next.js/TypeScript)**

**Role:** User Interface  
**Responsibilities:**  
- Gerçek zamanlı RUL göstergesi  
- Uçağın konumunu Google Maps üzerinde gösterme  
- Datadog grafikleri embed etme  
- Gemini’nin bakım reçetesini sunma  

**Key Libraries:**  
`framer-motion`, `google-maps-react`, `tailwindcss`

---

# 4. 📊 Data Schemas

## 4.1. Kafka Message Payload (JSON)

```json
{
  "flight_id": "FL-2025-NY",
  "timestamp": "2025-12-06T10:00:00Z",
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "external_context": {
    "temperature": 15.5,
    "humidity": 60
  },
  "sensors": {
    "fan_speed": 2388.05,
    "core_temp": 1400.2,
    "pressure": 554.3
  }
}
```
## 4.2. Datadog Custom Metrics

- **aero.ingestion.rate** – Messages per second (Go service)  
- **aero.weather.api_latency** – API fetch latency  
- **aero.model.rul_prediction** – Tahmin edilen kalan ömür  
- **aero.genai.cost** – Gemini maliyet tahmini  

---

# 5. 🛠️ Implementation Plan (DevOps & Git)

## 5.1. Directory Structure

/aero-sense-google-hackathon
├── /infra # Terraform files (GCP resources)
├── /services
│ ├── /ingestion-go # Golang Producer
│ ├── /ai-core-py # Python Consumer & Vertex Logic
│ └── /web-ui # Next.js Frontend
├── /data # Raw NASA datasets
├── /models # Training scripts for Vertex AI
└── /docs # Architecture images & PRD


## 5.2. Requirements for "Model Training"

- XGBoost regressor kullanılacak  
- Vertex AI Custom Training job ile eğitilecek  
- Model artifact şu dizine kaydedilecek:  
  **`gs://aero-sense-models/`**

---

# 6. 🎯 Success Criteria (Jury Checklist)

- **Integration:** Confluent → Python → Vertex AI → Datadog entegrasyonu başarılı mı?  
- **Innovation:** NASA + Live Weather hibrit veriyi kullanıyor mu?  
- **Google Native:** Backend Cloud Run’da mı? Gemini kullanıyor mu?  
- **Polyglot:** Go service yüksek performanslı mı?  
- **Observability:** Datadog panelleri aksiyon alınabilir şekilde mi?  

# 7. 📘 Hackathon Requirements Mapping (Partner Challenges → Aero-Sense Implementation)

Bu bölüm, Aero-Sense platformunun **Datadog**, **Confluent** ve isteğe bağlı olarak **ElevenLabs** challenge gereksinimlerini nasıl karşıladığını sistematik şekilde açıklar.

---

## 7.1. Datadog Challenge Mapping

**Challenge Özeti:**  
- Vertex AI veya Gemini tabanlı bir LLM uygulaması için uçtan uca gözlemlenebilirlik.  
- LLM sinyallerini Datadog'a aktarma (logs, metrics, traces, APM).  
- Dashboard + SLO + detection rules + incident automation.  
- 3+ detection rule zorunlu.  
- Olay tetiklendiğinde Datadog Incident / Case oluşturma.

### ✔ Aero-Sense Nasıl Karşılıyor?

| Gereksinim | Aero-Sense Uygulaması |
|-----------|------------------------|
| LLM-based application | Gemini 1.5 Pro ile bakım önerisi üreten servis |
| Telemetry → Datadog | ai-core tüm inference metriklerini gönderir: latency, cost, drift, prediction distribution |
| Dashboard | RUL trendleri, inference zamanları, Kafka lag, Redis latency, drift sinyalleri |
| Detection Rules (min 3) | 1) RUL anomaly < 10, 2) inference latency > threshold, 3) Gemini cost spike detection |
| Incident / Case Creation | Datadog API + webhook integration ile otomatik incident oluşturma |
| SLO | Model latency SLO, ingestion throughput SLO, LLM cost SLO |

---

## 7.2. Confluent Challenge Mapping

**Challenge Özeti:**  
- Gerçek zamanlı bir veri akışı üzerinde gelişmiş AI/ML teknikleri.  
- Confluent Cloud + Google Cloud AI entegrasyonu.  
- Veriyle gerçek zamanlı etkileşen “AI on data in motion” uygulaması.

### ✔ Aero-Sense Nasıl Karşılıyor?

| Gereksinim | Aero-Sense Uygulaması |
|-----------|------------------------|
| Real-time data stream | NASA CMAPSS sensör datası + canlı hava durumu |
| Confluent Cloud | telemetry.enriched topic + consumer group yapısı |
| AI model | Vertex AI XGBoost RUL Model |
| Real-time prediction | ai-core her mesajı işleyip RUL tahmini üretir |
| Novel use case | Havacılıkta gerçek zamanlı motor ömrü düşüşü takibi |
| Impact | Maintenance costs ↓, safety ↑ |

---

## 7.3. ElevenLabs Challenge Mapping (Opsiyonel Kullanım)

Aero-Sense ana çözümü için zorunlu değildir; ancak istenirse:

- Gemini bakım raporunu ElevenLabs Agents ile sesli şekilde okuyan bir **Konuşan Maintenance Assistant** eklenebilir.
- Uçuş mühendisleri için hands-free kullanım sağlar.

---

# 8. 🧮 Evaluation Strategy (Judging Criteria Alignment)

Bu bölüm, Aero-Sense’in jürinin 4 ana değerlendirme kriterine göre nasıl optimize edildiğini açıklar.

## 8.1. Technological Implementation
- Cloud Run üzerinde polyglot microservices: Go + Python + TypeScript.  
- Vertex AI Endpoints, Gemini API, Confluent Cloud, Datadog full-stack.  
- Infrastructure as Code: Terraform ile otomatik deployment.  
- End-to-end telemetry: logs, traces, metrics, LLM observability signals.  
- Redis caching ile API latency optimize edildi.

## 8.2. Design & UX
- RUL Gauge + real-time telemetry dashboard.  
- Google Maps üzerinde uçak konum & hava durumu overlay.  
- Gemini’den gelen teknik bakım önerileri okunabilir şekilde sunulur.  
- Minimal, hızlı ve intuitive UI (Next.js + Tailwind).

## 8.3. Potential Impact
- Havacılık sektöründe proaktif bakım → milyonlarca dolar maliyet tasarrufu.  
- Model Drift erken tespiti → emniyet artışı.  
- Diğer sektörlere uyarlanabilir (enerji, otomotiv, IoT).  

## 8.4. Quality of the Idea
- Hibrit veri yaklaşımı (NASA dataset + gerçek hava durumu).  
- LLM destekli otomatik maintenance engineering.  
- Tamamen Google Cloud Native + Partner ürünlerini derinlemesine kullanan uçtan uca tasarım.

---

# 9. 📦 Compliance & Submission Checklist

Hackathon teslim gereksinimleri ile tam uyum için Aero-Sense proje paketinin aşağıdaki içeriğe sahip olması zorunludur.

## 9.1. Required Project Artifacts

### ✔ Hosted Application URL  
- Cloud Run URL'si  
- Dashboard + UI erişimi

### ✔ Public GitHub Repository  
- OSI-approved license (MIT, Apache 2.0 vb.)  
- /infra, /services, /models, /docs klasörlerinin tamamı  
- README → Deployment talimatları  
- Datadog config exports (JSON):  
  - dashboards  
  - SLOs  
  - monitors  
  - detection rules  

### ✔ 3-Minute Demo Video  
- YouTube / Vimeo (public)  
- İçermesi gerekenler:  
  - Architecture walkthrough  
  - Datadog detection rule tetikleme örneği  
  - Confluent data pipeline  
  - Vertex AI inference  
  - Gemini bakım aksiyonu

### ✔ Selected Challenge  
- Datadog  
- Confluent  
- (Opsiyonel) ElevenLabs

---

## 9.2. Datadog Hard Requirements Checklist

| Requirement | Status |
|------------|--------|
| In-Datadog Health Dashboard | ✔ |
| 3+ Detection Rules | ✔ |
| Telemetry streaming (LLM + runtime) | ✔ |
| Actionable record (Incident/Case) | ✔ |
| Vertex AI / Gemini usage | ✔ |
| Traffic Generator Script | ✔ |
| JSON export of Datadog configs | ✔ |

---

## 9.3. Google Cloud Credits Policy Compliance
- Credits redeemed before **Dec 15, 2025**  
- Usage within 2 weeks  
- Spending monitored via Budgets & Alerts  

---

## 9.4. Confluent Cloud Requirements Checklist
- 30-day trial code: `CONFLUENTDEV1`  
- Enriched telemetry stream  
- Real-time predictions  
- AI on data in motion use case  

---

## 9.5. Optional ElevenLabs Integration
- Voice-based maintenance assistant  
- Real-time speech output for Gemini reports  

# 10. 🔄 Data Flow & Event Lifecycle (Veri Akışı ve Olay Döngüsü)

Bu bölüm, veri nasıl aktığını, işlendiğini ve sisteme nasıl entegre olduğunu detaylı olarak anlatır. Claude veya jüri sistemi için çok kritiktir.

## 10.1. Event Lifecycle Diagram

```mermaid
graph TD
    A[NASA Dataset CSV] -->|HTTP POST /batch| B(Ingestion Engine - Go)
    W[OpenWeather API] -->|API Request| B
    B -->|Cache| R[Redis]
    B -->|Publish| K[Kafka telemetry.enriched]
    K -->|Consume| C[AI Core Service - Python]
    C -->|Predict RUL| V[Vertex AI Endpoint]
    C -->|Generate Maintenance Advice| G[Gemini 1.5 Pro]
    C -->|Push Metrics| D[Datadog Agent]
    C -->|Store Results| DB[BigQuery / Firestore]
    F[Dashboard UI] -->|Query Data| DB
    F -->|Fetch Realtime Metrics| D

```
## 10.2. Event Handling Notes

- **Latency sensitive paths:** Ingestion → Kafka → AI Core

- **Failure handling:**
  - Redis cache miss → fetch from OpenWeather
  - Kafka publish/consume failures → retry 3x with exponential backoff
  - Vertex AI errors → log to Datadog, fallback to last prediction

- **Telemetry tracking:** ingestion rate, API latency, prediction time, model drift

- **Data persistence:** BigQuery for analytics, Firestore for real-time access

---

# 11. 👤 User Stories & Edge Cases (Kullanıcı Hikayeleri ve Kenar Durumlar)

Bu bölüm, sistemin **kullanıcı perspektifinden anlaşılmasını ve test edilebilirliğini** sağlar. Claude’un sistemi anlaması için kritik.

## 11.1. Primary User Stories

### Mühendis (Maintenance Engineer)
- "Uçağın motorunun kalan ömrünü gerçek zamanlı görmek istiyorum."
- "Motor arızası olasılığı düşük olan uçuşları planlayıp, bakım zamanını optimize etmek istiyorum."

### DevOps / Monitoring Lead
- "AI modelinin performansını ve latency’yi Datadog üzerinden izlemek istiyorum."
- "Model drift veya anomali olduğunda otomatik alarm alıp aksiyon almak istiyorum."

### Product Owner / Manager
- "Platformun uçtan uca veri akışını ve hava durumu entegrasyonunu görebilmek istiyorum."
- "Dashboard üzerinden kullanıcı deneyimini ölçmek ve raporlamak istiyorum."

---

## 11.2. Edge Cases & System Safeguards

| Edge Case                     | Mitigation                                                  |
|--------------------------------|------------------------------------------------------------|
| Sensör verisi eksik / hatalı   | AI Core, eksik verileri interpolate eder veya önceki değeri kullanır |
| OpenWeather API down           | Redis cache fallback veya default weather values          |
| Kafka backlog çok yüksek       | Metrics & alerts → auto-scale ingestion consumers         |
| Vertex AI downtime             | Fallback cached predictions + Datadog alert               |
| Gemini API rate limit exceeded | Queue system with retry & throttling                       |

---

## 11.3. Benefits for Claude

- Sistem mantığı, veri akışı ve hata senaryoları net olarak tanımlandı.  
- User intent ve sistem tepkisi açık şekilde eşleştirildi.  
- Edge case’ler sayesinde model, "ne zaman hangi fallback kullanılır" mantığını doğru anlayabilir.





# NEW
# IMPLEMENTATION-MUST DO AND DATA-
### 📅 Tarih: 7 Aralık 2025  
### 🎯 Hedef: Google Cloud Hackathon (Datadog & Confluent Tracks)  
### ⏳ Son Teslim: 1 Ocak 2026

---

# 🏛️ BÖLÜM 1: İDARİ & KAYNAK YÖNETİMİ (SENİN GÖREVİN)

Bu bölüm hackathon kayıtları, ücretsiz krediler ve API anahtarlarıyla ilgili. **En kısa sürede tamamlanmalı.**

### ✔️ Yapılacaklar

- [ ] **Devpost Kaydı**  
  → https://aiinaction.devpost.com adresinden **Join Hackathon** butonuna tıkla.

- [ ] **Datadog Webinar Kaydı (KRİTİK)**  
  **Tarih:** 9 Aralık, 09:00 EST (TSİ ≈ 17:00)  
  → Hackathon sayfasındaki linkten kayıt ol.  
  → **+30 gün ek süreyi kap.**

- [ ] **Google Cloud Kredisi ($50)**  
  → Hackathon sayfasındaki formu doldur.  
  **Not:** Mailine gelen kredi kodunu sakla.  
  **Hemen Redeem etme!**  
  Vertex AI eğitimine 2. hafta başlarken kullanılacak.  
  **Son kullanma:** 15 Aralık.

- [ ] **Confluent Cloud Hesabı**  
  → Hesap aç.  
  → *Billing → Payment* bölümüne `CONFLUENTDEV1` kampanya kodunu ekle.  
  → 30 gün ücretsiz kullanım açılacak.

- [ ] **OpenWeatherMap API Key**  
  → https://openweathermap.org  
  → Üye ol → **My API Keys** → Yeni API key oluştur → Kaydet.

---

# 💻 BÖLÜM 2: YEREL GELİŞTİRME ORTAMI (SENİN GÖREVİN)

Bilgisayarını bir Google mühendisi set-up’ına çeviriyoruz.

- [ ] **Go (Golang) Kurulumu**  
  → https://go.dev/dl adresinden indir & kur  
  **Test:**  
go version



- [ ] **Python 3.9+ Kontrolü**  
Sisteminde Python zaten var, ama **3.9+ olmalı**.

- [ ] **Docker Kurulumu**  
→ Docker Desktop indir, kur, çalıştır.

- [ ] **Google Cloud SDK (gcloud CLI)**  
→ https://cloud.google.com/sdk/docs/install  
**Komut:**  
gcloud init



- [ ] **VS Code Eklentileri**
- Go (Go Team at Google)
- Python (Microsoft)
- HCL (Terraform için)
- Docker

---

# ☁️ BÖLÜM 3: BULUT HESAP KURULUMLARI (SENİN GÖREVİN)

### ✔️ Google Cloud

- [ ] **Yeni Proje Oluştur**  
→ *aero-sense-hackathon*

- [ ] **Aşağıdaki API’ları Enable et**
- Vertex AI API  
- Cloud Run API  
- Artifact Registry API  
- Cloud Build API

### ✔️ Datadog

- [ ] Datadog hesabı oluştur (Region: **US**)  
**Not:** US en uyumlu bölge.  

- [ ] API Key ve Application Key oluştur → Not et.

---

# 📂 BÖLÜM 4: REPO & VERİ HAZIRLIĞI (SENİN GÖREVİN)

### ✔️ GitHub

- [ ] **Yeni repo aç:** `aero-sense-hackathon`  
- [ ] Repoyu klonla:  
git clone <repo-url>



### ✔️ Lisans Dosyası

- [ ] Ana dizine **LICENSE** dosyası ekle.  
İçerik: MIT License veya Apache 2.0 (Hackathon zorunluluğu).

### ✔️ Proje Klasörleri

mkdir -p data/raw
mkdir -p services/ingestion-go
mkdir -p services/ai-core-python
mkdir -p infra
mkdir -p docs


### ✔️ NASA CMAPSS Verisi

- [ ] NASA CMAPSS dataset indir.  
- [ ] `train_FD001.txt` dosyasını  
  `data/raw/` klasörüne koy.

---

# 🤖 BÖLÜM 5: CLAUDE İLE KODLAMA (CLAUDE'UN GÖREVİ)

Aşağıdaki adımları **sırayla Claude’a yazacaksın.**

---

## ✅ Adım 1 — Go Ingestion Servisi (Veri Toplama)

Claude'a şu promptu gönder:

Sana daha önce verdiğim 'Project Master File'a sadık kalarak; services/ingestion-go klasörü altında çalışacak bir Go uygulaması istiyorum.

data/raw/train_FD001.txt dosyasını satır satır okusun.

OpenWeatherMap API'sinden (şimdilik mock fonksiyon) hava verisi çeksin.

Bu iki veriyi bir JSON struct'ta birleştirsin.

datadog-go/statsd kütüphanesini kullanarak her okumada aero.ingestion.events metriğini artırsın.

Bana main.go, go.mod ve Dockerfile içeriklerini ver.



---

## ✅ Adım 2 — Kafka Producer Entegrasyonu

Claude'a devam promptu:

Harika. Şimdi bu koda Confluent Kafka entegrasyonu ekle.
github.com/confluentinc/confluent-kafka-go kütüphanesini kullan.

Okuduğun veriyi telemetry.raw topiğine gönder.

Gönderirken Kafka Header'ına trace_id (UUID) eklemeyi unutma (Datadog tracing için).


---

## ✅ Adım 3 — Python AI Servisi (Kafka Consumer)

Claude'a şu promptu gönder:

Şimdi services/ai-core-python klasörüne geçelim. Python ve FastAPI kullanarak bir Kafka Consumer yazmanı istiyorum.

telemetry.raw topiğini dinlesin.

Gelen mesajdaki trace_id'yi okusun ve ddtrace kütüphanesi ile context'i devam ettirsin.

Şimdilik Vertex AI'a gitmeden sadece log bassın.

requirements.txt, main.py ve Dockerfile ver.


---

# 🚀 SONRAKİ ADIM (BU LİSTE BİTİNCE ELİNDE OLACAK)

- Tüm hesaplar açılmış  
- NASA verileri indirilmiş  
- Go ingestion servisi hazır  
- Kafka producer entegre edilmiş  
- Python tüketici servisi hazır  
- Log/Trace/Metrics altyapısı kurulum aşamasında  
- Tümü GitHub’a pushlanmış

---

# 🛡️ BÖLÜM 6: DATADOG ADVANCED IMPLEMENTATION PLAN

Bu plan **jürinin en çok etkileneceği** kısım.  
Claude ve sen bunu uygulayacaksınız.

---

## ⭐ 1. Distributed Tracing & Context Propagation (EN KRİTİK)

### Amaç  
Go → Kafka → Python boyunca **tek bir trace zinciri** oluşturmak.

### Teknik İşleyiş  
- **Go Producer:**  
  - ddtrace span başlat  
  - Trace ID & Span ID → Kafka Header’a enjekte et  

- **Python Consumer:**  
  - Header’dan trace ID’yi al  
  - Aynı trace içinde “child span” oluştur  
  - Böylece zincir kopmaz

### Kütüphaneler  
- Go → `gopkg.in/DataDog/dd-trace-go.v1`  
- Python → `ddtrace`

---

## 📊 2. Custom Business Metrics (AI Modeli + İş Değeri)

DogStatsD üzerinden gönderilecek metrikler:

- `aero.model.rul_prediction`  
- `aero.model.drift_score`  
- `aero.data.sensor_anomaly_count`  
- `aero.business.saved_cost` (sunumda en çok etkiyi yaratır)

---

## 🔗 3. Log Correlation

Amaç: Loglar → Trace’lerle otomatik eşleşsin.

**Yapılacaklar:**

- Tüm logları **JSON formatında** bas  
- İçine:  
  - `dd.trace_id`  
  - `dd.span_id`  
  ekle

Datadog bunları görünce trace/log otomatik bağlanır.

---

## 🎥 4. RUM + Session Replay (Frontend İzleme)

- Next.js tarafına  
@datadog/browser-rum

paketi kurulacak.

- Session Replay açılacak →  
Jüri user hareketlerini **video gibi** görecek.

---

## 🚨 5. SLO + Alerting

### SLO’lar
- **Latency SLO:** %99 istek < 500ms  
- **Availability SLO:** %99.9 uptime  

### Alert Örneği
- `aero.model.rul_prediction < 10`  
→ Slack veya Email uyarısı  
("Motor ömrü kritik seviyede!")

---

# 🤖 CLAUDE İÇİN HAZIR “DATADOG PROMPT” (KOPYALA-SAKLA)

Claude’a Go veya Python kodu yazdırırken **her defasında ekle**:

Datadog Implementation Requirements:

Tracing: ddtrace kullanarak Kafka Header Propagation uygula.
Trace ID'yi Kafka mesajına enjekte et (Producer) ve oradan oku (Consumer).

Metrics: DogStatsD kullanarak custom metrik gönder
(aero.xyz namespace'i ile).

Logs: Logları JSON formatında bas ve içine dd.trace_id enjekte edildiğinden emin ol.

Tagging: Tüm metriklere ve tracelere
env:production,
service:aero-sense,
version:1.0
etiketlerini ekle.


# DATA IMP
# ✈️ Ekstra Veri Katmanları ile “Impact + Creativity” Stratejisi  
**Tarih:** 7 Aralık 2025  
**Hedef:** Google Cloud Hackathon (Datadog & Confluent Tracks)  
**Durum:** Bu doküman projeyi *uçuracak* yaratıcı veri stratejisini anlatır. Hiçbir şey atlanmamıştır.

---

# ✈️ 1. GERÇEK UÇUŞ VERİSİ — *OpenSky Network API*  
### 🎯 Neden Game Changer?
Sadece NASA simülasyon verisini kullanmak *sıradan bir hackathon projesi* yaratır.  
Ama **gerçek zamanlı uçuş verisini** NASA veri seti ile senkronize edince ortaya *dijital ikiz (digital twin)* çıkar.

### 📡 API Kaynağı  
**OpenSky Network API — Ücretsiz**

### 🧠 Fikir  
Python (ya da Go) ile OpenSky API’ye gidiyoruz.  
“Şu an havada hangi uçak var? Örneğin BA117 (London → New York)”  
Bir uçak seçiyoruz.  

### 🛫 Senaryo  
OpenSky’dan gelen veriler:
- Anlık *irtifa* (altitude)
- Hız
- Koordinat (lat/lon)
- Tırmanma oranı (vertical rate)

Simülasyon (NASA) verisi:
- Motor sensörleri (temperature, pressure, fan speed…)

### 🔥 Bağlantı (Fusion)
- **Uçak tırmanıyorsa** → NASA verisinden “Climb mode” satırlarını
- **Cruise'ta ise** → “Cruise mode” satırlarını  
- Motor yük altındaysa → NASA sensörlerinde buna uygun veriler

### 🏆 Jüriye Mesaj
> “Biz sadece simülasyon oynatmıyoruz; şu an Atlantik üzerinde uçan gerçek bir uçağın **dijital ikizini** oluşturuyoruz.”

Bu hackathonda seni öne taşıyacak en etkili *creativity* hamlesi budur.

---

# 📰 2. Web Scraping — *Aviation Herald*  
### 🎯 Amaç: "Risk Intelligence Layer"

**Kaynak:** The Aviation Herald  
**Teknik:** Python + BeautifulSoup

### 🛠️ Nasıl Çalışacak?
- Script son 24 saatin haberlerini tarar.
- “Engine vibration”, “fuel pressure anomaly” gibi anahtar kelimeleri arar.
- Bir motor tipiyle ilgili yeni bir olay varsa → sistem bunu “context” olarak alır.

### 🧠 Impact
> “Dünyadaki güncel arıza trendlerini takip edip bakım ekiplerini proaktif uyarıyoruz.”

Bu, “AI + Observability + Proactive Insights” üçlüsünün en üst noktasıdır.

---

# 🔄 3. Güncellenmiş Veri Birleştirme Stratejisi — *Fusion Engine*  
Artık proje sadece “CSV okuyan bir backend” değil.  
**3 Farklı veri kaynağını gerçek zamanlı birleştiren bir engine yazıyoruz.**

| Veri Kaynağı | Tür | Rolü | Jüriye Etkisi |
|--------------|-----|------|----------------|
| **NASA CMAPSS** | Statik CSV | Motor iç sensörleri | Bilimsel doğruluk |
| **OpenSky API** | Canlı | Uçağın iskeleti: konum, hız, irtifa | Gerçekçilik, şaşırtıcı canlılık |
| **OpenWeatherMap** | Canlı | Dış ortam & hava etkileri | Çevresel farkındalık |

Bu üçlü bir araya geldiğinde:
- Motor yükünü OpenSky belirliyor  
- Motor davranışını NASA veri seti temsil ediyor  
- Dış koşulları OpenWeather belirliyor

**Buna hackathonda “Fusion Engine” diyeceğiz.**

---

# 🛠️ 4. Teknik Olarak Nasıl Yaparız? (Basit!)  

## 📍 Adım 1 — OpenSky Wrapper
Go ingestion servisine küçük bir fonksiyon eklenir:

```go
func fetchAircraft() Aircraft {
    // Istanbul üstündeki uçakları sorgula
    // Bir tane uçak seç
    // Latitude, longitude, altitude, verticalRate döndür
}

📍 Adım 2 — “Flight Mode” Belirleme

if altitudeIncreasing {
    mode = "CLIMB"
} else if altitudeStable {
    mode = "CRUISE"
} else {
    mode = "DESCEND"
}

📍 Adım 3 — NASA Verisinden Mod’a Uygun Satır Çekme
Python tarafında da yapılabilir:

def get_cmapss_slice(mode):
    if mode == "CLIMB":
        return df[df["alt"] < 5000]
    if mode == "CRUISE":
        return df[df["alt"] > 20000]
📍 Adım 4 — Hepsini Tek Mesaja Birleştirme
Go ingestion servisi:

{
  "flight": {
    "lat": 41.28,
    "lon": 29.0,
    "alt": 25000
  },
  "weather": {
    "temp": -52,
    "wind_speed": 34
  },
  "engine": {
    "n1": 0.92,
    "temp": 740,
    "fuel_flow": 0.84
  }
}

# 🚀 Uçağın Dijital İkizi — Mükemmel Sunum Anlatısı

## 🔄 Event Flow (Basit ve Net)
- Bu mesaj **Kafka’ya** gider.  
- **Python AI servisi** bu mesajı tüketir.  
- **Datadog Trace ID**, Kafka header üzerinden **uçtan uca** taşınır.  
  → Monitoring + Observability %100

---

## 💡 5. Neden Bu Strateji? — *Jüriye Anlatacağın Altın Cümle*
> **“Gerçek motor verileri ticari sır olduğu için NASA’nın CMAPSS fizik modelini kullandık.  
> Ancak bu modeli statik bırakmadık; OpenSky (gerçek uçuş) + OpenWeather (gerçek hava) verilerini anlık olarak birleştirip uçağın **dijital ikizini** oluşturduk.”**

Bu cümle **seni diğer takımlardan ayıran kırılma noktasıdır**.

📌 Sadece CSV ile çalışanlardan **10 kat** öndesin.

---

# 🧩 6. Projedeki Veri Rolleri — *Final & Sunuma Hazır*
Uçağı yaşayan bir varlık gibi düşün: İskelet, deri, iç organlar.

## 🦴 1. İskelet (Gerçek — Canlı Veri)
- **Kaynak:** OpenSky Network  
- **Rol:** Uçağın pozisyon ve hareket durumu  
- **Etkisi:** “Sistem şu an New York üzerindeki uçuşları izliyor.”

## 🧥 2. Deri (Gerçek — Canlı Veri)
- **Kaynak:** OpenWeatherMap  
- **Rol:** Çevresel koşullar  
- **Etkisi:** “Hava -50°C olduğu için motor verim seviyesi değişiyor.”

## 🔧 3. İç Organlar (Simülasyon — NASA)
- **Kaynak:** CMAPSS (NASA fizik tabanlı motor modeli)  
- **Rol:** Motor sensör verileri  
- **Etkisi:** “Gerçek motor davranışını NASA'nın fiziksel modeliyle sürdürüyoruz.”

---

# 🏁 SONUÇ — *Jürilik Özet*
- ✓ **Impact:** %100  
- ✓ **Creativity:** %100  
- ✓ **Datadog + Kafka + Vertex AI** için kusursuz veri akışı  
- ✓ Jüri önünde **teknik + hikâye anlatısı** mükemmel uyum


---

# 🔚 SON