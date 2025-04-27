# Conversation Analysis API

Bu proje, müşteri ve temsilci arasındaki konuşmaları analiz eden bir API sağlar. Kullanıcıların mesajlarını analiz ederek, konuşmacının rolünü, niyetini ve duygusal tonunu belirler.

## Özellikler

- **Konuşma Analizi**: Kullanıcı ve temsilci mesajlarını analiz ederek rol, niyet ve duygu tespiti yapar.
- **API Anahtarı Doğrulama**: Güvenlik için API anahtarı doğrulaması.
- **JSON Formatında Çıktı**: Analiz sonuçlarını yapılandırılmış JSON formatında döner.
- **Loglama**: Konuşma ve analiz sonuçlarını loglama desteği.

## Kurulum

### Yerel Kurulum

1. Projeyi klonlayın:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Gerekli bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```

3. Servisi başlatın:
   ```bash
   python api.py
   ```

### Docker ile Kurulum (Önerilen)

Bu proje, prometa-ui ve prometa-async-logging-service ile birlikte Docker Compose kullanarak çalıştırılabilir.

1. Gerekli diğer servis repoları için setup betiğini çalıştırın:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. Docker Compose ile tüm servisleri başlatın:
   ```bash
   docker-compose up -d
   ```

3. Servislere aşağıdaki adreslerden erişebilirsiniz:
   - UI: http://localhost:8501
   - Intent Service: http://localhost:7002
   - Logging Service: http://localhost:8001
   - PostgreSQL: localhost:5432

4. Servisleri durdurmak için:
   ```bash
   docker-compose down
   ```

5. Tüm container ve volumeleri kaldırmak için:
   ```bash
   docker-compose down -v
   ```

## Kullanım

### API Endpoint

- **POST** `/api/v1/chat/analyze`

#### Örnek İstek
```json
{
  "messages": [
    {
      "role": "user",
      "message": "Merhaba! Planımı yükseltmek istiyorum."
    },
    {
      "role": "agent",
      "message": "Tabii ki! Hangi özellikleri arıyorsunuz?"
    }
  ],
  "session_identifier": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### Örnek Yanıt
```json
{
  "bot_message": "Analiz tamamlandı.",
  "session_id": "123e4567-e89b-12d3-a456-426614174000",
  "analysis": [
    {
      "role": "user",
      "sentence": "Merhaba! Planımı yükseltmek istiyorum.",
      "sentiment": "positive",
      "intent": "plan_change"
    },
    {
      "role": "agent",
      "sentence": "Tabii ki! Hangi özellikleri arıyorsunuz?",
      "sentiment": "neutral",
      "intent": "inquiry"
    }
  ]
}
```



## Proje Yapısı

- **api/**: API ile ilgili route, schema ve servisler.
- **chatbot/**: Chatbot motoru ve mesaj formatlayıcı.
- **prompt/**: Sistem prompt tanımları.
- **util/**: Yardımcı araçlar (loglama, istemci vb.).
- **test/**: Test dosyaları.
- **config/**: config dosyaları. https://aistudio.google.com/prompts/new_chat buradan ücretsiz api key alabilirsiniz google hesabınız ile. API key'ini configdeki (default.json) api_key alanına yazmanız gerekiyor. API key'i ücretsiz olarak kullandığınızda google'nin verinizi işleme hakkı oluyor FYI.

#### config örneği
```json
{ 
    "app": {
      "port": 7002,
      "version": "v1",
      "api_key": "temp_secret123"
    },
    "gemini": {
        "api_key": "your api key",
        "model": "gemini-2.0-flash",
        "max_tokens": 8192
    },
    "logging_service_url":"http://localhost:8001",
    "ui_url":"http://localhost:8002"
}
```

#### Konfigürasyon Açıklamaları

- **app**: Uygulama ayarları
  - **port**: API'nin çalışacağı port numarası (7002)
  - **version**: API sürüm numarası (v1)
  - **api_key**: API güvenlik anahtarı, istemcilerin API'ye erişimini doğrulamak için kullanılır

- **gemini**: Google Gemini AI modeli ayarları
  - **api_key**: Google AI Studio'dan alınan API anahtarı
  - **model**: Kullanılacak Gemini modeli ('gemini-2.0-flash')
  - **max_tokens**: Bir istekte kullanılabilecek maksimum token sayısı (8192)

- **logging_service_url**: Loglama servisinin URL'si, analiz sonuçlarını ve konuşma kayıtlarını depolar
  
- **ui_url**: Kullanıcı arayüzü servisinin URL'si, istemci uygulamasına erişim için kullanılır

## Gereksinimler

- Python 3.11
- Bağımlılıklar için `requirements.txt` dosyasını kontrol edin.

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır.