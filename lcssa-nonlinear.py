# Quick script to show that LCSSA is non-linear.
# Example to trigger the behaviour:
# python measure.py ./llvm-stress ./opt 300000 10000 100000
# Currently large part of the time is spent in the SSA updater.
# Requires an llvm-checkout (with `llvm-stress` and `opt` available)
# Require `matplotlib` to plot the results. 

import matplotlib.pyplot as plt
import sys
import subprocess
import time

from sys import argv

def run(llvm_stress_path, opt_path, max_size, stride, start_size):
  time_arr = []
  size_arr = []
  for size in xrange(int(start_size), int(max_size), int(stride)):
    start_time = time.time() 
    generator = subprocess.Popen([llvm_stress_path, "-size", str(size)],
                                 stdout=subprocess.PIPE)
    opt = subprocess.Popen([opt_path, "-lcssa", "-o", "/dev/null"],
                           stdin=generator.stdout)
    generator.wait()
    end_time = time.time()
    time_arr.append(end_time - start_time)
    print(size)
    print(end_time - start_time)
    size_arr.append(size)
  return (time_arr, size_arr)

def plot(time_arr, size_arr):
  plt.plot(size_arr, time_arr, 'g^')
  plt.show()
  return

def main():
  if len(argv) != 6: 
    print("usage: python measure.py llvm-stress-binary opt-binary max_size stride start_size")
    sys.exit(1)
  (time_arr, size_arr) = run(argv[1], argv[2], argv[3], argv[4], argv[5])
  plot(time_arr, size_arr)
  sys.exit(0)

if __name__ == "__main__":
  main()
