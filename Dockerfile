###############################################################################
# Author: Agustin Bassi
# Date: March 25, 2020
# Copyright: Globant Inc.
# Project: PagoChat
# Brief: TODO: Describe it
###############################################################################

# The base image to start from
FROM python:3
# Author & Maintainer data
LABEL Author="Agustin Bassi"
LABEL E-mail="jagustinbassi@gmail.com"
LABEL version="1.0.0"
# Create and set the app dir
RUN mkdir -p /app/src
WORKDIR /app/src
# Copy the requirements to the container
COPY src/requirements.txt ./
# Install all dependencies
RUN pip install -r requirements.txt
# This port will be exposed outside the container
EXPOSE 5000

#########[ Enf of file ]#######################################################
