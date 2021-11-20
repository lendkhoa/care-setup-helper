"""
Helper to setup or restore postgres database from K8s
for platform, doctor_api & tm_oauth

Author: Khoa Le
Version: Nov 19, 2021
"""

import cprint as p
import subprocess

def main():
    print("Hello, world")
    #tm_kube_feature_staging()
    get_namespaces()

def tm_kube_feature_staging():
    output = subprocess.check_output(["tm-kubectx", "-e", "feature-staging"])
    p.cprint(output, p.bcolors.BOLD)

def get_namespaces():
    output = subprocess.check_output(["kubectl", "get", "namespaces"])
    namespaces = output.splitlines()
    i = 1
    for idx, line in enumerate(namespaces):
        if "kmg-" in line:
            p.cprint("[" + str(i) + "]" + line, p.bcolors.OKGREEN)
            i+=1


if __name__ == '__main__':
    main()
