"""
Helper to setup or restore postgres database from K8s
for platform, doctor_api & tm_oauth


Author: Khoa Le
Version: Nov 19, 2021
"""

import cprint as p
import subprocess
import numpy

commands = {
    "feature-staging": ["tm-kubectx", "-e", "feature-staging"],
    "get-namespaces": ["kubectl", "get", "namespaces"],
    "get-pods-from-namespace": ["kubectl", "get", "pods","-n"],
    "interactive-terminal": ["kubectl", "exec", "-n", "$NAME_SPACE", "-it", "$POD", "--", "bash", "-c", "/bin/bash"]
}

def actions():
    p.cprint("______________________________________________", p.bcolors.BOLD)
    p.cprint("Actions:", p.bcolors.BOLD)
    p.cprint("[1] Connect to feature-staging", p.bcolors.WARNING)
    p.cprint("[2] Get namespaces", p.bcolors.WARNING)
    p.cprint("[3] Get KMG namespaces", p.bcolors.WARNING)
    p.cprint("[4] Test", p.bcolors.WARNING)
    p.cprint("\n q to quit", p.bcolors.WARNING)

def main():
    stop = False
    while (not stop):
        actions()
        action = raw_input()
        if '1' in action:
            tm_kube_feature_staging()
        elif '2' in action:
            get_namespaces('')
        elif '3' in action:
            get_namespaces('kmg')
        elif '4' in action:
            test()
        if 'q' in action:
            stop = True
            quit()

def tm_kube_feature_staging():
    p.cprint('Connecting to tm-k8s feature-staging ...', p.bcolors.HEADER)
    output = subprocess.check_output(commands['feature-staging'])
    p.cprint(output, p.bcolors.OKGREEN)

def get_namespaces(kmg_filter):
    p.cprint('Getting KMG namespaces...' if kmg_filter else 'Getting namespaces...', p.bcolors.OKGREEN)
    try:
        output = subprocess.check_output(commands["get-namespaces"])
        namespaces = output.splitlines()
        kmg = []
        others = []
        i = 1
        kmg_i = 0
        o_j = 0
        for idx, line in enumerate(namespaces):
            if 'NAME' in line: continue
            if 'kmg-' in line:
                kmg.append(line)
            else:
                others.append(line)

        if kmg_filter:
            for l in kmg:
                p.cprint("[" + str(kmg_i) + "] " + l, p.bcolors.BOLD)
                kmg_i += 1
            get_pods_from_namespace(kmg[int(raw_input()) - 1])
        else:
            for l in others:
                p.cprint("[" + str(o_j) + "] " + l, p.bcolors.BOLD)
                o_j += 1
            get_pods_from_namespace(others[int(raw_input()) - 1])

    except subprocess.CalledProcessError as e:
        p.cprint('Something went wrong', p.bcolors.FAIL)

def get_pods_from_namespace(namespace):
    if 'q' in namespace: quit()

    namespace = namespace[0:namespace.index('Active')].strip()
    p.cprint('Getting pods from ' + namespace + '...', p.bcolors.OKGREEN)
    query = commands["get-pods-from-namespace"]
    query.append(namespace)
    output = subprocess.check_output(query).splitlines()

    # 1 indexed
    i = 1
    for idx, line in enumerate(output):
        if 'NAME' in line:
            p.cprint('   ' + line, p.bcolors.BOLD)
            continue

        p.cprint("[" + str(i) + "] " + line, p.bcolors.BOLD)
        i+=1
    pod = output[int(raw_input())]
    pod = pod[0:pod.index('  ')].strip()

    take_pod_action(namespace, pod)

def take_pod_action(namespace, pod):
    p.cprint('Available actions for pod ' + pod + ' in namespace ' + namespace, p.bcolors.OKGREEN)
    p.cprint('[1] Interactive terminal', p.bcolors.BOLD)
    command = commands['interactive-terminal']
    command[3] = namespace
    command[5] = pod
    try:
        ouput = subprocess.check_call(command)
    except Exception as e:
        p.cprint('Ran:', p.bcolors.WARNING)
        print(' '.join(output.args))
        p.cprint('Something went wrong \n' + e, p.bcolors.FAIL)

def test():
    nums = [
        "NAME                                       READY   STATUS    RESTARTS   AGE",
        "cove-kmg-1298-857fbb874f-ksq5s             2/2     Running   0          28h",
        "dashboard-kmg-1298-554db85dd8-qtxwl        2/2     Running   0          2d2h"
    ]
    numpy.delete(nums, 0)

    while True:
        for idx, lin in enumerate(nums):
            print(lin)
        a = raw_input()
        if "r" in a:
            exit()
        print(">>> " + a)


if __name__ == '__main__':
    main()
