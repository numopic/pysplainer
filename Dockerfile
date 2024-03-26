FROM python:3.9-bullseye

# Set up project directory
RUN mkdir /pysplainer
WORKDIR /pysplainer

RUN pip install poetry==1.7.1
COPY pyproject.toml ./
RUN touch README.md
RUN poetry install --no-root

COPY . ./
RUN poetry install --only-root

ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]