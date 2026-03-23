# 1. Base Image: Use an official, lightweight Python image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy only the requirements file first (this leverages Docker cache to speed up builds)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container
COPY src/ ./src/
COPY reports/ ./reports/

# 6. The ENTRYPOINT tells Docker what command to run when the container starts.
ENTRYPOINT ["python", "src/github_report.py"]

