# Build and run the docker container:
# $ docker build -t python-nuheat .
# $ docker run -it --rm -v $(pwd):/python-nuheat python-nuheat
#
# To run the interactive shell:
# $ ipython
#
# To run tests:
# $ python -m unittest

FROM       python:3.6-slim

VOLUME     /python-nuheat
WORKDIR    /python-nuheat
COPY       . /python-nuheat

# pyreadline and a downgraded version of jedi are required for ipython's
# autocompletion
RUN        pip3 install -U pip
RUN        pip3 install ipython pyreadline jedi==0.17.2
RUN        pip3 install ".[dev]"

CMD        ["/bin/bash"]
