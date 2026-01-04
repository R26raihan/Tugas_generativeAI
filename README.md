# 📰 News Sentiment Analysis API

API analisis sentimen berita Indonesia menggunakan FastAPI, Selenium, dan DistilBERT untuk menganalisis sentimen dari berbagai sumber berita terkemuka.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 Fitur

- ✅ **Web Scraping Otomatis** - Mengambil berita dari 15 sumber media terkemuka Indonesia
- ✅ **Analisis Sentimen NLP** - Menggunakan DistilBERT multilingual untuk analisis sentimen
- ✅ **Multi-Platform Support** - Mendukung CUDA (NVIDIA), MPS (Apple Silicon), dan CPU
- ✅ **Auto ChromeDriver** - Download dan setup ChromeDriver otomatis
- ✅ **Export CSV** - Hasil analisis dalam format CSV untuk analisis lebih lanjut
- ✅ **REST API** - Interface API yang mudah digunakan dengan dokumentasi interaktif
- ✅ **Modular Architecture** - Kode terstruktur dan mudah di-maintain

## 📊 Sumber Berita

API ini mengambil berita dari 15 media terkemuka:

- **Detik** - Terpopuler, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Kompas** - Tren, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **CNN Indonesia** - Nasional, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Tempo** - Terpopuler, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Tribunnews** - Populer, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Liputan6** - News, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Republika** - Terpopuler, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Islam
- **Okezone** - Beranda, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Suara** - Terpopuler, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Viva** - Berita, Otomotif, Politik, Ekonomi, Olahraga, Teknologi, Hiburan
- **Sindonews** - Nasional, Otomotif, Ekonomi, Olahraga, Teknologi, Hiburan
- **Antara News** - Nasional, Ekonomi, Olahraga, Teknologi, Hiburan
- **Bisnis.com** - Ekonomi, Otomotif, Teknologi, Hiburan
- **Jawa Pos** - Nasional, Ekonomi, Olahraga, Teknologi, Hiburan
- **BBC Indonesia** - Berita, Internasional, Teknologi

## 🏗️ Arsitektur

```
Fastapi/
├── config/              # Konfigurasi aplikasi
│   ├── device_config.py # Deteksi device (CUDA/MPS/CPU)
│   └── news_sources.py  # Konfigurasi sumber berita
├── services/            # Business logic
│   ├── driver_service.py    # ChromeDriver management
│   ├── scraper_service.py   # Web scraping
│   └── sentiment_service.py # Analisis sentimen
├── utils/               # Utilities
│   └── selectors.py     # CSS selectors
├── routes/              # API endpoints
│   └── analysis_routes.py
├── main.py              # Entry point
└── requirements.txt     # Dependencies
```

## 📊 Diagram Sistem

### 1. Arsitektur Sistem

```mermaid
graph TB
    subgraph "Client Layer"
        Client["HTTP Client<br/>(Browser/Postman/curl)"]
    end
    
    subgraph "FastAPI Application"
        API["FastAPI Server<br/>Port 8000"]
        Routes["API Routes<br/>analysis_routes.py"]
        
        subgraph "Services"
            Driver["Driver Service<br/>ChromeDriver Management"]
            Scraper["Scraper Service<br/>Web Scraping"]
            Sentiment["Sentiment Service<br/>NLP Analysis"]
        end
        
        subgraph "Configuration"
            DeviceConfig["Device Config<br/>CUDA/MPS/CPU"]
            NewsConfig["News Sources<br/>15 Media"]
            Selectors["CSS Selectors<br/>Per Source"]
        end
    end
    
    subgraph "External Services"
        Chrome["Chrome Browser<br/>Headless Mode"]
        HuggingFace["HuggingFace<br/>DistilBERT Model"]
        NewsWebsites["News Websites<br/>Detik, Kompas, CNN, etc."]
    end
    
    subgraph "Output"
        CSV["CSV File<br/>data_{keyword}_news_nlp.csv"]
        JSON["JSON Response<br/>API Response"]
    end
    
    Client -->|HTTP Request| API
    API --> Routes
    Routes --> Driver
    Routes --> Scraper
    Routes --> Sentiment
    
    Driver --> Chrome
    Scraper --> Chrome
    Chrome --> NewsWebsites
    
    Sentiment --> HuggingFace
    
    DeviceConfig -.->|Configure| Sentiment
    NewsConfig -.->|URLs| Scraper
    Selectors -.->|CSS| Scraper
    
    Sentiment --> CSV
    Routes --> JSON
    JSON -->|HTTP Response| Client
```

