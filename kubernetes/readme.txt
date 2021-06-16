Deploying in kubernetes cluster

You can test this deployment on your laptop using minikube. 
Please refer to https://minikube.sigs.k8s.io/docs/start/ to get started.

If you do not have kubectl installed, you can run kubectl using a shell alias,
    alias kubectl="minikube kubectl --"
Place above line in your .bash_aliases.

You should also have docker and docker-compose installed.

The following has been tested on minikube 1.20 cluster.

Steps:

    Open a command console
        cd to the backtest home folder, eg ~/work/backtest
    Start your minikube cluster
        minikube start
    Start the docker-env (for access to our images from within minikube)
        eval $(minikube docker-env)
    Generate a new .env file
        bin/gen_env.py prod.env
    Build our images (this will use the Dockerfile in our ./docker folders)
        docker-compose build
    Generate secrets from our .env file
        kubectl create secret generic bt-env-secrets --from-env-file=.env
    Run db (will attach ./dbdata for db files)
        kubectl apply -f kubernetes/db/volume.yml
        kubectl apply -f kubernetes/db/volume_claim.yml
        kubectl apply -f kubernetes/db/deployment.yml
        kubectl apply -f kubernetes/db/service.yml
    Run web
        kubectl apply -f kubernetes/web/deployment.yml
        kubectl apply -f kubernetes/web/service.yml
    Run nginx
        kubectl apply -f kubernetes/nginx/deployment.yml
        kubectl apply -f kubernetes/nginx/service.yml
    Enable ingress addon
        minikube addons enable ingress
    Run ingress to expose nginx externally
        kubectl apply -f kubernetes/ingress.yml
    Get thecube.atsc.org.my ip address
        kubectl get ingress
    Add minikube.local to /etc/hosts
        sudo vi /etc/hosts, then add line "ip_from_above  thecube.atsc.org.my"
    Access minikube dashboard to check everything started ok
        minikube dashboard
    Access backtest, 
        open a browser tab with url "http://thecube.atsc.org.my/"

    Stop minikube
        minikube stop
    Delete all clusters, else all existing deployments, services etc will be restarted
        minikube delete --all

