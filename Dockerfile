FROM debian:latest

RUN apt-get update && apt-get dist-upgrade -y

RUN apt-get install -y locales locales-all
RUN update-locale LANG=en_US.UTF-8
ENV TZ=Asia/Yekaterinburg
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y tzdata openssh-server sudo bash-completion tree git build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev gzip wget liblzma-dev net-tools nano iputils-ping libpq-dev

RUN useradd -m -d /home/ezv -s /bin/bash -G sudo ezv
RUN echo 'ezv:099609' | chpasswd
RUN echo 'root:099609' | chpasswd

WORKDIR /app

RUN wget https://www.python.org/ftp/python/3.11.6/Python-3.11.6.tgz
RUN tar -xf Python-3.11.6.tgz && \
    cd Python-3.11.6 && \
    ./configure --enable-optimizations && \
    make -j 2 && \
    make altinstall

RUN rm -rf Python-3.11.6 \
    && rm -f Python-3.11.6.tgz 

#ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/app/venv/

RUN apt install -y python3-pip python3.11-venv

RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

RUN service ssh start
EXPOSE 22

ENTRYPOINT cd /app/proj && python3 -m main
