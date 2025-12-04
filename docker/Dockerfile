# Enable Buildkit and run
# DOCKER_BUILDKIT=1 docker build --progress=plain --ssh default=$HOME/.ssh/name_of_your_ssh_key .

FROM python:3.11-slim as build

# Set up the working directory in the container
#WORKDIR /quantnet-agent

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    openssh-client \ 
    git \
    && apt-get clean

# Update pip
#RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel

#RUN mkdir -p -m 0600 ~/.ssh && \
#    ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# Set environment variable for GitLab Package Registry authentication
# ARG PIP_EXTRA_INDEX_URL
# ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}

RUN --mount=type=secret,id=GH_TOKEN \
    export GH_TOKEN=$(cat /run/secrets/GH_TOKEN) && \
    git clone --single-branch --branch develop https://${GH_TOKEN}@github.com/quant-net/quant-net-mq quantnet_mq && \
    cd quantnet_mq && pip install --no-cache-dir .

RUN --mount=type=secret,id=GH_TOKEN \
    export GH_TOKEN=$(cat /run/secrets/GH_TOKEN) && \
    git clone --single-branch --branch develop https://${GH_TOKEN}@github.com/quant-net/quant-net-plugins quant-net-plugins

RUN --mount=type=secret,id=GH_TOKEN \
    export GH_TOKEN=$(cat /run/secrets/GH_TOKEN) && \
    git clone --single-branch --branch develop https://${GH_TOKEN}@github.com/quant-net/quant-net-agent.git && \
    cd quant-net-agent && pip install --no-cache-dir .


COPY docker/docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["quantnet_agent"]