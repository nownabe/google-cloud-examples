#!/usr/bin/env bash

echo 'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"' >> /etc/environment

apt-get update
apt-get -y install python3-pip git
pip3 install tensorflow google-cloud-aiplatform

gsutil -m cp -r gs://cloud-samples-data/ai-platform/flowers /opt/

git clone https://github.com/nownabe/google-cloud-examples /opt/google-cloud-examples