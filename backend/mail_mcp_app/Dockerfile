# =========================
# Stage 1: Build UI
# =========================
FROM node:20-slim AS ui-builder

WORKDIR /app/mcp_ui

COPY mcp_ui/package*.json ./

# Clean install dependencies
RUN npm ci

COPY mcp_ui/ ./

# Create the UI bundle
RUN npm run build


# =========================
# Stage 2: MCP server
# =========================
FROM python:3.14-slim AS mcp-server

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy Python MCP server
COPY mail_mcp ./mail_mcp

# Copy built MCP UI
COPY --from=ui-builder /app/mcp_ui/dist ./mcp_ui/dist

# Install Python dependencies
WORKDIR /app/mail_mcp

RUN uv sync --locked --no-dev

# Make virtual environment available
ENV PATH="/app/mail_mcp/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uv", "run", "mail-mcp"]