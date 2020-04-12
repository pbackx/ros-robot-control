FROM ros:melodic-ros-base

RUN apt update && \
    apt install -y wget python python-pip && \
    rm -rf /var/lib/apt/lists/*

RUN wget -O - https://deb.nodesource.com/setup_12.x | sudo -E bash - && \
    sudo apt-get install -y nodejs

RUN mkdir /project && \
    cd /project && \
    wget https://github.com/aws/aws-greengrass-core-sdk-python/archive/v1.5.0.tar.gz && \
    tar zxvf v1.5.0.tar.gz && \
    rm v1.5.0.tar.gz

RUN pip install flask imutils Pillow boto3