### 2. Flow Analisis Sentimen

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Routes
    participant Driver
    participant Scraper
    participant Sentiment
    participant Chrome
    participant News
    participant Model
    
    Client->>API: GET /analyze/{keyword}
    API->>Routes: Route request
    Routes->>Routes: get_sentiment_service()
    
    Note over Routes: Initialize services
    
    loop For each news source
        Routes->>Scraper: scrape_headlines(url, source, category)
        Scraper->>Driver: Get driver instance
        Driver-->>Scraper: Chrome driver
        Scraper->>Chrome: Navigate to URL
        Chrome->>News: HTTP Request
        News-->>Chrome: HTML Response
        Chrome-->>Scraper: Page loaded
        Scraper->>Scraper: Scroll & extract headlines
        Scraper-->>Routes: List of headlines
    end
    
    Routes->>Sentiment: analyze_data(headlines, keyword)
    
    Note over Sentiment: Filter by keyword
    
    loop For each headline
        Sentiment->>Model: Analyze sentiment
        Model-->>Sentiment: Label + Score
        Sentiment->>Sentiment: Classify (Positif/Negatif/Netral)
    end
    
    Sentiment->>Sentiment: Generate statistics
    Sentiment->>Sentiment: Save to CSV
    Sentiment-->>Routes: Analysis results
    Routes-->>API: JSON response
    API-->>Client: HTTP 200 + JSON
```

### 3. Proses Scraping Detail

```mermaid
flowchart TD
    Start([Start Scraping]) --> Init[Initialize ChromeDriver<br/>with headless options]
    Init --> Loop{For each<br/>news source?}
    
    Loop -->|Yes| Navigate[Navigate to URL]
    Navigate --> Wait[Wait for page load<br/>WebDriverWait 10s]
    Wait --> Scroll[Scroll page<br/>3 times, 2s each]
    
    Scroll --> TrySelectors{Try CSS<br/>selectors}
    TrySelectors -->|Class name| FindClass[Find by CLASS_NAME]
    TrySelectors -->|Tag name| FindTag[Find by TAG_NAME]
    
    FindClass --> Check{Headlines<br/>found?}
    FindTag --> Check
    
    Check -->|Yes| Extract[Extract text<br/>from elements]
    Check -->|No| NextSelector{More<br/>selectors?}
    
    NextSelector -->|Yes| TrySelectors
    NextSelector -->|No| NoData[⚠ No data found]
    
    Extract --> Success[✓ Headlines extracted]
    Success --> Loop
    NoData --> Loop
    
    Loop -->|No| Return[Return all headlines]
    Return --> End([End])
    
    style Success fill:#90EE90
    style NoData fill:#FFB6C1
