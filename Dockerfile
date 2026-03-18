# Build stage
FROM python:3.10-slim as builder

WORKDIR /app

# Update vulnerable packages FIRST
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade wheel>=0.46.2 jaraco.context>=6.1.0

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.10-slim

WORKDIR /app

# Update vulnerable packages in runtime stage too
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade wheel>=0.46.2 jaraco.context>=6.1.0

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY src/ ./src/

# Ensure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["python", "src/app.py"]