
# Voice-to-Cart (FastAPI)

Servicio backend que recibe mensajes (texto o voz) desde WhatsApp y chat web, interpreta la intención con un LLM desacoplado y agrega productos a un carrito de compras.

## 🧱 Arquitectura (alto nivel)

```mermaid
flowchart LR
  A[Canales\nWhatsApp / Chat Web] -->|/message| B[FastAPI]
  B --> C[MessageProcessor]
  C --> D[ConfigManager]
  C --> E[LLMEngine (Interface)]
  E <---> E1[DummyLLM / OpenAI / Gemini]
  C --> F[CartService]
  D -->|reglas/tono| E
  B -->|/config| D
  B -->|/cart| F
```

## 📁 Estructura de carpetas

```
app/
  main.py
  schemas.py
  config.py
  services/cart.py
  processing/message_processor.py
  llm/base.py
  llm/dummy.py
tests/
  test_endpoints.py
  test_processor.py
config.example.yaml
```

## ⚙️ Ejemplo de configuración (YAML)

```yaml
tone: "amigable"
constraints:
  no_out_of_stock: true
  max_items_per_message: 20
preferences:
  preferred_brands: ["Acme", "La Serenísima"]
  inclusive_language: true
  units_default: "unidad"
parsing:
  quantity_words:
    uno: 1
    una: 1
    dos: 2
    tres: 3
    media: 0.5
```

## 🔁 Flujo de ejemplo

1. Cliente envía: *"Agregá 2 leches descremadas La Serenísima y 1 pan integral Fargo"*.
2. `POST /message` recibe `{channel:"web", type:"text", text:"..."}`.
3. `MessageProcessor` aplica configuración dinámica y llama al `LLMEngine`.
4. El motor devuelve una lista estructurada de artículos (`name`, `quantity`, `variant`, `brand`, `notes`).
5. `CartService` agrega los artículos al carrito del `user_id` y retorna estado de detecciones + carrito.
6. `GET /cart?user_id=abc` muestra el estado del carrito.

## ▶️ Ejecutar

```bash
uvicorn app.main:app --reload
```

Abrí Swagger en: http://localhost:8000/docs

## 🧪 Pruebas

```bash
pytest
```
