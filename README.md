# Store Monitoring

Watch demo video [here](https://youtu.be/wz-MtXdi6Iw)

Tech Stack:

- Python 3.11
- FasiAPI 0.92
- SQLAlchemy 2.0.4
- PostgreSQL 15.2

### Install dependencies

`pip install -r requirements.txt`

> OR manually install fastapi, uvicorn[standard], sqlalchemy, psycopg[binary]

### Environment Variables

Refer `.env.sample` file and create `.env` file

### Run API server (auto reload on code chnage)

`uvicorn api-server.main:app --reload`

### Run with more options (auto reload on code chnage)

`uvicorn api-server.main:app --reload --host=0.0.0.0 --port=8000`

---

See logic for report generation [here](Logic.md)

See PostgreSQL initial preparation [here](Logic.md)