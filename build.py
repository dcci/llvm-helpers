import git
from git import Repo
import os
import shutil
import sys
import subprocess

def git_hash(checkout_dest):
    repo = git.Repo(checkout_dest)
    return repo.head.object.hexsha

def git_reset(checkout_dest, sha):
    repo = git.Repo(checkout_dest)
    repo.git.reset(sha)

class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

def clone_repo(skip_checkout, checkout_dest):
    repo_url = "https://github.com/llvm-mirror/llvm"
    if skip_checkout:
        print("Skipping checkout")
    else:
        print("Cloning llvm repo")
        Repo.clone_from(repo_url, os.getcwd() + "/llvm-repo", progress=Progress())

def create_build(build_dir):
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

def cmake(build_dir, checkout_dest):
    os.chdir(build_dir)
    assert os.getcwd() == build_dir, "os.chdir() fail"
    cmd = ["cmake", "-G", "Ninja", "-DCMAKE_BUILD_TYPE=Release", checkout_dest]
    rc = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=False)
    if rc != 0:
        print("cmake invocation failed")
        sys.exit(rc)

def ninja(checkout_dest, build_dir, dest_dir):
    binary_name = "opt"
    os.chdir(build_dir)
    assert os.getcwd() == build_dir, "os.chdir() fail"
    cmd = ["ninja", "opt"]
    rc = subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=False)
    if rc != 0:
        print("ninja invocation failed")
        sys.exit(rc)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    shutil.copy2(build_dir + "/bin/" + binary_name, \
        dest_dir + "/" + binary_name + "-" + git_hash(checkout_dest))

def main():
    checkout_dest = os.getcwd() + "/llvm-repo"
    skip_checkout = True
    build_dir = os.getcwd() + "/build"
    dest_dir = os.getcwd() + "/result"
    hash_list = ["7f580b605b2cec5e68ce68ed0e57f564b2ae9bb3", "ab968f698e440b3ca2e2ebd209fc250ae075e69c", "1c4b8129419698a189be6119cd9d7b971432ffb1"]

    # FIXME: check prerequisites (cmake, ninja in $PATH).
    clone_repo(skip_checkout, checkout_dest)
    create_build(build_dir)
    cmake(build_dir, checkout_dest)
    for sha in hash_list:
        git_reset(checkout_dest, sha)
        ninja(checkout_dest, build_dir, dest_dir)
    sys.exit(0)

if __name__ == "__main__":
    main()
