# Build and run the docker container:
# $ docker build -t python-nuheat .
# $ docker run -it --rm -v /path/to/project/root:/python-nuheat python-nuheat
#
# To run the interactive shell:
# $ ipython
#
# To run tests:
# $ python -m unittest

FROM       python:3.6-slim

VOLUME     /python-nuheat
WORKDIR    /python-nuheat
COPY       requirements.txt /python-nuheat

# pyreadline and a downgraded version of jedi are required for ipython's
# autocompletion
RUN        pip3 install -U pip \
           && pip3 install ipython pyreadline jedi==0.17.2 \
           && pip3 install -r requirements.txt

CMD        ["/bin/bash"]
