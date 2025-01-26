# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install MPI, SSH, and other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libopenmpi-dev \
    openmpi-bin \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install mpi4py
RUN pip install --no-cache-dir mpi4py

# Create a non-root user
ARG USERNAME=mpi_user
ARG UID=1000
ARG GID=1000

RUN groupadd --gid $GID $USERNAME && \
    useradd --uid $UID --gid $GID --create-home --shell /bin/bash $USERNAME

# Set permissions for the /app directory
RUN mkdir -p /app && chown $USERNAME:$USERNAME /app

WORKDIR /app
USER $USERNAME

# Ensure the user has access to pip-installed packages
ENV PATH="/home/$USERNAME/.local/bin:${PATH}"

# Copy the application code
COPY . .

# Default command to keep container running (for Kubernetes orchestration)
CMD ["mpiexec", "-n", "4", "python", "/app/mpi_max_temp.py"]
