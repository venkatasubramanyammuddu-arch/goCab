# goCab

A small cab booking app built in Python (FastAPI) to learn system design. It follows a six-week plan; this README covers everything done so far (Day 1).

## What runs

`docker compose up` starts three containers:

| Service | Image | Port | Purpose |
|---|---|---|---|
| `app` | built from `Dockerfile` | 8000 | FastAPI application |
| `db` | `postgres:16` | 5432 | PostgreSQL database |
| `redis` | `redis:7` | 6379 | Redis (cache, rate limits, locations later) |

Inside Docker's private network the services reach each other by name: the app connects to `db` and `redis`, not `localhost`. Inside a container, `localhost` means that container itself.

## Project layout

```
cab-app/
├── app/main.py          FastAPI app with the /health endpoint
├── Dockerfile           Recipe for the app image
├── docker-compose.yml   Starts app + Postgres + Redis together
├── requirements.txt     Pinned Python packages
├── .env.example         Template for settings (committed)
├── .env                 Real local settings (NOT committed)
├── .dockerignore        Files kept out of the Docker image
└── .gitignore           Files kept out of Git
```

## First-time setup

1. Install and start **Docker Desktop**. Wait until it says the engine is running.
2. Create your settings file from the template:
   ```
   copy .env.example .env
   ```
   Then edit `.env` and set your own `POSTGRES_PASSWORD`. Never commit `.env`.
3. Start everything, from the project folder:
   ```
   docker compose up -d --build
   ```

## Daily commands

Run these from `E:\subbu\cab-app`.

| Goal | Command |
|---|---|
| Start everything | `docker compose up -d` |
| Start and rebuild the app after code changes | `docker compose up -d --build` |
| Stop and remove containers (data is kept) | `docker compose down` |
| Stop and also delete the database data | `docker compose down -v` |
| Stop or start one service | `docker compose stop redis` / `docker compose start redis` |
| Restart one service | `docker compose restart app` |

`--build` matters: without it Docker keeps running the old image and your code changes do not appear.

## How to check the app is running in Docker

### 1. Browser
- http://127.0.0.1:8000/health shows `{"status":"ok","db":"ok","redis":"ok"}`
- http://127.0.0.1:8000/docs shows the interactive API page. Open `GET /health`, click **Try it out**, then **Execute**.

### 2. Docker Desktop
Open **Containers** and find the `cab-app` group with `app-1`, `db-1`, `redis-1`. A green dot means running. Click a container and open **Logs** to watch its output live. Refresh `/health` in the browser and a new log line appears for each request.

### 3. Terminal

| Question | Command |
|---|---|
| Which services are running and healthy? | `docker compose ps` |
| What has the app printed? | `docker compose logs app` |
| Follow the app's logs live | `docker compose logs -f app` (Ctrl+C to stop following) |
| Last 20 lines of the database log | `docker compose logs db --tail 20` |
| Does the endpoint answer? | `curl http://127.0.0.1:8000/health` |
| Is Redis alive? | `docker compose exec redis redis-cli ping` (answers `PONG`) |
| Open a SQL prompt in Postgres | `docker compose exec db psql -U cab -d cabapp` (type `\q` to leave) |
| Which containers exist on this machine? | `docker ps` |

Note: `curl -i http://127.0.0.1:8000/health` also shows the HTTP status code (200 healthy, 503 degraded).

### 4. Proof that the container serves the app
```
docker compose stop app      # the browser page now fails
docker compose start app     # the page works again
```

## What the health check means

`GET /health` runs `SELECT 1` on Postgres and `PING` on Redis, each with a 2 second timeout.

| Situation | HTTP status | Body |
|---|---|---|
| Everything works | 200 | `{"status":"ok","db":"ok","redis":"ok"}` |
| Something is down | 503 | `{"status":"degraded","db":"ok","redis":"error: ConnectionError"}` |

Try it: `docker compose stop redis`, refresh `/health`, then `docker compose start redis`. The app recovers by itself.

## Run without Docker (optional)

Only the app, with no Postgres or Redis, so `/health` will report errors unless they are reachable.

```
python -m venv .venv
.venv\Scripts\activate
set PIP_USE_FEATURE=truststore
pip install -r requirements.txt
set DATABASE_URL=postgresql://cab:YOUR_PASSWORD@localhost:5432/cabapp
set REDIS_URL=redis://localhost:6379/0
uvicorn app.main:app --reload --port 8000
```

`PIP_USE_FEATURE=truststore` is needed on this machine because the antivirus inspects HTTPS traffic and Python does not trust its certificate. It needs `pip install truststore` first (see Troubleshooting).

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `docker` commands fail with "cannot connect to the daemon" | Docker Desktop is not running. Open it and wait for the engine to start. |
| Browser says "refused to connect" on port 8000 | The `app` container is not running. Check `docker compose ps` and `docker compose logs app`. |
| `/health` returns 503 right after `up` | Postgres or Redis is still starting. Wait a few seconds and retry. |
| Code changes do not show up | Rebuild with `docker compose up -d --build`. |
| Port already in use | Another program uses 8000, 5432 or 6379. Stop it or change the left-hand number in `ports:` in `docker-compose.yml`. |
| `pip install` fails with `CERTIFICATE_VERIFY_FAILED` | Antivirus HTTPS inspection. Set `PIP_CERT` to the antivirus certificate file once to install `truststore`, then use `PIP_USE_FEATURE=truststore`. |
| `git push` fails with an SSL error | In this repo only: `git config http.sslBackend schannel`. |
| `git push` says authentication failed | Run it without disabling prompts so Git Credential Manager can open the sign-in window. |
| App crashes at start with `KeyError: 'DATABASE_URL'` | The variable is missing. Start through Docker Compose, which sets it from `.env`. |

## Git

- Remote: https://github.com/venkatasubramanyammuddu-arch/goCab
- Branch: `main`
- Commit at the end of every day. Never commit `.env`.

```
git status
git add -A
git commit -m "Day N: short description"
git push
```

## Progress

| Day | Topic | State |
|---|---|---|
| 1 | Project setup, Docker Compose, health check | Done |
| 2 | Project structure, settings, SQLAlchemy, Alembic, users table | Next |
