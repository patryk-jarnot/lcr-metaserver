#FROM python:3.7
FROM ubuntu:21.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y npm \
    && apt-get install -y python3 \
    && apt-get install -y python3-pip \
    && apt-get install -y screen

ENV PYTHONUNBUFFERED 1
ENV PATH="/lcr-metaserver/platolocorestapi/bin:$PATH"

RUN mkdir -p /lcr-metaserver

# Update working directory
WORKDIR /lcr-metaserver

# to create a user
#ARG username
#RUN adduser -D ${username}
#RUN chown -R ${username} /app
#USER ${username}

# copy everything from this directory to server docker container
COPY . /lcr-metaserver

# Install the Python libraries
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt


CMD ./run_angular.sh & ./run_flask.sh

