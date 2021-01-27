import os

app_name = "job-keyword"
docker_tag = app_name
registry = "localhost:5555"
registry_tag = registry  + "/" + docker_tag

def git_pull():
    run_cmd("git pull")

def build_image():
    run_cmd("docker build --tag=" + docker_tag + " --force-rm=true .")
    run_cmd("docker tag " + docker_tag +  " " + registry_tag)
    run_cmd("docker push " + registry_tag)

def k8s_deploy():
    run_cmd("kubectl delete deployment " + app_name)
    run_cmd("kubectl create deployment " + app_name + " --image=" + registry_tag)


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
