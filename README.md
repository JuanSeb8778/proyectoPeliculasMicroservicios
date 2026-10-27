# 🎬 ReelHub — Plataforma de Películas con Microservicios

Plataforma para gestionar películas, usuarios, reseñas y listas personales, construida con una **arquitectura de microservicios políglota** (Java, Node.js y Python). Incluye un **agente de IA con Google Gemini** que responde preguntas sobre el catálogo usando el **Model Context Protocol (MCP)**, con una interfaz de chat en React.

![Java](https://img.shields.io/badge/Java%2021-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=nodedotjs&logoColor=white)
![Express](https://img.shields.io/badge/Express-000000?style=flat-square&logo=express&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)

## 📐 Arquitectura

```
                         ┌───────────────────────────┐
                         │  UI de chat (React)       │
                         └─────────────┬─────────────┘
                                       ▼
                         ┌───────────────────────────┐      ┌──────────────┐
                         │ Agente IA (FastAPI)       │ ───▶ │ Google Gemini│
                         │   └─ cliente MCP          │      └──────────────┘
                         └─────────────┬─────────────┘
                                       ▼ MCP (stdio)
                         ┌───────────────────────────┐      ┌──────────────┐
                         │ Servidor MCP (Python)     │ ───▶ │  PostgreSQL  │
                         └───────────────────────────┘      └──────────────┘

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ movies           │ │ userMovieList    │ │ users            │ │ reviews          │
│ Node.js/Express  │ │ Node.js/Express  │ │ Spring Boot      │ │ Spring Boot      │
│ :3001            │ │ :3002            │ │ MongoDB :8080    │ │ JPA + H2 :8081   │
└──────────────────┘ └──────────────────┘ └──────────────────┘ └──────────────────┘
```

| Servicio | Tecnología | Responsabilidad | Puerto |
|---|---|---|---|
| `moviesMicroservice` | Node.js · Express · Swagger | Catálogo de películas (CRUD) | `3001` |
| `userMovieListMicroservice` | Node.js · Express · Swagger | Listas de películas de cada usuario | `3002` |
| `usersMicroservice` | Java 21 · Spring Boot · MongoDB · MapStruct · Lombok | Gestión de usuarios | `8080` |
| `reviewsMicroservice` | Java 21 · Spring Boot · JPA · H2 · MapStruct · Lombok | Reseñas de películas | `8081` |
| `service aiAssistant/AGENT` | Python · FastAPI · Gemini · MCP · PostgreSQL | Agente de IA que consulta el catálogo | `8000` |
| `service aiAssistant/ui` | React | Chat con el agente de IA | `3000` |

## ✨ Funcionalidades

- CRUD de películas, usuarios y reseñas, con documentación **Swagger / OpenAPI** en cada servicio.
- Listas personales: agregar, actualizar y quitar películas de la lista de un usuario.
- Reseñas consultables por película y por usuario.
- **Agente de IA** con Gemini 2.0 Flash que entiende preguntas en lenguaje natural y usa herramientas MCP para consultar la base de datos: buscar películas, filtrarlas por año o género, agregarlas, actualizarlas o eliminarlas.
- Arquitectura en capas en cada servicio (rutas/controladores → servicios → repositorios → entidades) con DTOs y mappers.

## 🚀 Cómo ejecutarlo

### Requisitos
Node.js 18+, Java 21, Python 3.11+, MongoDB, PostgreSQL y una API key de [Google AI Studio](https://aistudio.google.com/).

### Servicios Node.js

```bash
cd moviesMicroservice        # o userMovieListMicroservice
npm install
node index.js
```

### Servicios Spring Boot

```bash
cd usersMicroservice         # o reviewsMicroservice
./gradlew bootRun
```

### Agente de IA

Crea el archivo `service aiAssistant/AGENT/.env` (no se sube al repositorio):

```env
GEMINI_API_KEY=tu_api_key
DB_NAME=nombre_bd
DB_USER=usuario
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432
```

```bash
cd "service aiAssistant/AGENT"
pip install -r requirements.txt
python main.py
```

### Interfaz de chat

```bash
cd "service aiAssistant/ui"
npm install
npm start
```

## 📡 Endpoints principales

| Servicio | Método | Ruta | Descripción |
|---|---|---|---|
| movies | `GET` / `POST` | `/movies` | Listar / crear películas |
| movies | `GET` / `PUT` / `DELETE` | `/movies/:id` | Consultar / actualizar / eliminar |
| userMovieList | `GET` | `/user-movie-list/:userId` | Lista de un usuario |
| userMovieList | `POST` | `/user-movie-list` | Agregar película a una lista |
| userMovieList | `PUT` / `DELETE` | `/user-movie-list/:userId/:movieId` | Actualizar / quitar de la lista |
| users | `GET` / `POST` | `/api/users` | Listar / crear usuarios |
| users | `GET` / `PUT` / `DELETE` | `/api/users/{id}` | Consultar / actualizar / eliminar |
| reviews | `GET` / `POST` | `/api/reviews` | Listar / crear reseñas |
| reviews | `GET` | `/api/reviews/movie/{movieId}` | Reseñas de una película |
| reviews | `GET` | `/api/reviews/user/{userId}` | Reseñas de un usuario |
| agente IA | `POST` | `/query` | Pregunta en lenguaje natural al agente |

La documentación interactiva está en `/api-docs` (Node.js) y `/swagger-ui.html` (Spring Boot).

## 👥 Autores

- **Juan Sebastián Ángel Ramírez** — [@JuanSeb8778](https://github.com/JuanSeb8778) · [LinkedIn](https://www.linkedin.com/in/juan-sebastian-angel-ramirez-44225b265/)
- [@Diyued](https://github.com/Diyued)

Proyecto académico del programa de Ingeniería de Software — **Institución Universitaria EAM**.
