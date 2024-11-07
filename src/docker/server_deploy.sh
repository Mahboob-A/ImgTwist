#!/bin/bash 

set -o errexit 
set -o nounset 

if [[ -z "${GENP_ALGOCM_EC2_IP_ADDR}" ]]; then
    echo "EC2 Server IP Address for ImgTwist is not defined."
    echo "Please export the EC2 server IP address in host machine and try again."
    exit 1
fi 

tar --exclude='.git' --exclude='./venv' --exclude='/__pycache__/' -cvf ./dev_imgtwist_deply.tar .

echo "Uploading the Project to the server ... " 

rsync -e "ssh -i ${GENP_ALGOCM_EC2_PEM}" ./dev_imgtwist_deply.tar ubuntu@"${GENP_ALGOCM_EC2_IP_ADDR}":/tmp/dev_imgtwist_deply.tar

echo "Upload complete ... "

echo "Building the docker compose  ... "

ssh -i "${GENP_ALGOCM_EC2_PEM}" -o StrictHostKeyChecking=no ubuntu@"${GENP_ALGOCM_EC2_IP_ADDR}" << 'ENDSSH'

    PROJECT_PATH=/home/ubuntu/img-twist/backend 
    LOG_PATH=/home/ubuntu/mg-twist/logs
    WAIT_TIME=10

    echo "Creating directory for project and logs... "
    mkdir -p "$PROJECT_PATH"
    mkdir -p "$LOG_PATH"

    echo "Creating the log files ... "
    touch "$LOG_PATH"/general.log 
    touch "$LOG_PATH"/error.log 

    echo "Deleting the old project files ... "
    rm -rf "$PROJECT_PATH"/* 

    echo "Extracting the dev_imgtwist_deply.tar file in specified project directory ... "
    tar -xf /tmp/dev_imgtwist_deply.tar -C "$PROJECT_PATH"

    echo " Taking down running project docker containers ... "
    docker_compose_down_output=$(docker compose -p dev_imgtwist_backend_api -f "$PROJECT_PATH"/dev.yml down)
    docker_compose_down_exit_code=$?
    
    if [[ $docker_compose_down_exit_code -ne 0 ]]; then 
        echo "Error: Taking down the running docker compose containers failed. (Exit code: $docker_compose_down_exit_code)"
        echo -e "\nError: Taking DOWN the running docker compose containers failed\nError Message: $docker_compose_down_output\nExit code: $docker_compose_down_exit_code\nTime: $(date +%Y-%m-%d_%H-%M-%S)" >> "$LOG_PATH"/error.log
        exit $docker_compose_down_exit_code
    fi 

    echo "Waiting for \"$WAIT_TIME\" seconds before running the docker compose file ... "
    sleep "$WAIT_TIME"

    echo "Starting the docker compose file ... "
    docker_compose_up_output=$(sudo docker compose -p dev_imgtwist_backend_api -f $PROJECT_PATH/dev.yml up --build -d --remove-orphans)
    docker_compose_up_exit_code=$?

    if [[ $docker_compose_up_exit_code -ne 0 ]]; then 
        echo "Error: Starting the docker compose containers failed. (Exit code: $docker_compose_up_exit_code)"
        echo -e "\nError: Starting the docker compose containers failed\nError Message: $docker_compose_up_output\nExit code: $docker_compose_up_exit_code\nTime: $(date +%Y-%m-%d_%H-%M-%S)" >> "$LOG_PATH"/error.log
        exit $docker_compose_up_exit_code
    fi 

    echo -e "\nSuccess: New deployment is successful.\nTime: $(date +%Y-%m-%d_%H-%M-%S)" >> "$LOG_PATH"/general.log

ENDSSH

echo "Build and Deploy in the Server is Successful ... "