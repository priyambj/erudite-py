FROM ubuntu:16.04
MAINTAINER Florian Geigl <florian.geigl@gmail.com>
RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion xvfb curl libqt5webkit5
RUN apt-get update && apt-get upgrade -y && apt-get install -y htop 
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh
RUN /opt/conda/bin/conda update -y conda conda-build conda-env anaconda 
RUN /opt/conda/bin/conda install -y dryscrape xgboost seaborn tqdm termcolor joblib keras pygobject3 gtk3 \
    -c pkgw -c floriangeigl -c conda-forge -c bioconda -c jaikumarm
RUN apt-key adv --keyserver pgp.skewed.de --recv-key 98507F25 && \
    touch /etc/apt/sources.list.d/graph-tool.list && \
    echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' >> /etc/apt/sources.list.d/graph-tool.list && \
    echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' >> /etc/apt/sources.list.d/graph-tool.list && \
    apt-get update && apt-get install -y python-graph-tool && \
    ln -s /usr/lib/python2.7/dist-packages/graph_tool /opt/conda/lib/python2.7/site-packages/graph_tool && \
    apt-get clean && apt-get autoremove
RUN git clone https://github.com/BMKEG/erudite-py.git /opt/erudite
