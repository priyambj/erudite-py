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

# add libraries over pip here
RUN pip install -y textstat && \
    # NLTK Project datasets
    mkdir -p /usr/share/nltk_data && \
    # NLTK Downloader no longer continues smoothly after an error, so we explicitly list
    # the corpuses that work
    python -m nltk.downloader -d /usr/share/nltk_data abc alpino \
    averaged_perceptron_tagger basque_grammars biocreative_ppi bllip_wsj_no_aux \
    book_grammars brown brown_tei cess_cat cess_esp chat80 city_database cmudict \
    comparative_sentences comtrans conll2000 conll2002 conll2007 crubadan dependency_treebank \
    europarl_raw floresta framenet_v15 gazetteers genesis gutenberg hmm_treebank_pos_tagger \
    ieer inaugural indian jeita kimmo knbc large_grammars lin_thesaurus mac_morpho machado \
    masc_tagged maxent_ne_chunker maxent_treebank_pos_tagger moses_sample movie_reviews \
    mte_teip5 names nps_chat omw opinion_lexicon panlex_swadesh paradigms \
    pil pl196x ppattach problem_reports product_reviews_1 product_reviews_2 propbank \
    pros_cons ptb punkt qc reuters rslp rte sample_grammars semcor senseval sentence_polarity \
    sentiwordnet shakespeare sinica_treebank smultron snowball_data spanish_grammars \
    state_union stopwords subjectivity swadesh switchboard tagsets timit toolbox treebank \
    twitter_samples udhr2 udhr unicode_samples universal_tagset universal_treebanks_v20 \
    verbnet webtext word2vec_sample wordnet wordnet_ic words ycoe && \
    # Stop-words
    pip install stop-words && \
    # clean up
    find /usr/share/nltk_data/ -name *.zip | xargs -n1 -I@ rm @ && \ 
    rm -rf /root/.cache/pip/*

# expose jupyter port 
EXPOSE 8888 

# start jupyter at container start
CMD ["startup.sh"] 

# copy jupyter startscript into the container
COPY start-notebook.sh /usr/local/bin/ 

# copy startup script into the container
COPY startup.sh /usr/local/bin/ 
