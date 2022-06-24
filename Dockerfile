# This file builds a container for the Aidos-1 planner. See README.md for
# instructions on how to use it.

# The recipe below implements a Docker multi-stage build:
# <https://docs.docker.com/develop/develop-images/multistage-build/>

###############################################################################
# A first image to build the planner
###############################################################################
FROM ubuntu:20.04 AS builder

# Set up environment variables.
ENV CXX g++
ENV CPLEX_INSTALLER cplex_studio129.linux-x86-64.bin
ENV DOWNWARD_CPLEX_ROOT /opt/ibm/ILOG/CPLEX_Studio129/cplex
ENV OSI_VERSION Osi-0.107.9
ENV DOWNWARD_COIN_ROOT /opt/osi
ENV TZ=Europe/Zurich
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies.
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        ca-certificates \
        cmake           \
        default-jre     \
        g++             \
        git             \
        libgmp3-dev     \
        make            \
        python          \
        unzip           \
        wget         && \
    rm -rf /var/lib/apt/lists/*

# Install CPLEX.
WORKDIR /third-party/cplex
COPY $CPLEX_INSTALLER .
RUN ./$CPLEX_INSTALLER -DLICENSE_ACCEPTED=TRUE -i silent

# Install OSI with support for CPLEX.
WORKDIR /workspace/osi/
RUN wget http://www.coin-or.org/download/source/Osi/$OSI_VERSION.tgz && \
    tar xvzf $OSI_VERSION.tgz && \
    cd $OSI_VERSION && \
    mkdir $DOWNWARD_COIN_ROOT && \
    ./configure CC="gcc"  CFLAGS="-pthread -Wno-long-long" \
                CXX="g++" CXXFLAGS="-pthread -Wno-long-long" \
                LDFLAGS="-L$DOWNWARD_CPLEX_ROOT/lib/x86-64_linux/static_pic" \
                --without-lapack --enable-static=yes \
                --prefix="$DOWNWARD_COIN_ROOT" \
                --disable-zlib --disable-bzlib \
                --with-cplex-incdir=$DOWNWARD_CPLEX_ROOT/include/ilcplex \
                --with-cplex-lib="-lcplex -lm -ldl"  && \
    make && \
    make install

# Install Fast Downward.
WORKDIR /workspace/
COPY src src
COPY driver driver
COPY aidos_build_configs.py aidos_build_configs.py
COPY build.py build.py
COPY build_configs.py build_configs.py
COPY fast-downward.py fast-downward.py
RUN ./build.py aidos_ipc && \
    strip --strip-all builds/aidos_ipc/bin/downward

###############################################################################
# The final image to run the planner
###############################################################################
FROM ubuntu:20.04 AS runner

RUN apt-get update && apt-get install --no-install-recommends -y \
    python  \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/aidos/

# Copy the relevant files from the previous docker build into this build.
COPY --from=builder /workspace/fast-downward.py .
COPY --from=builder /workspace/builds/aidos_ipc/bin/ ./builds/aidos_ipc/bin/
COPY --from=builder /workspace/driver ./driver
COPY --from=builder /opt/ibm/ILOG/CPLEX_Studio129/cplex/bin/x86-64_linux /opt/ibm/ILOG/CPLEX_Studio129/cplex/bin/x86-64_linux
COPY --from=builder /opt/osi /opt/osi

ENV DOWNWARD_CPLEX_ROOT=/opt/ibm/ILOG/CPLEX_Studio129/cplex
ENV DOWNWARD_COIN_ROOT=/opt/osi
ENV LD_LIBRARY_PATH=$DOWNWARD_CPLEX_ROOT/bin/x86-64_linux:$DOWNWARD_COIN_ROOT/lib

# We enumerate the three stages to leave out validation stage (which would need VAL).
ENTRYPOINT ["/workspace/aidos/fast-downward.py", "--build=aidos_ipc", "--translate", "--preprocess", "--search"]
