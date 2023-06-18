FROM apache/airflow:2.6.1
USER airflow
WORKDIR /opt/airflow
COPY --chown=airflow:root requirements.txt ./
COPY --chown=airflow:root dags/ ./dags
COPY --chown=airflow:root plugins/ ./plugins
COPY --chown=airflow:root data ./data
COPY --chown=airflow:root logs/ ./logs
ENV AIRFLOW_HOME="/opt/airflow"
RUN pip install --user -r requirements.txt