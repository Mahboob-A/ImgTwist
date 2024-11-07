ARG PYTHON_VERSION=3.10-bullseye

FROM python:${PYTHON_VERSION} AS python 

FROM python AS python-build-stage
ARG BUILD_ENVIRONMENT=dev

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        libpq-dev 

COPY ./requirements . 

RUN pip wheel --wheel-dir /usr/src/app/wheel \
        -r ${BUILD_ENVIRONMENT}.txt 

FROM python AS python-run-stage 

RUN addgroup --system imgtwist && adduser --system --ingroup imgtwist imgtwist 
ARG BUILD_ENVIRONMENT=dev 
ARG APP_HOME=/home/imgtwist/app 

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1 
ENV BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN mkdir -p ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles && \
        chown -R imgtwist:imgtwist ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles  && \
        chmod -R 775 ${APP_HOME}/staticfiles ${APP_HOME}/mediafiles

RUN apt-get update && apt-get install --no-install-recommends -y \
        libpq-dev \
        gettext \
        && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
        && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheel /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
        && rm -rf /wheels/ 

COPY --chown=imgtwist:imgtwist ./docker/dev/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY --chown=imgtwist:imgtwist ./docker/dev/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

COPY --chown=imgtwist:imgtwist . ${APP_HOME} 

RUN chown imgtwist:imgtwist ${APP_HOME} 

USER imgtwist

ENTRYPOINT ["/entrypoint.sh"]

