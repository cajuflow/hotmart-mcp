FROM python:3.12-slim

# Instalar uv
RUN pip install uv

# Configurar diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração
COPY pyproject.toml ./
COPY README.md ./

# Instalar dependências
RUN uv sync --no-dev

# Ativar virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Copiar código fonte
COPY src/ ./src/
COPY hotmart_mcp.py ./

# Criar usuário não-root
RUN groupadd -r mcp && useradd -r -g mcp -s /bin/bash mcp
RUN chown -R mcp:mcp /app
USER mcp

# Expor porta
EXPOSE 8000

# Variáveis de ambiente
ENV TRANSPORT_TYPE=sse
ENV PYTHONUNBUFFERED=1

# Comando padrão
CMD ["python", "hotmart_mcp.py"]
