FROM       python:3.13-slim

VOLUME     /python-nuheat
WORKDIR    /python-nuheat
COPY       . /python-nuheat

RUN        pip3 install -U pip && pip3 install ipython ".[dev]"

CMD        ["/bin/bash"]
