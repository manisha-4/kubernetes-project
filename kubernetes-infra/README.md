# Kubernetes Deployment Guide for Cat E-Commerce

This folder contains all Kubernetes manifests for deploying the cat e-commerce application on local Kubernetes (Docker Desktop or Minikube).

## Prerequisites

### Install Kubernetes Locally

**Option 1: Docker Desktop (Recommended for Mac/Windows)**
```bash
# Enable Kubernetes in Docker Desktop
# Preferences > Kubernetes > Enable Kubernetes
# Wait for cluster to be ready
```

**Option 2: Minikube (Linux/Mac/Windows)**
```bash
# Install Minikube
brew install minikube

# Start cluster
minikube start --cpus 4 --memory 8192 --driver=docker

# Enable ingress addon
minikube addons enable ingress
```

**Verify Kubernetes is running:**
```bash
kubectl cluster-info
kubectl get nodes
```

## Manifest Files

| File | Purpose |
|------|---------|
| `01-namespace.yaml` | Create `cat-ecommerce` namespace |
| `02-configmap.yaml` | Frontend environment configuration |
| `03-frontend-deployment.yaml` | Frontend React app deployment |
| `04-frontend-service.yaml` | Frontend ClusterIP service |
| `05-ingress.yaml` | Ingress for routing traffic |
| `06-hpa.yaml` | Horizontal Pod Autoscaler |
| `07-backend-deployment.yaml` | Backend Flask app deployment |
| `08-backend-service.yaml` | Backend ClusterIP service |
| `09-backend-secrets.yaml` | Backend secrets (DB, JWT) |

## Step-by-Step Deployment

### 1. Build Docker Images

**Frontend:**
```bash
cd frontend
docker build -t cat-frontend:latest .
cd ..
```

**Backend:**
```bash
cd backend
docker build -t cat-backend:latest .
cd ..
```

Verify images:
```bash
docker images | grep cat-
```

### 2. Create Namespace
```bash
kubectl apply -f kubernetes-infra/01-namespace.yaml
```

### 3. Create ConfigMap (Frontend Config)
```bash
kubectl apply -f kubernetes-infra/02-configmap.yaml
```

### 4. Create Secrets (Backend Secrets)
```bash
kubectl apply -f kubernetes-infra/09-backend-secrets.yaml
```

### 5. Deploy Frontend
```bash
kubectl apply -f kubernetes-infra/03-frontend-deployment.yaml
kubectl apply -f kubernetes-infra/04-frontend-service.yaml
```

### 6. Deploy Backend
```bash
kubectl apply -f kubernetes-infra/07-backend-deployment.yaml
kubectl apply -f kubernetes-infra/08-backend-service.yaml
```

### 7. Setup Ingress
```bash
kubectl apply -f kubernetes-infra/05-ingress.yaml
```

### 8. Setup Auto-scaling
```bash
kubectl apply -f kubernetes-infra/06-hpa.yaml
```

### Deploy All at Once
```bash
kubectl apply -f kubernetes-infra/
```

## Verify Deployment

```bash
# Check namespace
kubectl get namespaces

# Check deployments
kubectl get deployments -n cat-ecommerce

# Check pods
kubectl get pods -n cat-ecommerce

# Check services
kubectl get services -n cat-ecommerce

# Check ingress
kubectl get ingress -n cat-ecommerce
```

## Access Application

### Local Development (without Ingress)

**Port Forward Frontend:**
```bash
kubectl port-forward -n cat-ecommerce svc/frontend-service 3000:80
# Access: http://localhost:3000
```

**Port Forward Backend:**
```bash
kubectl port-forward -n cat-ecommerce svc/backend-service 5000:5000
# Access: http://localhost:5000
```

### Using Ingress (cat-shop.local)

1. **Update /etc/hosts** (Mac/Linux):
```bash
sudo nano /etc/hosts
# Add line:
127.0.0.1 cat-shop.local
```

2. **For Docker Desktop:**
- Ingress is available at `localhost`
- Access: http://cat-shop.local

3. **For Minikube:**
```bash
# Get Minikube IP
minikube ip

# Update /etc/hosts with Minikube IP:
192.168.99.100 cat-shop.local

# Or use tunnel
minikube tunnel
```

## Useful kubectl Commands

```bash
# View deployment details
kubectl describe deployment frontend -n cat-ecommerce

# View pod logs
kubectl logs -n cat-ecommerce -l app=frontend --tail=50

# Get into a pod
kubectl exec -it <pod-name> -n cat-ecommerce /bin/sh

# Watch pods
kubectl get pods -n cat-ecommerce -w

# Delete deployment
kubectl delete deployment frontend -n cat-ecommerce

# Scale deployment
kubectl scale deployment frontend --replicas=3 -n cat-ecommerce

# Check HPA status
kubectl get hpa -n cat-ecommerce
```

## Troubleshooting

### Pods not starting
```bash
kubectl describe pod <pod-name> -n cat-ecommerce
kubectl logs <pod-name> -n cat-ecommerce
```

### Image pull errors
```bash
# Make sure images are built locally
docker images | grep cat-

# Rebuild if needed
docker build -t cat-frontend:latest ./frontend
docker build -t cat-backend:latest ./backend
```

### Ingress not working
```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# For Minikube, enable ingress addon
minikube addons enable ingress
```

### Port forwarding
```bash
# If port is in use, kill process
lsof -i :3000  # Find process
kill -9 <PID>  # Kill it
```

## Scaling

### Manual Scaling
```bash
kubectl scale deployment frontend --replicas=5 -n cat-ecommerce
```

### Auto-scaling
```bash
# Check HPA status
kubectl get hpa -n cat-ecommerce

# View HPA details
kubectl describe hpa frontend-hpa -n cat-ecommerce
```

## Update Deployment

### Rebuild and redeploy
```bash
# Rebuild image
docker build -t cat-frontend:latest ./frontend

# Update deployment (changes image)
kubectl rollout restart deployment/frontend -n cat-ecommerce

# Check rollout status
kubectl rollout status deployment/frontend -n cat-ecommerce
```

## Delete Everything

```bash
# Delete specific deployment
kubectl delete deployment frontend -n cat-ecommerce

# Delete entire namespace
kubectl delete namespace cat-ecommerce
```

## Next Steps

For EKS (AWS) deployment, see the Terraform configuration in the `terraform/` folder.

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Docker Desktop Kubernetes](https://docs.docker.com/docker-for-mac/kubernetes/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/)