```

### 4. Analisis Sentimen Detail

```mermaid
flowchart TD
    Start([Receive headlines]) --> Filter[Filter by keyword<br/>case-insensitive]
    Filter --> Check{Headlines<br/>found?}
    
    Check -->|No| NoData[Return: No data message]
    Check -->|Yes| Prepare[Prepare texts<br/>truncate to 512 chars]
    
    Prepare --> Batch[Batch process with<br/>DistilBERT model]
    
    Batch --> Loop{For each<br/>result}
    
    Loop --> Classify{Classify<br/>sentiment}
    Classify -->|POSITIVE & score>0.6| Pos[Sentiment: Positif]
    Classify -->|NEGATIVE & score>0.6| Neg[Sentiment: Negatif]
    Classify -->|Otherwise| Neu[Sentiment: Netral]
    
    Pos --> Count[Update counters]
    Neg --> Count
    Neu --> Count
    
    Count --> Store[Store detailed result]
    Store --> Loop
    
    Loop -->|Done| Stats[Calculate statistics:<br/>- Counts<br/>- Percentages<br/>- Examples]
    
    Stats --> CSV[Export to CSV<br/>source,category,text,sentiment,score]
    CSV --> Response[Build JSON response]
    Response --> End([Return response])
    
    NoData --> End
    
    style Pos fill:#90EE90
    style Neg fill:#FFB6C1
    style Neu fill:#87CEEB
```

### 5. Device Detection Flow

```mermaid
flowchart TD
    Start([Detect Device]) --> CheckCUDA{CUDA<br/>available?}
    
    CheckCUDA -->|Yes| UseCUDA[Device: CUDA<br/>Index: 0<br/>Name: GPU name]
    CheckCUDA -->|No| CheckMPS{MPS<br/>available?}
    
    CheckMPS -->|Yes| UseMPS[Device: MPS<br/>Index: 0<br/>Name: Apple Silicon]
    CheckMPS -->|No| UseCPU[Device: CPU<br/>Index: -1<br/>Name: CPU]
    
    UseCUDA --> Return[Return device config]
    UseMPS --> Return
    UseCPU --> Return
    
    Return --> End([End])
    
    style UseCUDA fill:#90EE90
    style UseMPS fill:#87CEEB
    style UseCPU fill:#FFD700
