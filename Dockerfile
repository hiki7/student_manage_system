FROM python:3.12 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry==1.5.0

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

FROM python:3.12

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /studentManagementSystem

COPY --from=requirements-stage /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=requirements-stage /usr/local/bin /usr/local/bin

COPY . .

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=studentManagementSystem.settings \
    PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["python", "studentManagementSystem/manage.py", "runserver", "0.0.0.0:8000"]
