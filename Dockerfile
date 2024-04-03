FROM python:3.9-slim as base

ENV PYTHONBUFFERED 1
WORKDIR /code

RUN pip install --upgrade pip

EXPOSE 8000

FROM base as current

COPY requirements.txt /code
RUN pip install -r /code/requirements.txt

COPY api /code/api
COPY tests /code/tests

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM base as feat

COPY requirements-feat.txt /code

RUN apt-get update \
    && apt-get install -yq git
RUN pip install -r /code/requirements-feat.txt


COPY api /code/api
COPY tests /code/tests

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
