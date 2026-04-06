FROM python:3.11-slim

WORKDIR /app

# Copy only requirements first (this allows caching)
COPY requirements.txt .

# Upgrade pip and install dependencies (no hash check)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Copy rest of the code after dependencies (so Docker cache is reused)
COPY . .

CMD ["python", "app.py"]