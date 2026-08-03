# 语法：Python 3.12 精简镜像 + uv 装包
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DIYAN_TRANSPORT=stdio \
    PIP_NO_CACHE_DIR=1

RUN pip install --no-cache-dir "diyan-research-mcp==0.1.1"

# 非 root
RUN useradd --create-home --shell /bin/bash mcp
USER mcp
WORKDIR /home/mcp

ENTRYPOINT ["diyan-research-mcp"]
