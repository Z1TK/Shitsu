ARG PYTHON_VERISON=3.12
FROM python:${PYTHON_VERISON}-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONNUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY entripoint.sh /entripoint.sh
RUN chmod +x /entripoint.sh

CMD ["/entripoint.sh"]