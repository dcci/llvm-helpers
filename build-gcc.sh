#!/bin/sh

cd ~
sudo apt install git libmpc-dev libmpfr-dev libgmp-dev flex bison cmake ninja-build
git clone git://gcc.gnu.org/git/gcc.git
mkdir gcc-build
cd gcc-build
../gcc/configure --enable-languages=c,c++ --prefix=$HOME/gcc-install
make -j96
make install

cd ~
git clone https://github.com/llvm-mirror/test-suite
cd test-suite
mkdir build-gcc
cd build-gcc
cmake -GNinja -DCMAKE_C_COMPILER=$HOME/gcc-install/bin/gcc -DCMAKE_CXX_COMPILER=$HOME/gcc-install/bin/g++ ../
