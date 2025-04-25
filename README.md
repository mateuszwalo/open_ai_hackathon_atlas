# template
```bash
git clone https://github.com/mateuszwalo/template.git
cd template
```
uzupełnij klucze do openai w .env
OPENAI_API_KEY=sk-...

potem budujecie kontener z compose

```bash
docker-compose up -d --build

docker ps #opcjonalnie do sprawdzenia czy all działa
```
test postgresa - tam ustalicie w .env jakies hasła etc

```bash
docker exec -it postgres_db psql -U $POSTGRES_USER -d $POSTGRES_DB
\dt         -- listuj tabele
SELECT 1;   -- testowe zapytanie

``` 
test mongo

```bash
docker exec -it mongo_db mongosh $MONGO_URI/$MONGO_DB
db.stats()

```
uwaga pamietajcie ze tylko neo ma interfejs graficzny!

a porty są tak obciążone
PostgreSQL: localhost:5432
MongoDB: localhost:27017
Neo4j: localhost:7474 (HTTP), localhost:7687 (Bolt)
Redis: localhost:6379

neo4js

Otwórz przeglądarkę
http://localhost:7474 powinno pójść, poprzednia wersja nie była git jednak xd

Zaloguj się:
Login: neo4j
Hasło: strongpassword1234

```cypher
RETURN 1 AS test
```
redis
```bash
docker exec -it redis_cache redis-cli
ping
# => PONG
```

w razie problemów tak resetuje kontener

```bash
docker-compose restart backend
docker-compose down
```

tak testujemy api
```bash
curl -X POST http://localhost:8000/agent   -H "Content-Type: application/json"   -d '{"message": "Cześć! Kim jesteś?"}'
``` 
jak uzupełnicie klucze to wam się pojawi to

{"detail":"400: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}"}

chyba że zapłaicie 5$ :D