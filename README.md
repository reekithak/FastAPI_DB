# Fast API Reference

#### Commands

###### Uvicorn Commands
- uvicorn app.main:app  --port 8000 --reload
##### Docker Commands
- docker-compose up -d
- docker-compose down
- docker exec -it learn_fastAPI bash
- docker exec -it 1970a605494d bash 
- docker build -t fastapi .
- docker ps -a
- docker images ls
- docker logs 68c2c183b733
##### Alembic Commands
- alembic init alembic 
- alembic revision -m "create posts table"
- alembic current
- alembic history / heads
- alembic upgrade  0d79980473ac / head
##### Postman Saving
- pm.environment.set("JWT", pm.response.json()["Access Token"]);