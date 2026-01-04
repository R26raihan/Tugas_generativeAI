# News Sentiment Analysis API - System Documentation

Dokumentasi lengkap sistem analisis sentimen berita dengan diagram Mermaid.

---

## 1. Arsitektur Sistem

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

---

## 2. Struktur Folder

```mermaid
graph LR
    subgraph "Fastapi/"
        Main["main.py<br/>Entry Point"]
        Req["requirements.txt<br/>Dependencies"]
        
        subgraph "config/"
            DC["device_config.py"]
            NS["news_sources.py"]
            CI["__init__.py"]
        end
        
        subgraph "services/"
            DS["driver_service.py"]
            SS["scraper_service.py"]
            SentS["sentiment_service.py"]
            SI["__init__.py"]
        end
        
        subgraph "utils/"
            Sel["selectors.py"]
            UI["__init__.py"]
        end
        
        subgraph "routes/"
            AR["analysis_routes.py"]
            RI["__init__.py"]
        end
    end
    
    Main -.->|imports| config/
    Main -.->|imports| services/
    Main -.->|imports| routes/
    
    routes/ -.->|uses| services/
    routes/ -.->|uses| config/
    services/ -.->|uses| utils/
    services/ -.->|uses| config/
```

---

## 3. Flow Analisis Sentimen

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

---

## 4. Proses Scraping Detail

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

---

## 5. Analisis Sentimen Detail

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

---

## 6. Dependency Injection Pattern

```mermaid
graph TB
    subgraph "Startup Event"
        Start[Application Startup] --> DetectDevice[Detect Device<br/>CUDA/MPS/CPU]
        DetectDevice --> InitDriver[Initialize ChromeDriver<br/>with options]
        InitDriver --> InitSentiment[Initialize SentimentService<br/>with device_index]
        InitSentiment --> Ready[Application Ready]
    end
    
    subgraph "Request Handling"
        Request[HTTP Request] --> Dependency[get_sentiment_service<br/>FastAPI Depends]
        Dependency --> Check{Service<br/>initialized?}
        Check -->|No| Error503[HTTP 503<br/>Service not ready]
        Check -->|Yes| Inject[Inject service<br/>into endpoint]
        Inject --> Process[Process request]
    end
    
    Ready -.->|Global variable| Check
    
    style Ready fill:#90EE90
    style Error503 fill:#FFB6C1
```

---

## 7. Device Detection Flow

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

---

## 8. ChromeDriver Options

```mermaid
mindmap
    root((ChromeDriver<br/>Options))
        Headless Mode
            --headless=new
            Run without GUI
        Stability
            --no-sandbox
            --disable-dev-shm-usage
            --disable-gpu
        Window
            --window-size=1920,1080
            Full HD resolution
        Anti-Detection
            --user-agent
            Custom UA string
            --disable-blink-features
            AutomationControlled
            excludeSwitches
            enable-automation
        Performance
            useAutomationExtension: false
            Faster startup
```

---

## 9. Data Model

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

---

## 10. API Endpoints

```mermaid
graph LR
    subgraph "API Endpoints"
        Root["GET /<br/>Root endpoint"]
        Docs["GET /docs<br/>Swagger UI"]
        OpenAPI["GET /openapi.json<br/>OpenAPI spec"]
        Analyze["GET /analyze/{keyword}<br/>Main analysis endpoint"]
    end
    
    Root -->|Returns| Info["API info<br/>& endpoints list"]
    Docs -->|Shows| UI["Interactive<br/>documentation"]
    OpenAPI -->|Returns| Spec["API<br/>specification"]
    Analyze -->|Returns| Results["Sentiment<br/>analysis results"]
    
    Analyze -.->|Triggers| Scraping["Web scraping<br/>process"]
    Analyze -.->|Triggers| Analysis["Sentiment<br/>analysis"]
    Analyze -.->|Generates| CSV["CSV file<br/>output"]
```

---

## 11. Error Handling

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

---

## 12. Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        LB["Load Balancer<br/>nginx/traefik"]
        
        subgraph "Application Servers"
            App1["FastAPI Instance 1<br/>Port 8000"]
            App2["FastAPI Instance 2<br/>Port 8001"]
            App3["FastAPI Instance 3<br/>Port 8002"]
        end
        
        subgraph "Chrome Instances"
            Chrome1["ChromeDriver 1<br/>Headless"]
            Chrome2["ChromeDriver 2<br/>Headless"]
            Chrome3["ChromeDriver 3<br/>Headless"]
        end
        
        subgraph "ML Models"
            Model["DistilBERT Model<br/>Cached locally"]
        end
        
        subgraph "Storage"
            CSV1["CSV Files<br/>Instance 1"]
            CSV2["CSV Files<br/>Instance 2"]
            CSV3["CSV Files<br/>Instance 3"]
            SharedStorage["Shared Storage<br/>NFS/S3"]
        end
    end
    
    Internet["Internet"] --> LB
    LB --> App1
    LB --> App2
    LB --> App3
    
    App1 --> Chrome1
    App2 --> Chrome2
    App3 --> Chrome3
    
    App1 -.->|Load| Model
    App2 -.->|Load| Model
    App3 -.->|Load| Model
    
    App1 --> CSV1
    App2 --> CSV2
    App3 --> CSV3
    
    CSV1 -.->|Sync| SharedStorage
    CSV2 -.->|Sync| SharedStorage
    CSV3 -.->|Sync| SharedStorage
    
    Chrome1 --> NewsWebsites["News Websites"]
    Chrome2 --> NewsWebsites
    Chrome3 --> NewsWebsites
```

---

## Summary

Sistem ini menggunakan:
- **FastAPI** untuk REST API
- **Selenium + ChromeDriver** untuk web scraping
- **DistilBERT** untuk analisis sentimen
- **Modular architecture** untuk maintainability
- **Dependency injection** untuk service management
- **Multi-platform support** (CUDA/MPS/CPU)
- **CSV export** untuk hasil analisis
