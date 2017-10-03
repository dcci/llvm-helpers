WORKDIR=$PWD/tmp
if [ -d $WORKDIR ]; then
  echo "Dirty workdir"
  echo $WORKDIR
  echo "Remove it and re-run"
  exit 1
fi

mkdir $WORKDIR
cd $WORKDIR

# Setup virtual environment
/usr/bin/virtualenv venv
. venv/bin/activate

# Checkout test-suite and LNT
for D in test-suite lnt
  do
    if [ ! -d "$D" ]; then
      git clone http://llvm.org/git/$D
    fi
  done

# Install LNT
pip install -r lnt/requirements.client.txt
python lnt/setup.py develop

# Install LIT
pip install  svn+http://llvm.org/svn/llvm-project/llvm/trunk/utils/lit/

# Create a sandbox directory
mkdir $PWD/sandbox

# Set some variables
SANDBOX=$PWD/sandbox
COMPILER=/home/davide/work/llvm/build-rel-noassert/
TESTSUITE=$PWD/test-suite       # We should've checked it out here
OPTSET=ReleaseLTO               # Or Os, or O0-g, or ReleaseThinLTO (see test-suite/cmake/cache for other options)

# Create sandbox
mkdir $SANDBOX
cd $SANDBOX

# Fill in LNT flags
LNT_FLAGS =" --sandbox $SANDBOX"
LNT_FLAGS+=" --no-timestamp"
LNT_FLAGS+=" --use-lit=lit"
LNT_FLAGS+=" --cc $COMPILER/bin/clang"
LNT_FLAGS+=" --cxx $COMPILER/bin/clang++"
LNT_FLAGS+=" --test-suite=$TESTSUITE"
LNT_FLAGS+=" --cmake-define TEST_SUITE_BENCHMARKING_ONLY=On"
LNT_FLAGS+=" --no-auto-name '${COMPILER%.*}'"
LNT_FLAGS+=" --output \"$SANDBOX/report.json\""
LNT_FLAGS+=" -C target-arm64-iphoneos -C $OPTSET"

LNT_FLAGS+=" --cmake-define TEST_SUITE_RUN_BENCHMARKS=Off"
LNT_FLAGS+=" --build-threads 1"
LNT_FLAGS+=" --cmake-define TEST_SUITE_SUBDIRS=\"CTMark\""

# Run LNT
lnt runtest test-suite ${LNT_FLAGS}

