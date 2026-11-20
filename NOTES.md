# Learning notes

## Day 1: project setup and health check

- **Learned:** Docker Compose starts the app, PostgreSQL and Redis with one command, and the services reach each other by name (`db`, `redis`), not `localhost`. A real health check tests its dependencies with timeouts and returns 503 when one is down. FastAPI can return JSON, HTML, text and files, and the status code is a separate choice from the body.
- **Confused me:** How to check that the app is really running in Docker (answer: browser on port 8000, `docker compose ps`, `docker compose logs app`). Also why my code change did not appear: the container runs the code from the last build, so I need `docker compose up -d --build`. A `NameError` made `/test` return 500 and the real cause was only in the logs.
- **Revisit:** Reading Python tracebacks from the bottom up. Why `depends_on` needs a health check. A dev setup that reloads code without rebuilding.
