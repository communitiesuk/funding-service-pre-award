FROM python:3.13-bullseye@sha256:4dad5fc8eb40eec30ad0ef972b9137fe5d45a303074e0022842b6c5f27cd5a7f

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:c467e9b5da1e763ee5841f9ae51020d11569ca08991a05367ceca6eda0be9b16 /uv /uvx /bin/

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
