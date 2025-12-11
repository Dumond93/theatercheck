FROM alpine

WORKDIR /theatercheck

RUN apk update
RUN apk add --no-cache python3 py3-pip
RUN pip install plexapi beautifulsoup4 --break-system-packages
RUN apk del py3-pip && apk cache clean

COPY ./theatercheck.py /theatercheck/

ENTRYPOINT python3 -u theatercheck.py $BASEURL $TOKEN $LIBRARY $INTERVAL
