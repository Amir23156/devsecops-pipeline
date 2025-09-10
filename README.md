# DevSecOps Pipeline with AWS EKS

## Overview
This project demonstrates a full **DevSecOps pipeline** for a containerized **Flask microservice** running on **Amazon EKS (Elastic Kubernetes Service)**.  
It includes:
- Continuous Integration (CI) with GitHub Actions
- Security scanning using **Trivy**
- Automatic deployment to **Amazon EKS**
- Zero-downtime rolling updates
- Load balancing with an AWS Elastic Load Balancer
- GitHub OIDC integration for secure, secretless AWS authentication

---

## Architecture

### Flow:
1. Developer pushes code to GitHub.
2. GitHub Actions workflow triggers automatically.
3. The **CI stage**:
   - Builds the Docker image.
   - Runs vulnerability scans with **Trivy**.
   - Pushes the image to **Docker Hub**.
4. The **CD stage**:
   - Assumes an AWS IAM role via OIDC.
   - Deploys the updated image to **Amazon EKS**.
   - Performs a rolling update with zero downtime.
5. AWS Elastic Load Balancer exposes the service to external users.

---

### Architecture Diagram
```mermaid
flowchart LR
  Dev[Developer] -->|Push Code| GitHub

  subgraph CI[GitHub Actions CI/CD]
    GitHub --> Build[Build & Trivy Scan]
    Build --> PushImage[Push to Docker Hub]
    PushImage -.-> DockerHub[(Docker Hub)]
    Build --> Deploy[Deploy to AWS EKS via OIDC]
  end

  subgraph AWS[Amazon Web Services]
    IAM[IAM Role - OIDC]
    Deploy --> IAM
    IAM --> EKS[EKS Cluster: devsecops-cluster]
    EKS --> Pods[Flask Pods (2 Replicas)]
    Pods --> SVC[LoadBalancer Service]
    SVC --> ELB[Elastic Load Balancer]
    ELB --> User[External Users]
  end
```
### Project Structure
devsecops-pipeline/
│
├── app/                  # Flask application
│   ├── main.py           # Flask API code
│   └── Dockerfile        # Dockerfile for building the app
│
├── k8s/                  # Kubernetes manifests
│   ├── namespace.yaml    # Namespace definition
│   ├── deployment.yaml   # Flask app deployment
│   └── service.yaml      # LoadBalancer service
│
├── .github/
│   └── workflows/
│       ├── ci.yml        # Build & Scan pipeline
│       └── ci-cd-eks.yml # Full CI/CD with EKS deploy
│
├── requirements.txt      # Python dependencies
└── README.md

## Setup Instructions

### Prerequisites
Before starting, ensure you have the following installed and configured:

- **AWS account** with EKS enabled
- **kubectl** installed
- **eksctl** installed
- **Docker** installed
- **GitHub OIDC role** configured with the following permissions:
  - `AmazonEKSClusterPolicy`
  - `AmazonEKSWorkerNodePolicy`
  - `AmazonEC2ContainerRegistryFullAccess`

### 1. Clone the Repository
git clone https://github.com/Amir23156/devsecops-pipeline.git
cd devsecops-pipeline

### 2. Build and Run Locally
docker build -t flask-app:latest -f app/Dockerfile .
docker run -p 5000:5000 flask-app:latest

### 3. Test Endpoint
curl http://127.0.0.1:5000/health
curl http://127.0.0.1:5000/metrics
curl http://127.0.0.1:5000/orders


### 4. Deploy to Kubernetes (Local Minikube)
kubectl apply -f k8s/
kubectl get pods -n devsecops
Then Port Forward to test :
kubectl -n devsecops port-forward svc/flask-app 8080:80
curl http://127.0.0.1:8080/health

## Deploy to Amazon EKS

We first want to create an EKS cluster from CloudShell :
eksctl create cluster \
  --name devsecops-cluster \
  --region us-east-1 \
  --nodes 2 \
  --node-type t3.medium \
  --version 1.29
Then we can verify the cluster simply by running : kubectl get nodes

## Security Integration

We run a trivy vulnerability check through the command : trivy image flask-app:latest
**Automated Scanning** Trivy runs automatically during GitHub Actions CI:
- Scans the Docker image for vulnerabilities.
- Fails the pipeline if critical vulnerabilities are found.

## CI/CD Workflow 
### CI Pipeline (`.github/workflows/ci.yml`)

Triggered on every push or pull request:

1. **Build** Docker image.
2. **Run** Trivy vulnerability scan.
3. **Push** Docker image to Docker Hub.

---

### CD Pipeline (`.github/workflows/ci-cd-eks.yml`)

Triggered after a successful CI build:

- **Assumes** AWS IAM role via OIDC.
- **Updates** Kubernetes manifests.
- **Deploys** new version to **Amazon EKS** with zero downtime using rolling updates.

## Accessing the App via AWS
After deployment we can run : kubectl -n devsecops get svc flask-app
<img width="1149" height="105" alt="image" src="https://github.com/user-attachments/assets/503f9296-0d81-41a1-a785-13bd5816619d" />
And we can see the app running and test its endpoints :
![Capture d’écran 2025-09-10 030010](https://github.com/user-attachments/assets/9079ea8f-d5dd-4f00-a767-495bf207cbf3)





