FROM ubuntu:16.04
MAINTAINER Florian Geigl <florian.geigl@gmail.com>
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion xvfb curl libqt5webkit5 vim screen htop && \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*
#RUN apt-get update && apt-get upgrade -y --no-install-recommends && \
#    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV DUSER erudite
ENV DUID 1000
ENV CONDA_DIR /opt/conda/
RUN useradd -m -s /bin/bash -N -u $DUID $DUSER && \
    chown $DUSER /opt/

USER $DUSER
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    mkdir -p /home/$DUSER/ && \
    mkdir /home/$DUSER/.jupyter && \
    mkdir -p -m 700 /home/$DUSER/.local/share/jupyter && \
    echo "cacert=/etc/ssl/certs/ca-certificates.crt" > /home/$DUSER/.curlrc
RUN cd /home/$DUSER && wget --quiet https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh
RUN /opt/conda/bin/conda update -y conda conda-build conda-env anaconda && \
    /opt/conda/bin/conda install -y dryscrape xgboost seaborn tqdm termcolor joblib keras pygobject3 gtk3 tensorflow \
    -c pkgw -c floriangeigl -c conda-forge -c bioconda -c jaikumarm && \
    /opt/conda/bin/conda clean -i -l -t -y

USER root
ENV PATH /opt/conda/bin:$PATH
RUN apt-key adv --keyserver pgp.skewed.de --recv-key 98507F25 && \
    touch /etc/apt/sources.list.d/graph-tool.list && \
    echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' >> /etc/apt/sources.list.d/graph-tool.list && \
    echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' >> /etc/apt/sources.list.d/graph-tool.list && \
    apt-get update && apt-get install -y --no-install-recommends python-graph-tool && \
    ln -s /usr/lib/python2.7/dist-packages/graph_tool /opt/conda/lib/python2.7/site-packages/graph_tool && \
    apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*
EXPOSE 8888
WORKDIR /home/$DUSER
CMD ["startup.sh"]

COPY start-notebook.sh /usr/local/bin/
COPY startup.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/start-notebook.sh /usr/local/bin/startup.sh
RUN chown -R $DUSER:users /home/$DUSER/.jupyter
RUN git clone https://github.com/BMKEG/erudite-py.git /home/$DUSER/erudite

USER $DUSER
