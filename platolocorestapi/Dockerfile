FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PATH="/platolocorestapi/bin:$PATH"
ENV PYTHONPATH /platolocorestapi


RUN mkdir -p /platolocorestapi

# Update working directory
WORKDIR /platolocorestapi

# copy everything from this directory to server docker container
COPY ./requirements.txt /platolocorestapi/

# Install the Python libraries
RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

CMD python3 src/waitress_server.py

