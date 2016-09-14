FROM ubuntu:16.04
MAINTAINER Florian Geigl <florian.geigl@gmail.com>
# install some basics and libraries needed for dryscrape
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && apt-get update --fix-missing && \
    apt-get upgrade -y --no-install-recommends && \
    apt-get install -y --no-install-recommends wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion xvfb curl libqt5webkit5 vim screen htop less && \
    # clean up apt \
    apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# set up some basics and add conda to the path for all users
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh \
    mkdir .jupyter && \
    mkdir -p -m 700 .local/share/jupyter && \
    echo "cacert=/etc/ssl/certs/ca-certificates.crt" > .curlrc

# install anaconda
RUN wget --quiet https://repo.continuum.io/archive/Anaconda2-4.1.1-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh

# add conda to the path var
ENV PATH /opt/conda/bin:$PATH

# install graph-tool
RUN apt-key adv --keyserver pgp.skewed.de --recv-key 98507F25 && \
    touch /etc/apt/sources.list.d/graph-tool.list && \
    echo 'deb http://downloads.skewed.de/apt/xenial xenial universe' >> /etc/apt/sources.list.d/graph-tool.list && \
    echo 'deb-src http://downloads.skewed.de/apt/xenial xenial universe' >> /etc/apt/sources.list.d/graph-tool.list && \
    apt-get update && apt-get install -y --no-install-recommends python-graph-tool && \
    ln -s /usr/lib/python2.7/dist-packages/graph_tool /opt/conda/lib/python2.7/site-packages/graph_tool && \
    apt-get clean && apt-get autoremove && rm -rf /var/lib/apt/lists/*
    
RUN conda update -y conda conda-build conda-env && \
    # you can add further conda libraries here \
    conda install -y dryscrape xgboost seaborn tqdm termcolor joblib keras pygobject3 gtk3 tensorflow \
    pymysql \
    # and further conda channels here \
    -c pkgw -c floriangeigl -c conda-forge -c bioconda -c jaikumarm \
    && \
    # cleans up conda after installation of libraries \
    conda clean -i -l -t -y

# enable this command to install libraries using pip
# RUN pip install 

EXPOSE 8888 # expose the jupyter port 
CMD ["startup.sh"] # start jupyter at container start
COPY start-notebook.sh /usr/local/bin/ # copy jupyter startscript into the container
COPY startup.sh /usr/local/bin/ # copy startup script into the container
