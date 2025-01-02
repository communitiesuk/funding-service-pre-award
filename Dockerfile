FROM python:3.10-bullseye@sha256:aae2541095fee6367d9bfcde94c0d6feef4c33dc894a1d709e9bdefa63660eef

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:f0786ad49e2e684c18d38697facb229f538a6f5e374c56f54125aabe7d14b3f7 /uv /uvx /bin/

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
