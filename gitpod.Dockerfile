FROM gitpod/workspace-python-tk-vnc:branch-tk-dev
#FROM gitpod/workspace-base:latest

COPY requirements.txt  ./requirements.txt
COPY poetry.lock ./poetry.lock
COPY pyproject.toml ./pyproject.toml

RUN pip install poetry \
    && poetry config virtualenvs.create false && poetry config virtualenvs.in-project false \
    && poetry install
    # && poetry export --without-hashes -f requirements.txt --output requirements.txt && pip3 install --no-deps -r requirements.txt
RUN pip install -r requirements.txt
#RUN  python -m pip install -r requirements.txt
ENV PYTHONUSERBASE=/workspace/.pip-modules \
    PIP_USER=yes
ENV PATH=$PYTHONUSERBASE/bin:$PATH

# Setup Heroku CLI
RUN curl https://cli-assets.heroku.com/install.sh | sh

# Add aliases

RUN echo 'alias heroku_config=". $GITPOD_REPO_ROOT/.vscode/heroku_config.sh"' >> ~/.bashrc
#    echo 'alias python=python3' >> ~/.bashrc && \
#    echo 'alias pip=pip3' >> ~/.bashrc && \
#    echo 'alias font_fix="python3 $GITPOD_REPO_ROOT/.vscode/font_fix.py"' >> ~/.bashrc