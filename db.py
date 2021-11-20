"""
Helper to setup or restore postgres database from K8s
for platform, doctor_api & tm_oauth


Author: Khoa Le
Version: Nov 19, 2021
"""

import cprint as p
import subprocess

commands = {
    "feature-staging": ["tm-kubectx", "-e", "feature-staging"],
    "get-namespaces": ["kubectl", "get", "namespaces"]
}

def actions():
    p.cprint("______________________________________________", p.bcolors.BOLD)
    p.cprint("Actions:", p.bcolors.BOLD)
    p.cprint("[1] Connect to feature-staging", p.bcolors.WARNING)
    p.cprint("[2] Get KMG namespaces", p.bcolors.WARNING)
    p.cprint("[3] Test", p.bcolors.WARNING)
    p.cprint("q to quit", p.bcolors.WARNING)

def main():
    stop = False
    while (not stop):
        actions()
        action = raw_input()
        if "1" in action:
            tm_kube_feature_staging()
        elif "2" in action:
            get_namespaces()
        elif '3' in action:
            test()
        if "q" in action:
            stop = True
            quit()

def tm_kube_feature_staging():
    p.cprint('Connecting to tm-k8s feature-staging ...', p.bcolors.HEADER)
    output = subprocess.check_output(commands['feature-staging'])
    p.cprint(output, p.bcolors.OKGREEN)

def get_namespaces():
    p.cprint('Getting KMG namespaces...', p.bcolors.OKGREEN)
    try:
        output = subprocess.check_output(commands["get-namespaces"])
        namespaces = output.splitlines()
        i = 1
        for idx, line in enumerate(namespaces):
            if "kmg-" in line:
                p.cprint("[" + str(i) + "]" + line, p.bcolors.BOLD)
                i+=1
    except subprocess.CalledProcessError as e:
        p.cprint('Something went wrong', p.bcolors.FAIL)

def test():
    p.cprint("Some work - DONE", p.bcolors.OKGREEN)


if __name__ == '__main__':
    main()
