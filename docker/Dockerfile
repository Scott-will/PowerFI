# dockerfile, image, container
FROM python:3.11

WORKDIR /PowerFIServer

COPY PowerFIServer/ .

RUN pip install --no-cache-dir \
    annotated-types anyio asyncpg bandit certifi charset-normalizer \
    fastapi flake8 greenlet h11 idna iniconfig markdown-it-py mccabe mdurl \
    myql oauthlib packaging pbr pluggy pyaml pycodestyle pydantic \
    pydantic_core pyflakes Pygments pytest PyYAML requests rich \
    ruamel.yaml ruamel.yaml.clib setuptools six sniffio SQLAlchemy \
    stringcase typing_extensions urllib3 uvicorn wheel yahoo-oauth yfpy

ENV PYTHONPATH="/PowerFIServer"


CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "8000"]