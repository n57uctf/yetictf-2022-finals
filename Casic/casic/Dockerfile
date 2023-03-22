FROM ubuntu:20.04
MAINTAINER @bigger777
RUN apt update && apt install -y tcpd xinetd libpq-dev libcurl4-gnutls-dev
RUN useradd casic
COPY ./casic-config /etc/xinetd.d/casic
COPY ./bin/casic /casic
COPY ./bin/send_email /send_email
COPY ./bin/libquickmail.a /libquickmail.a
RUN chmod 0777 /casic
EXPOSE 7777
CMD xinetd -dontfork
