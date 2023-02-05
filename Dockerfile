FROM python:3.10

RUN useradd -m -r -d /usr/local/tonie-podcast-sync -U -u 4000 tps 

WORKDIR /usr/local/tonie-podcast-sync 

USER 4000

ENV PATH "/usr/local/tonie-podcast-sync/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

RUN pip install poetry

ADD poetry.lock .
ADD pyproject.toml .
ADD README.md .
ADD tonie_api/ tonie_api/
ADD podcast.py .
ADD toniepodcastsync.py .
ADD docker-entrypoint.py run.py

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "run.py"]