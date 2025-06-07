FROM python:3.10

# Install nsjail dependencies
RUN apt-get update && apt-get install -y \
    git \
    make \
    gcc \
    g++ \
    libprotobuf-dev \
    libnl-route-3-dev \
    libcap-dev \
    protobuf-compiler \
    bison \
    flex \
    pkgconf \
    clang \
    && rm -rf /var/lib/apt/lists/*

# Clone and build nsjail in /root to avoid permission issues
RUN git clone https://github.com/google/nsjail.git /tmp/nsjail && \
    cd /tmp/nsjail && \
    make && \
    cp nsjail /usr/bin/nsjail

# Set up working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app /app
RUN chmod -R a+rX /app

EXPOSE 8080

# Start the Flask app
CMD ["python3", "main.py"]
