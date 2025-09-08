# CryptoComics DEX API

A high-performance FastAPI backend for cryptocurrency DEX (Decentralized Exchange) data aggregation and analytics.

## Features

- **Pool Analytics** - Retrieve liquidity pool data with sorting and pagination
- **Transaction History** - Access recent swap transactions for specific pools  
- **Token Holders** - Query token holder distributions with flexible filtering
- **Real-time Performance** - Sub-second response times with connection pooling
- **Robust Error Handling** - Automatic retry logic and graceful failure handling

## Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL database
- Redis (optional, for caching)

### Installation

```bash
# Clone repository
git clone <repository-url>
cd cryptocomicsdexapi

# Install dependencies
pip install -e .

# Set environment variables
export DATABASE_USER=your_db_user
export DATABASE_PASSWORD=your_db_password  
export DATABASE_HOSTNAME=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=your_db_name

# Run the API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
docker build -t cryptocomics-dex-api .
docker run -p 8000:8000 cryptocomics-dex-api
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/v1/pools` | List liquidity pools with pagination |
| `GET /api/v1/pool/{address}` | Get specific pool details |
| `GET /api/v1/pool/transactions/{address}` | Pool transaction history |
| `GET /api/v1/denom/holders/{denomaddress}` | Token holder distribution |

## Performance

- **Database Connection Pooling** - Optimized PostgreSQL connections with pre-ping validation
- **Query Optimization** - Database-level sorting and filtering
- **Caching Layer** - Redis integration for frequently accessed data
- **Async Operations** - Non-blocking request handling

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM with connection pooling
- **PostgreSQL** - Primary data store
- **Redis** - Caching layer
- **Uvicorn** - ASGI server

## License

MIT
