FROM python:3

RUN pip install pipenv

WORKDIR /usr/src/app
COPY Pipfile* ./
RUN pipenv install --system --deploy

COPY . .

CMD ["python", "main.py"]
