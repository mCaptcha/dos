#FROM rust:latest as planner
#RUN cargo install cargo-chef
#WORKDIR /src
#COPY . /src/
#RUN cargo chef prepare --recipe-path recipe.json
#
#FROM rust:latest as cacher
#WORKDIR /src/
#RUN cargo install cargo-chef
#COPY --from=planner /src/recipe.json recipe.json
#RUN cargo chef cook --release --recipe-path recipe.json

FROM rust:latest as rust
WORKDIR /src
COPY . .
#COPY --from=cacher /src/target target
RUN cargo --version
RUN cargo build --release

FROM debian:bullseye as mcaptcha-dos-server
LABEL org.opencontainers.image.source https://github.com/mCaptcha/dos
RUN useradd -ms /bin/bash -u 1001 mcaptcha-dos-server
WORKDIR /home/mcaptcha-dos-server
COPY --from=rust /src/target/release/mcaptcha-dos-server /usr/local/bin/
COPY --from=rust /src/config/default.toml /etc/mcaptcha-dos/config.toml
USER mcaptcha-dos-server
CMD [ "/usr/local/bin/mcaptcha-dos-server" ]
