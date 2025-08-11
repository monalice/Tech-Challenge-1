# API Pública de Consulta de Livros

Esta é uma API RESTful desenvolvida com FastAPI para consulta de dados de livros extraídos do site `books.toscrape.com`. Foi projetado para fornecer uma infraestrutura de dados escalável e reutilizável para futuros modelos de Machine Learning, especialmente em contextos de recomendação de livros.

## 📋 Sumário

- [Descrição do Projeto](#-descrição-do-projeto)
- [Arquitetura](#-arquitetura)
- [Funcionalidades](#-funcionalidades)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Execução do Projeto](#-execução-do-projeto)
- [Documentação da API](#-documentação-da-api)
- [Exemplos de Uso](#-exemplos-de-uso)

## 🎯 Descrição do Projeto

O projeto implementa uma API completa para consulta de livros com as seguintes características:

- **Web Scraping**: Extração automatizada de dados do site books.toscrape.com
- **API RESTful**: Endpoints bem estruturados seguindo padrões REST
- **Autenticação JWT**: Sistema seguro de autenticação e autorização
- **Banco de Dados**: Persistência com PostgreSQL
- **Docker**: Containerização para deploy fácil
- **Validação de Dados**: Validações robustas contra SQL injection
- **Documentação Automática**: Swagger UI e ReDoc integrados

## 🏗️ Arquitetura

A arquitetura do sistema segue o padrão de camadas bem definidas.
Além do diagrama abaixo, o plano arquitetural pode ser acessado em [Plano Arquitetural](https://docs.google.com/document/d/1Fq5yAo2G2wR5sPdnzCS7yubVXqXuCiIqjnrK0Pxo37k/edit?usp=sharing).

```text
┌─────────────────────┐      ┌──────────────────┐      ┌─────────────────────┐
│  books.toscrape.com │ ───► │   Web Scraper    │ ───► │  PostgreSQL Database│
└─────────────────────┘      └──────────────────┘      └─────────────────────┘
                                                                    │
                                                                    ▼
                                                        ┌─────────────────────┐
                                                        │  FastAPI Application│
                                                        │                     │
                                                        │  ┌───────────────┐  │
                                                        │  │ Routes Layer  │  │
                                                        │  ├───────────────┤  │
                                                        │  │Services Layer │  │
                                                        │  ├───────────────┤  │
                                                        │  │ Models Layer  │  │
                                                        │  ├───────────────┤  │
                                                        │  │ Utils Layer   │  │
                                                        │  └───────────────┘  │
                                                        └─────────────────────┘
                                                                    │
                                                                    ▼
                                                        ┌─────────────────────┐
                                                        │ JWT Authentication  │
                                                        └─────────────────────┘
                                                                    │
                                                                    ▼
                                                        ┌─────────────────────┐
                                                        │   API Endpoints     │
                                                        └─────────────────────┘
                                                                    │
                                                    ┌───────────────┼───────────────┐
                                                    ▼               ▼               ▼
                                        ┌─────────────────┐ ┌─────────────┐ ┌─────────────┐
                                        │ Swagger Docs    │ │Client Apps  │ │Future ML    │
                                        │                 │ │             │ │Models       │
                                        └─────────────────┘ └─────────────┘ └─────────────┘
```

### Componentes Principais:

- **Script de Web Scraping**: Extrai dados automaticamente do site fonte
- **Banco de Dados PostgreSQL**: Armazena livros e usuários
- **API FastAPI**: Serve os dados através de endpoints REST
- **Sistema de Autenticação**: JWT para proteção de rotas
- **Docker**: Containerização para ambiente isolado

## 🚀 Funcionalidades

### Públicas:
- ✅ Listar todos os livros com paginação
- ✅ Buscar livros por título e/ou categoria
- ✅ Obter detalhes de um livro específico
- ✅ Listar todas as categorias disponíveis
- ✅ Filtrar livros por faixa de preço
- ✅ Obter livros com melhor avaliação
- ✅ Health check da API

### Autenticadas:
- ✅ Registro de usuários
- ✅ Login com geração de token JWT
- ✅ Refresh de tokens
- ✅ Trigger manual de scraping

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- PostgreSQL (se executar sem Docker)

### 1. Clone o Repositório

```bash
git clone https://github.com/monalice/Tech-Challenge-1.git
cd Tech-Challenge-1
```

### 2. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto e preenche-lo com o modelo já existente, `env`

## 🚀 Execução do Projeto

### Opção 1: Docker (Recomendado)

```bash
# Construir e executar os containers
docker-compose up --build

# Executar em background
docker-compose up -d --build
```

### Opção 2: Execução Local

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar a aplicação
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Acessos:

#### 🌐 **Produção (Render):**
- **API**: https://tech-challenge-1-a0ab.onrender.com
- **Documentação Swagger**: https://tech-challenge-1-a0ab.onrender.com/api/v1/docs
- **Documentação ReDoc**: https://tech-challenge-1-a0ab.onrender.com/api/v1/redoc

#### 💻 **Desenvolvimento Local:**
- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/api/v1/docs
- **Documentação ReDoc**: http://localhost:8000/api/v1/redoc
- **PostgreSQL**: localhost:5432

## 📚 Documentação da API

### Health Check
- **GET** `/api/v1/health` - Verifica status da API

### Livros
- **GET** `/api/v1/books` - Lista livros com paginação
- **GET** `/api/v1/books/{book_id}` - Detalhes de um livro
- **GET** `/api/v1/books/search` - Busca livros por filtros
- **GET** `/api/v1/books/top-rated` - Livros com melhor avaliação
- **GET** `/api/v1/books/price-range` - Filtro por faixa de preço

### Categorias
- **GET** `/api/v1/categories` - Lista todas as categorias

### Autenticação
- **POST** `/api/v1/auth/register` - Registro de usuário
- **POST** `/api/v1/auth/login` - Login
- **POST** `/api/v1/auth/refresh` - Renovar token

### Scraping (Protegido)
- **POST** `/api/v1/scraping/trigger` - Executa scraping manual

## 📖 Exemplos de Uso

> **📌 Nota:** Os exemplos abaixo usam `localhost:8000` para desenvolvimento local. 
> Para produção, substitua por: `https://tech-challenge-1-a0ab.onrender.com`

### 1. Health Check

```bash
# Desenvolvimento
curl -X GET "http://localhost:8000/api/v1/health"

# Produção  
curl -X GET "https://tech-challenge-1-a0ab.onrender.com/api/v1/health"
```

**Resposta:**
```json
{
  "status": "ok",
  "books_count": 1000
}
```

### 2. Listar Livros com Paginação

```bash
curl -X GET "http://localhost:8000/api/v1/books?limit=5&offset=0"
```

**Resposta:**
```json
{
  "count": 5,
  "books": [
    {
      "id": 1,
      "title": "A Light in the Attic",
      "price": 51.77,
      "rating": 3,
      "availability": "In stock",
      "category": "Poetry",
      "image_url": "http://books.toscrape.com/media/cache/2c/61/2c61093155705cdb24982bb74bb5611f.jpg"
    }
  ]
}
```

### 3. Buscar Livros por Título

```bash
curl -X GET "http://localhost:8000/api/v1/books/search?title=Light"
```

### 4. Obter Livros por Faixa de Preço

```bash
curl -X GET "http://localhost:8000/api/v1/books/price-range?min_price=10&max_price=50&limit=10"
```

### 5. Registrar Usuário

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=usuario&password=senha123&confirm_pessword=senha123&fullname=Nome Completo&cellphone=11999999999"
```

### 6. Fazer Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=usuario&password=senha123"
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 7. Usar Token para Acessar Rota Protegida

```bash
curl -X POST "http://localhost:8000/api/v1/scraping/trigger" \
     -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

### 8. Obter Detalhes de um Livro

```bash
curl -X GET "http://localhost:8000/api/v1/books/1"
```

**Resposta:**
```json
{
  "id": 1,
  "title": "A Light in the Attic",
  "price": 51.77,
  "rating": 3,
  "availability": "In stock",
  "category": "Poetry",
  "image_url": "http://books.toscrape.com/media/cache/2c/61/2c61093155705cdb24982bb74bb5611f.jpg"
}
```

### 9. Listar Categorias

```bash
curl -X GET "http://localhost:8000/api/v1/categories"
```

**Resposta:**
```json
{
  "count": 50,
  "categories": [
    "Art",
    "Biography",
    "Business",
    "Childrens",
    "Christian",
    "Classics"
  ]
}
```

### 10. Livros Mais Bem Avaliados

```bash
curl -X GET "http://localhost:8000/api/v1/books/top-rated?limit=10"
```
