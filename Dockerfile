FROM python:3.10-bullseye@sha256:86ae49e94b125580c964601409b9e8da5812e0e382df2b2d7566856e04ec33bc

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:63b7453435641145dc3afab79a6bc2b6df6f77107bec2d0df39fd27b1c791c0a /uv /uvx /bin/

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8080

CMD ["gunicorn", "--worker-class", "gevent", "wsgi:app", "-b", "0.0.0.0:8080"]
