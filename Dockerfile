FROM apache/airflow:2.8.0
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
ADD requirements.txt . 
RUN pip install --upgrade pip \
  && pip install -r requirements.txt