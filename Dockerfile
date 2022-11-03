FROM       python:3.7-slim

VOLUME     /python-nuheat
WORKDIR    /python-nuheat
COPY       . /python-nuheat

# pyreadline and a downgraded version of jedi are required for ipython's
# autocompletion
RUN        pip3 install -U pip
RUN        pip3 install ipython pyreadline jedi==0.17.2
RUN        pip3 install ".[dev]"

CMD        ["/bin/bash"]
