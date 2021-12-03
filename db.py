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
    "get-pods-from-namespace": ["kubectl", "get", "pods","-n", "$NAME_SPACE"],
    "interactive-terminal": ["kubectl", "exec", "-n", "$NAME_SPACE", "-it", "$POD", "--", "bash", "-c", "/bin/bash"],
    "generate-snap": ["pg_dump", "$DATABASE_URL", ">", "snap.sql"],
    "cp-snap": ["kubectl", "cp", "$NAME_SPACE/", "$POD:/", "$SERVICE", "/snap.sql"," ",  "./snap.sql"],
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
            print(">>> 1")
            for l in kmg:
                p.cprint("[" + str(kmg_i) + "] " + l, p.bcolors.BOLD)
                kmg_i += 1
            p.cprint("r to return", p.bcolors.WARNING)
            p.cprint("q to quit", p.bcolors.WARNING)
            action = raw_input()
            if 'r' in action: return
            if 'q' in action: quit()
            get_pods_from_namespace(kmg[int(action)])
        else:
            print(">>> 2")
            for l in others:
                p.cprint("[" + str(o_j) + "] " + l, p.bcolors.BOLD)
                o_j += 1
            p.cprint("r to return", p.bcolors.WARNING)
            p.cprint("q to quit", p.bcolors.WARNING)
            action = raw_input()
            if 'r' in action: return
            if 'q' in action: quit()
            get_pods_from_namespace(others[int(action)])

    except subprocess.CalledProcessError as e:
        p.cprint('Something went wrong', p.bcolors.FAIL)

def get_pods_from_namespace(namespace):
    if 'q' in namespace: quit()

    namespace = namespace[0:namespace.index('Active')].strip()
    p.cprint('Getting pods from ' + namespace + '...', p.bcolors.OKGREEN)
    commands["get-pods-from-namespace"][4] = namespace
    command = commands["get-pods-from-namespace"]
    output = subprocess.check_output(command).splitlines()

    # 1 indexed
    i = 1
    for idx, line in enumerate(output):
        if 'NAME' in line:
            p.cprint('   ' + line, p.bcolors.BOLD)
            continue

        print("[" + str(i) + "] " + line)
        i+=1

    p.cprint("r to return", p.bcolors.WARNING)
    p.cprint("q to quit", p.bcolors.WARNING)
    action = raw_input()
    if 'r' in action: return
    if 'q' in action: quit()

    pod = output[int(action)]
    pod = pod[0:pod.index('  ')].strip()

    take_pod_action(namespace, pod)

def take_pod_action(namespace, pod):
    p.cprint('Available actions for pod ' + pod + ' in namespace ' + namespace, p.bcolors.OKGREEN)
    p.cprint('[1] Interactive terminal', p.bcolors.WARNING)
    p.cprint('[2] Cp snap.sql to local', p.bcolors.WARNING)
    p.cprint('q to quit', p.bcolors.WARNING)

    pod_action = raw_input()
    if 'q' in pod_action: quit()
    pod_action = int(pod_action)
    try:
        if pod_action == 1:
            command = commands['interactive-terminal']
            command[3] = namespace
            command[5] = pod
            p.cprint('Opening interactive terminal for pod ' + pod, p.bcolors.OKGREEN)
            ouput = subprocess.check_call(command)
        elif pod_action == 2:
            command = commands['cp-snap']
            command[3] = namespace
            command[5] = pod
            p.cprint('Downloading snap.sql on pod ' + pod, p.bcolors.OKGREEN)
            ouput = subprocess.check_call(command)

    except Exception as e:
        p.cprint('Something went wrong \n' + e, p.bcolors.FAIL)

def test():
    subprocess.check_output(["./test.bsh"])



if __name__ == '__main__':
    main()
