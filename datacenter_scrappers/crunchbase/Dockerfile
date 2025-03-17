FROM ubuntu:22.04

LABEL maintainer="v5"

COPY copyables /

# Update packages, install essential dependencies, and clean up
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \run command
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    supervisor \
	xvfb  \
	socat  \
	net-tools  \
    x11vnc \
    fluxbox \
    wget && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    rm -rf /var/cache/* /var/log/apt/* /tmp/*

# Install Latest Google Chrome and Chrome Remote Desktop
RUN wget --no-check-certificate -O /tmp/google-chrome-stable.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends /tmp/google-chrome-stable.deb && \
    rm /tmp/google-chrome-stable.deb

# Configure the environment
RUN useradd -m chrome && \
    mkdir -p /home/chrome/.fluxbox && \
    echo ' \n\
       session.screen0.toolbar.visible:        false\n\
       session.screen0.fullMaximization:       true\n\
       session.screen0.maxDisableResize:       true\n\
       session.screen0.maxDisableMove: true\n\
       session.screen0.defaultDeco:    NONE\n\
    ' >> /home/chrome/.fluxbox/init && \
    chown -R chrome:chrome /home/chrome/.fluxbox

USER chrome

#VOLUME ["/home/chrome"]

WORKDIR /home/chrome

EXPOSE 5900
EXPOSE 9222


CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]