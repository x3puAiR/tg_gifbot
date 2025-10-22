FROM centos:7

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NONINTERACTIVE=1 \
    SKIP_CONFIG=1

WORKDIR /app

# Default envs; users should override TELEGRAM_BOT_TOKEN and paths as needed
ENV TELEGRAM_BOT_TOKEN="" \
    BASE_DIR="/app" \
    TEMP_DIR="/data"

# Copy minimal files first for better caching during install script
COPY requirements.txt ./
COPY install_centos.sh ./

# Use the provided install script to set up Python 3.6, FFmpeg, and venv deps
RUN bash /app/install_centos.sh

# Copy the rest of the app
COPY . .

# Create a data volume for temp/cache
VOLUME ["/data"]

# Add entrypoint
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python3", "main_run_bot.py"]


