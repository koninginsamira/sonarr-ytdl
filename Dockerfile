FROM python:3-alpine
LABEL maintainer="Forest Ames <fox.ames@smallfox.io>"

# Update and install ffmpeg
RUN apk update && \
    apk add ffmpeg 

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# create abc user so root isn't used
RUN \
	adduser -u 911 -D -h /config -s /bin/false abc && \
	addgroup abc users && \
# create some files / folders
	mkdir -p /config /app /sonarr_root /logs && \
	touch /var/lock/sonarr-ytdl.lock

# add volumes
VOLUME /config
VOLUME /sonarr_root
VOLUME /logs

# add local files
COPY app/ /app

# update file permissions
RUN \
    chmod a+x \
    /app/sonarr-ytdl.py \ 
    /app/utils.py \
    /app/config.yml.template

# ENV setup
ENV CONFIGPATH /config/config.yml

CMD [ "python", "-u", "/app/sonarr-ytdl.py" ]
