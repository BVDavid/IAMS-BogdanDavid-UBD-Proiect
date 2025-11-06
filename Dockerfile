FROM python:3.11-alpine

# Setam directorul de lucru in container
WORKDIR /app

# Copiem si instalam dependentele
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem tot codul aplicatiei
COPY app /app

# Expunem portul (Flask ruleaza implicit pe 5000)
EXPOSE 5000

# Comanda de pornire a aplicatiei
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
