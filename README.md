# Store Monitoring

Install dependencies

`pip install -r requirements.txt`

> OR manually install fastapi, uvicorn[standard], sqlalchemy, psycopg[binary]

Run API server (auto reload on code chnage)

`uvicorn api-server.main:app --reload`

Run with more options (auto reload on code chnage)

`uvicorn api-server.main:app --reload --host=0.0.0.0 --port=8000`