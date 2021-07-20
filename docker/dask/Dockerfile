FROM continuumio/miniconda3:4.8.2


RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2

RUN apt-get update && \
apt-get install -y --no-install-recommends \
        openjdk-11-jre

# Prints installed java version, just for checking
RUN java --version

# Setup JAVA_HOME, this is useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

RUN conda install --yes \
    -c conda-forge \
    python==3.8 \
    pyarrow \
    python-blosc \
    cytoolz \
    dask==2021.7.0 \
    lz4 \
    nomkl \
    numpy==1.18.1 \
    pandas==1.0.1 \
    tini==0.18.0 \
    && conda clean -tipsy \
    && find /opt/conda/ -type f,l -name '*.a' -delete \
    && find /opt/conda/ -type f,l -name '*.pyc' -delete \
    && find /opt/conda/ -type f,l -name '*.js.map' -delete \
    && find /opt/conda/lib/python*/site-packages/bokeh/server/static -type f,l -name '*.js' -not -name '*.min.js' -delete \
    && rm -rf /opt/conda/pkgs

COPY prepare.sh /usr/bin/prepare.sh

RUN mkdir /opt/app

ENTRYPOINT ["tini", "-g", "--", "/usr/bin/prepare.sh"]