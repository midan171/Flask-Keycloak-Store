FROM python:3.9

WORKDIR /app

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Add verbose output to see what's failing
RUN pip install --no-cache-dir -r requirements.txt -v

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]