# syntax=docker/dockerfile:1.9
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv using the installer script
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Add uv to PATH
ENV PATH="/root/.local/bin:${PATH}"

# Configure uv for optimal Docker usage
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_NO_CACHE=1 \
    MCP_SERVER_HOST="0.0.0.0" \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/workspace:${PYTHONPATH}"

# Create non-root user
RUN groupadd -r app && useradd -r -d /app -g app app

# Create workspace structure matching local development
WORKDIR /workspace
RUN mkdir -p /workspace/mcp_server /workspace/graphiti_core

# Set proper permissions for workspace
RUN chown -R app:app /app /workspace

# Copy the entire graphiti_core source code first (for dependencies)
COPY --chown=app:app ../graphiti_core /workspace/graphiti_core/
COPY --chown=app:app ../pyproject.toml /workspace/
COPY --chown=app:app ../poetry.lock /workspace/
COPY --chown=app:app ../uv.lock /workspace/

# Copy MCP server files
COPY --chown=app:app mcp_server/pyproject.toml /workspace/mcp_server/
COPY --chown=app:app mcp_server/uv.lock /workspace/mcp_server/

# Switch to MCP server directory
WORKDIR /workspace/mcp_server

# Install dependencies with local graphiti_core (disable all caching)
ENV UV_NO_CACHE=true
RUN rm -rf /tmp/uv-cache /root/.cache/uv /workspace/.cache 2>/dev/null || true
RUN uv sync --frozen --no-dev

# Copy MCP server application code
COPY --chown=app:app mcp_server/graphiti_mcp_server.py ./
COPY --chown=app:app mcp_server/.env* ./

# Fix any remaining permissions and clean any cache
RUN chown -R app:app /workspace && \
    rm -rf /tmp/uv-cache /root/.cache /workspace/.cache 2>/dev/null || true

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uv", "run", "graphiti_mcp_server.py"]
