if __name__ == '__main__':
    import os

    image_name = "job-keyword"
    # docker_tag = f"{socket.gethostbyname('alaitp-cloud')}:5555/{image_name}:dev"
    docker_tag = f"localhost:5555/{image_name}:local-dev"
    os.system(f"docker build --tag={image_name} --force-rm=true .")
    os.system(f"docker tag {image_name} {docker_tag}")
    os.system(f"docker push {docker_tag}")

# kubectl delete deploy job-keyword
# kubectl create deploy job-keyword --image=localhost:5555/job-keyword:local-dev