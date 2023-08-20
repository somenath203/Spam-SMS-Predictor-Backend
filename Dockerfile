FROM python:3.11.2


WORKDIR /app


COPY . /app


RUN pip install -r requirements.txt


EXPOSE 80


ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
