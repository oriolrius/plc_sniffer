FROM python:alpine3.16

ARG UID=0
ARG GID=0

WORKDIR /sniffer

# Install all required dependencies including development tools and runtime libraries
RUN apk update \
    && apk add --no-cache \
       libpcap \
       tcpdump \
       net-tools \
       python3-dev \<
       py3-pip \
       build-base \
       libpcap-dev \
       linux-headers \
       gcc \
       musl-dev \
    && rm -rf /var/cache/apk/*

# Copy only the files necessary for dependency installation first
COPY pyproject.toml ./

# Install Python dependencies directly with pip
RUN pip install --no-cache-dir scapy>=2.5.0 
RUN pip install --no-cache-dir -e .

# Copy the rest of the application code
COPY . .

# CMD to run the application
# Ensure plc_sniffer.py is the correct main script.
CMD ["python3", "plc_sniffer.py"]

# Optional: Add and switch to a non-root user for better security
# Consider uncommenting these lines for production
# ARG APP_USER_UID=1000
# ARG APP_USER_GID=1000
# RUN addgroup -S -g ${APP_USER_GID} appgroup && \
#     adduser -S -u ${APP_USER_UID} -G appgroup appuser
# USER appuser
