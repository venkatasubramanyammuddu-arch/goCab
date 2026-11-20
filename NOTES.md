# Learning notes

## Day 1: project setup and health check

- **Learned:** Docker Compose starts the app, PostgreSQL and Redis with one command, and the services reach each other by name (`db`, `redis`), not `localhost`. A real health check tests its dependencies with timeouts and returns 503 when one is down. FastAPI can return JSON, HTML, text and files, and the status code is a separate choice from the body.
- **Confused me:** How to check that the app is really running in Docker (answer: browser on port 8000, `docker compose ps`, `docker compose logs app`). Also why my code change did not appear: the container runs the code from the last build, so I need `docker compose up -d --build`. A `NameError` made `/test` return 500 and the real cause was only in the logs.
- **Revisit:** Reading Python tracebacks from the bottom up. Why `depends_on` needs a health check. A dev setup that reloads code without rebuilding.

## Day 2: project structure and database basics

- **Learned:** Routers group endpoints by feature, so `main.py` only creates the app and plugs routers in. Settings live in one `Settings` class that refuses to start the app when a variable is missing. SQLAlchemy maps Python classes to tables, and Alembic records every schema change as a versioned migration (autogenerate compares the models with the real database; always read the result before applying).
- **Confused me:** Why a login from my machine failed while the app in Docker worked: a PostgreSQL installed on Windows already used port 5432, so my host reached the wrong database. Fixed by publishing the container on 5433. Also microservices vs endpoints in one file: separate files are modules, not services.
- **Revisit:** How `Depends(get_db)` hands each request its own session (Day 3 will use it). What `pool_pre_ping` protects against.

### PostgreSQL vs SQL Server (differences I met today)

| Topic | SQL Server | PostgreSQL |
|---|---|---|
| Auto-number column | `IDENTITY(1,1)` | Backed by a sequence (`nextval('users_id_seq')`) |
| Variable text | `NVARCHAR(255)` | `VARCHAR(255)`, Unicode by default |
| Time with time zone | `DATETIMEOFFSET` | `TIMESTAMPTZ` |
| Current time default | `GETDATE()` / `SYSDATETIMEOFFSET()` | `now()` |
| Describe a table | `sp_help users` | `\d users` in `psql` |
| Schema changes | EF migrations / SSDT | Alembic |
