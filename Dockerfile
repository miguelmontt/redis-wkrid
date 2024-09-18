# Usa una imagen base de Python
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar el código al contenedor
COPY app.py .

# Instalar las dependencias
RUN pip install redis azure-identity

# Comando por defecto
CMD ["python", "app.py"]
