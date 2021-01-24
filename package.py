import os

app_name = "job-keyword"
docker_tag = app_name + ":" + "prod"

def git_pull():
    run_cmd("git pull")

def build_image():
    print_cmd("eval $(minikube docker-env)")
    print_cmd("docker build --tag=" + docker_tag + " --force-rm=true .")
    print_cmd("eval $(minikube docker-env -u)")

def k8s_deploy():
    print_cmd("kubectl delete deployment " + app_name)
    print_cmd("kubectl create deployment " + app_name + " --image=" + docker_tag)


def run_sudo_cmd(cmd):
    cmd = "sudo " + cmd
    print cmd
    os.system(cmd)

def run_cmd(cmd):
    print cmd
    os.system(cmd)

def print_cmd(cmd):
    print cmd

if __name__ == '__main__':
    git_pull()
    build_image()
    k8s_deploy()
