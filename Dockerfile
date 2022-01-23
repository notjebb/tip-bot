FROM ubuntu:20.04

# Install.

RUN apt-get update
RUN apt install locales locales-all -y
RUN locale-gen en_US.UTF-8
RUN apt install sudo libpq-dev -y
RUN useradd -m -d /home/devUser -s /bin/bash -G sudo devUser
RUN echo 'devUser:123' | chpasswd
RUN apt install python3 python3-pip -y

# Add files.
# ADD ./ /home/ubuntu/dev/tip-bot

USER devUser
ENV TERM xterm

WORKDIR /home/devUser/dev/tip-bot

COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt


# Define default command.
CMD ["bash"]