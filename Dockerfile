# 1. Use an official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set work directory
WORKDIR /app

# 4. Install dependencies
# We do this before copying code to use Docker's cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project
COPY . /app/

# 6. Expose the port Django runs on
EXPOSE 8000

# 7. Run the server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web3_config.wsgi:application"]

