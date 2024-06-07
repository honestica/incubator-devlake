# CONTRIBUTING - Lifen specifications

This document provides instructions on how to contribute to the Lifen Fork of the DevLake project.

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker: [Installation guide](https://docs.docker.com/get-docker/)
- Access to the Lifen Docker Hub repository where the images are stored.

## Developer Setup

1. **Login to Docker Hub**:
   Start by logging in to Docker Hub from your command line:
   ```bash
   docker login
   ```
   Enter your Docker Hub username and password when prompted.

2. **Clone the Repository**:
    Clone the Lifen Fork of the DevLake repository to your local machine:
    ```bash
    git clone https://github.com/honestica/incubator-devlake
    ```

3. **Copy .env file and override configuration**
    Copy the `.env.example` file to `.env` and fill in the required environment variables.
    ```bash
    cp env.example .env
    ```
    Override the following variables :
    - `ENCRYPTION_SECRET`: Generate yours with `openssl rand -base64 2000 | tr -dc 'A-Z' | fold -w 128 | head -n 1`

    You can also override the DEVLAKE_PLUGINS variable set in the `docker-compose-dev.yml` file to add or remove the plugins you want to use.

4. **Start the MySQL, Grafana containers and backend (devlake) containers:**:
    We provided a containered version of the backend to avoid to manage the dependencies on your local machine (python 3.9, go 20, libgit2...)
    Start the services using Docker Compose:
    ```bash
    docker-compose -f docker-compose-dev.yml up -d mysql grafana devlake
    ```

5. **Start the application**
    To run the backend, connect to the container and run the following commands:
    ```bash
       docker-compose -f docker-compose-dev.yml exec devlake /bin/bash
       make dev
    ```
    To run the frontend (a docker container could come)
    ```bash
       make configure-dev
    ```

## Building a new devlake-dev image

/!\ WIP /!\
To build a new version of the Docker image, run the following command in the root directory of the project:

```bash
docker build -t honestica/devlake-dev:versionX.Y -f Dockerfile-dev .
```
Replace `versionX.Y` with the appropriate version number for the new image.

## Pushing the Image to Docker
After building the image, push it to Docker Hub using the following command:

```bash
docker push honestica/devlake-dev:versionX.Y
```

Ensure that you replace `yourusername/devlake:versionX.Y` with the correct Docker Hub username, repository, and tag.

## Updating docker-compose.yml

After pushing the new image version, update the `docker-compose.yml` file in your repository to use the new image version if necessary.

1. Open `docker-compose.yml`.
2. Find the `image:` line under the service you updated.
3. Change the tag to the new version:
   ```yaml
   image: yourusername/devlake:versionX.Y
   ```
