FROM python:3.10-bullseye@sha256:185d3a481d7ea75214220e5dea6ad46444a83248f255fa460644b4faf1d849be

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:0d686193e6d06a262184e4367d00276e24a524357080868c1732c2718f75d4d9 /uv /uvx /bin/

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
