CC_PATH=/home/davide/work/llvm/build-clang/bin/clang

CC="$CC_PATH --target=aarch64-linux-musl -integrated-as" ./configure --disable-shared --prefix=/usr/local/musl-aarch64
make -j48
sudo make install

/usr/local/musl-aarch64/bin/musl-clang --version
