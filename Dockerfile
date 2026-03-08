FROM alpine:3.18

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NONINTERACTIVE=1 \
    SKIP_CONFIG=1

WORKDIR /app

ENV TELEGRAM_BOT_TOKEN="" \
    BASE_DIR="/app" \
    TEMP_DIR="/data"

COPY requirements.txt ./

# Install runtime and build dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash \
    ffmpeg && \
    apk add --no-cache --virtual .build-deps \
    python3-dev \
    gcc \
    musl-dev \
    libffi-dev \
    zlib-dev \
    jpeg-dev \
    openjpeg-dev \
    linux-headers

# Create venv and install Python dependencies from requirements.txt
RUN python3 -m venv /app/.env && \
    /app/.env/bin/pip install --upgrade pip "setuptools<81" wheel && \
    /app/.env/bin/pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

COPY . .

VOLUME ["/data"]

COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/app/.env/bin/python", "main_run_bot.py"]
