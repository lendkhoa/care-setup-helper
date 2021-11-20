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
    "get-namespaces": ["kubectl", "get", "namespaces"],
    "get-pods-from-namespace": ["kubectl", "get", "pods","-n"]
}

def actions():
    p.cprint("______________________________________________", p.bcolors.BOLD)
    p.cprint("Actions:", p.bcolors.BOLD)
    p.cprint("[1] Connect to feature-staging", p.bcolors.WARNING)
    p.cprint("[2] Get KMG namespaces", p.bcolors.WARNING)
    p.cprint("[3] Test", p.bcolors.WARNING)
    p.cprint("\n q to quit", p.bcolors.WARNING)

def main():
    stop = False
    while (not stop):
        actions()
        action = raw_input()
        if '1' in action:
            tm_kube_feature_staging()
        elif '2' in action:
            get_namespaces()
        elif '3' in action:
            test()
        if 'q' in action:
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
        kmg = []
        i = 1
        kmg_i = 0
        for idx, line in enumerate(namespaces):
            if 'kmg-' in line:
                kmg.append(line)
                kmg_i += 1
                p.cprint("[" + str(i) + "] " + line, p.bcolors.BOLD)
                i+=1

        get_pods_from_namespace(kmg[int(raw_input()) - 1])

    except subprocess.CalledProcessError as e:
        p.cprint('Something went wrong', p.bcolors.FAIL)

def get_pods_from_namespace(namespace):
    namespace = namespace[0:namespace.index('Active')].strip()
    p.cprint('Getting pods from ' + namespace + '...', p.bcolors.OKGREEN)
    query = commands["get-pods-from-namespace"]
    query.append(namespace)
    pods = subprocess.check_output(query)
    print(pods)

    # i = 1
    # for idx, line in enumerate(pods):
    #     p.cprint("[" + str(i) + "] " + line, p.bcolors.BOLD)
    #     i+=1


def test():
    p.cprint("Test - DONE", p.bcolors.OKGREEN)
    q = commands["get-pods-from-namespace"]
    print(q)
    print(commands["get-pods-from-namespace"])
    q.append(">>")
    print(q)


if __name__ == '__main__':
    main()
