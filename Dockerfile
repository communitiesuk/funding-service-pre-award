FROM python:3.10-bullseye@sha256:24645cd6f38fd6f9b1b8106ffba23ed8e0e4ef798f81a80f67165973b0989f02

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:9618e472e7ed9aa980719c68e51416e7ec23d85742d9ccca5c817d76ed2eb5aa /uv /uvx /bin/

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