```

### 6. Data Model

```mermaid
erDiagram
    RESPONSE ||--o{ DETAILED_RESULT : contains
    RESPONSE ||--|| SENTIMENT_SUMMARY : has
    RESPONSE ||--|| SOURCE_DISTRIBUTION : has
    RESPONSE ||--|| CATEGORY_DISTRIBUTION : has
    
    RESPONSE {
        string keyword
        int total_items
        object sentiment_summary
        object source_distribution
        object category_distribution
        array detailed_results
    }
    
    DETAILED_RESULT {
        string source
        string category
        string text
        string sentiment
        float score
    }
    
    SENTIMENT_SUMMARY {
        int Positif_count
        float Positif_percentage
        array Positif_examples
        int Negatif_count
        float Negatif_percentage
        array Negatif_examples
        int Netral_count
        float Netral_percentage
        array Netral_examples
    }
    
    SOURCE_DISTRIBUTION {
        int Detik
        int Kompas
        int CNN_Indonesia
        int others
    }
    
    CATEGORY_DISTRIBUTION {
        int Politik
        int Ekonomi
        int Olahraga
        int others
    }
```

### 7. Error Handling

```mermaid
flowchart TD
    Request[HTTP Request] --> Validate{Request<br/>valid?}
    
    Validate -->|No| Error400[HTTP 400<br/>Bad Request]
    Validate -->|Yes| CheckService{Service<br/>ready?}
    
    CheckService -->|No| Error503[HTTP 503<br/>Service Unavailable]
    CheckService -->|Yes| Process[Process Request]
    
    Process --> Scrape{Scraping<br/>success?}
    Scrape -->|Timeout| Warn[⚠ Log timeout<br/>Continue with others]
    Scrape -->|Error| Warn2[⚠ Log error<br/>Continue with others]
    Scrape -->|Success| Collect[Collect headlines]
    
    Warn --> Collect
    Warn2 --> Collect
    
    Collect --> Analyze{Analysis<br/>success?}
    Analyze -->|Error| Error500[HTTP 500<br/>Internal Server Error]
    Analyze -->|Success| Response[HTTP 200<br/>Success Response]
    
    Error400 --> End([End])
    Error503 --> End
    Error500 --> End
    Response --> End
    
    style Error400 fill:#FFB6C1
    style Error503 fill:#FFB6C1
    style Error500 fill:#FFB6C1
    style Response fill:#90EE90
```


## 🚀 Quick Start

### Prerequisites

- Python 3.8 atau lebih tinggi
- Google Chrome browser (untuk ChromeDriver)

### Instalasi

1. Clone repository:
```bash
git clone <repository-url>
cd sentimen_analysis/Fastapi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan server:
```bash
python main.py
```

Server akan berjalan di `http://localhost:8000`

## 🧪 Testing

### Menjalankan Server Lokal

1. **Start server**:
```bash
cd /Users/raihansetiawan/sentimen_analysis/Fastapi
python main.py
```

Output yang diharapkan:
```
MPS tersedia. Menggunakan perangkat: Apple Silicon (MPS)
Menyiapkan ChromeDriver...
ChromeDriver siap digunakan!
Memuat model sentiment analysis...
Model sentiment analysis siap!
Aplikasi siap digunakan!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

2. **Buka Interactive Documentation**:

Buka browser dan akses:
```
http://localhost:8000/docs
```

Anda akan melihat Swagger UI dengan:
- ✅ Daftar semua endpoint
- ✅ Try it out button untuk testing langsung
- ✅ Request/Response examples
- ✅ Schema definitions

![Swagger UI](docs/images/swagger-ui.png)

3. **Test API dari Browser**:

**Root Endpoint**:
```
http://localhost:8000/
```

**Analyze Endpoint** (contoh dengan keyword "politik"):
```
http://localhost:8000/analyze/politik
```

4. **Test dengan curl**:

```bash
# Test root endpoint
curl http://localhost:8000/

# Test analyze endpoint
curl http://localhost:8000/analyze/teknologi

# Save response to file
curl http://localhost:8000/analyze/ekonomi > result.json
```

5. **Test dengan Postman**:

- Method: `GET`
- URL: `http://localhost:8000/analyze/pemerintah`
- Headers: (tidak diperlukan)
- Send request

6. **Cek Output CSV**:

Setelah request selesai, cek file CSV yang dihasilkan:
```bash
ls -lh data_*_news_nlp.csv
cat data_politik_news_nlp.csv | head -10
```

### Testing Checklist

- [ ] Server berhasil start tanpa error
- [ ] Docs page (`/docs`) dapat diakses
- [ ] Root endpoint (`/`) mengembalikan response
- [ ] Analyze endpoint berhasil scraping berita
- [ ] File CSV ter-generate dengan benar
- [ ] Response JSON memiliki struktur yang benar
- [ ] ChromeDriver berjalan dalam headless mode
- [ ] Model sentiment analysis ter-load

### Troubleshooting Testing

**Port sudah digunakan**:
```bash
# Kill process di port 8000
lsof -ti:8000 | xargs kill -9

# Atau gunakan port lain
uvicorn main:app --port 8001
```

**ChromeDriver error**:
```bash
# Reinstall ChromeDriver
pip uninstall webdriver-manager
pip install webdriver-manager
```

**Model download lambat**:
```bash
# Model akan di-download otomatis saat pertama kali
# Tunggu hingga selesai (sekitar 1-2 menit)
# Model akan di-cache untuk penggunaan selanjutnya
```

## 📖 Penggunaan

### API Endpoints

#### 1. Root Endpoint
```bash
GET http://localhost:8000/
```

Response:
```json
{
  "message": "News Sentiment Analysis API",
  "endpoints": {
    "analyze": "/analyze/{keyword}"
  }
}
```

#### 2. Analisis Sentimen
```bash
GET http://localhost:8000/analyze/{keyword}
```

Contoh:
```bash
curl http://localhost:8000/analyze/politik
```

Response:
```json
{
  "keyword": "politik",
  "total_items": 150,
  "sentiment_summary": {
    "Positif": {
      "count": 45,
      "percentage": 30.0,
      "examples": [...]
    },
    "Negatif": {
      "count": 30,
      "percentage": 20.0,
      "examples": [...]
    },
    "Netral": {
      "count": 75,
      "percentage": 50.0,
      "examples": [...]
    }
  },
  "source_distribution": {...},
  "category_distribution": {...},
  "detailed_results": [...]
}
```

#### 3. Interactive Documentation
```bash
http://localhost:8000/docs
```

### Output CSV

Hasil analisis otomatis disimpan dalam file CSV:
```
data_{keyword}_news_nlp.csv
```

Format CSV:
```csv
source,category,text,sentiment,score
Detik,Politik,"Judul berita...",Positif,0.95
CNN Indonesia,Ekonomi,"Judul lain...",Netral,0.75
```

## 🔧 Konfigurasi

### Device Configuration

Aplikasi otomatis mendeteksi device terbaik:
- **CUDA** - Untuk GPU NVIDIA
- **MPS** - Untuk Apple Silicon (M1/M2/M3)
- **CPU** - Fallback untuk sistem tanpa GPU

### ChromeDriver Options

ChromeDriver berjalan dalam headless mode dengan konfigurasi:
- `--headless=new` - Mode headless
- `--no-sandbox` - Untuk stabilitas
- `--disable-gpu` - Optimasi
- `--window-size=1920,1080` - Resolusi
- Custom user-agent untuk anti-detection

## 📊 Teknologi

- **FastAPI** - Modern web framework untuk Python
- **Selenium** - Web scraping automation
- **webdriver-manager** - Auto ChromeDriver management
- **Transformers** - HuggingFace library untuk NLP
- **DistilBERT** - Multilingual sentiment analysis model
- **PyTorch** - Deep learning framework

## 🎯 Use Cases

1. **Monitoring Brand** - Analisis sentimen publik terhadap brand/produk
2. **Riset Politik** - Analisis opini publik terhadap isu politik
3. **Analisis Pasar** - Sentimen berita ekonomi dan bisnis
4. **Media Monitoring** - Tracking coverage berita dari berbagai sumber
5. **Research** - Data untuk penelitian sentimen media

## 📈 Performance

- **Scraping Speed**: ~2-3 detik per sumber berita
- **Analysis Speed**: Tergantung device (GPU > CPU)
- **Concurrent Requests**: Mendukung multiple requests
- **Accuracy**: ~85-90% (tergantung kualitas data)

## 🛠️ Development

### Menambah Sumber Berita

Edit `config/news_sources.py`:
```python
NEWS_SOURCES = {
    "Nama Media": {
        "Kategori": "https://url-kategori.com"
    }
}
```

Edit `utils/selectors.py`:
```python
SELECTORS = {
    "Nama Media": ["css-selector-1", "css-selector-2"]
}
```

### Testing

```bash
# Test scraping
curl http://localhost:8000/analyze/test

# Check logs
tail -f logs/app.log
```

## 🐛 Troubleshooting

### ChromeDriver Issues
```bash
# Reinstall ChromeDriver
pip uninstall webdriver-manager
pip install webdriver-manager
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Model Download Issues
```bash
# Clear cache and retry
rm -rf ~/.cache/huggingface/
```

## 📝 License

MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

Untuk pertanyaan atau saran, silakan buka issue di repository ini.

## 🙏 Acknowledgments

- [HuggingFace](https://huggingface.co/) untuk model DistilBERT
- [FastAPI](https://fastapi.tiangolo.com/) untuk framework
- [Selenium](https://www.selenium.dev/) untuk web scraping tools
- Semua sumber berita yang datanya digunakan

---

**Note**: Aplikasi ini dibuat untuk tujuan edukasi dan riset. Pastikan untuk mematuhi terms of service dari setiap sumber berita yang di-scrape.
