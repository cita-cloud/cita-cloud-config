FROM python:slim-buster
WORKDIR /cita_cloud_config
COPY --from=citacloud/kms_sm:latest /usr/bin/kms /usr/bin/
RUN /bin/sh -c set -eux;\
    apt-get update;\
    apt-get install -y --no-install-recommends libsqlite3-0;\
    rm -rf /var/lib/apt/lists/*;
COPY cita_cloud_config.py requirements.txt /cita_cloud_config/
RUN /bin/sh -c set -eux;\
    pip install -r requirements.txt;
ENTRYPOINT ["/cita_cloud_config/cita_cloud_config.py"]