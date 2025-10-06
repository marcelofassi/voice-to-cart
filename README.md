# voice-to-cart (backend)

Un backend de referencia con FastAPI para recibir mensajes (texto/voz) desde WhatsApp o chat web, interpretar intención con un LLM desacoplado y extraer artículos para un carrito mockeado.

## Diagrama de arquitectura (alto nivel)

```mermaid
flowchart LR
  subgraph Channels
    A1[WhatsApp Webhook] -->|/message| B
    A2[Web Chat] -->|/message| B
  end

  subgraph API[FastAPI API Layer]
    B[/POST /message/]
    C[/POST /config/]
    D[/GET /cart/]
  end

  B --> P[Message Processor]
  C --> CFG[Config Manager]
  D --> CART[Cart Service]

  P -->|load| CAT[Product Catalog]
  P -->|uses| LLM[LLM Engine (Interface)]
  P --> CART

  LLM <..> CFG
  P <..> CFG

  CART -->|simulate| ECOM[(Mock Ecommerce API)]
  CAT <--> ECOM
```

**Fallback ASCII:**

Channels(WhatsApp/Web) -> FastAPI(/message,/config,/cart)
/message -> Processor -> (Catalog, LLM Engine via interface, Config)
Processor -> Cart Service -> Mock Ecommerce API
/config -> Config Manager (dinámico)
/cart -> Cart Service
```

## Ejecución local

```bash
uvicorn app.main:app --reload
```

Abrir Swagger UI en: http://localhost:8000/docs

## Pruebas

```bash
pytest -q
```
