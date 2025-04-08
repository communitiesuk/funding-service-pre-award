FROM python:3.10-bullseye@sha256:eda978a7fc5c81371b0bc87dc410a3a2a15fe2901e53df76835879afc967b3bf

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest@sha256:0b6dc79013b689f3bc0cbf12807cb1c901beaafe80f2ee10a1d76aa3842afb92 /uv /uvx /bin/

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
