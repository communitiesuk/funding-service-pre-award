FROM python:3.10-bullseye@sha256:c4f2ab8f2d5b520e4038e2c1dac555f0b1c0274b658c20b1d40b2e72d1e536ce

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:feebeb26b63566bb53d53031dee5497e49a0aa66feffd33aabe2e98307c72f6d /uv /uvx /bin/

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
