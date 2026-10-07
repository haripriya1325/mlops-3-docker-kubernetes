# MLOps Experiment 3 - Docker + Kubernetes

This project follows the supplied lab guide: containerize a trained ML model with Docker,
deploy it to Kubernetes, expose it with a ClusterIP Service, port-forward it locally,
and scale the Deployment to 3 replicas.

## Project structure

```text
mlops_3/
├── data/
├── model/
│   └── student_model.pkl
├── src/
│   ├── __init__.py
│   └── app.py
├── tests/
│   └── test_api.py
├── Dockerfile
├── requirements.txt
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

## 1. Create/activate venv (PowerShell)

```powershell
cd C:\Users\harip\Downloads\mlops_3
python -m venv venv
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& .\venv\Scripts\Activate.ps1)
```

## 2. Verify tools

```powershell
python --version
docker --version
kubectl version --client
```

Docker Desktop must be running and Kubernetes must be enabled.

## 3. Install Python packages locally

```powershell
pip install -r requirements.txt
```

## 4. Run the FastAPI app locally

```powershell
python -m uvicorn src.app:app --host 0.0.0.0 --port 8000
```

Open another PowerShell:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Expected:

```text
{"status":"healthy"}
```

Prediction:

```powershell
$body = @{
  features = @(5,85,3,1,4,1,1,20,2,3,2,90,85,1,2)
} | ConvertTo-Json -Compress

Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## 5. Build Docker image

Stop the local uvicorn process first (Ctrl+C), then:

```powershell
docker build -t student-mlops:latest .
docker images
```

## 6. Run Docker container

```powershell
docker run -d --name student-ml-api -p 8000:8000 student-mlops:latest
docker ps
curl.exe http://127.0.0.1:8000/health
```

Prediction:

```powershell
$body = @{
  features = @(5,85,3,1,4,1,1,20,2,3,2,90,85,1,2)
} | ConvertTo-Json -Compress

Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## 7. Deploy to Kubernetes

If the Docker container is using port 8000, stop/remove it before port-forwarding later:

```powershell
docker stop student-ml-api
docker rm student-ml-api
```

Apply Deployment:

```powershell
kubectl apply -f k8s\deployment.yaml
kubectl get deployments
kubectl get pods
```

Apply Service:

```powershell
kubectl apply -f k8s\service.yaml
kubectl get services
kubectl get deployments,pods,services
```

## 8. Port-forward the Kubernetes Service

Keep this terminal open:

```powershell
kubectl port-forward service/student-ml-service 8000:8000
```

Expected:

```text
Forwarding from 127.0.0.1:8000 -> 8000
```

Open another PowerShell:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Prediction:

```powershell
$body = @{
  features = @(5,85,3,1,4,1,1,20,2,3,2,90,85,1,2)
} | ConvertTo-Json -Compress

Invoke-RestMethod -Uri "http://127.0.0.1:8000/predict" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body
```

## 9. Scale to 3 replicas

```powershell
kubectl scale deployment student-ml-deployment --replicas=3
kubectl get pods
kubectl get deployment student-ml-deployment
```

Expected:

```text
READY   UP-TO-DATE   AVAILABLE
3/3     3            3
```

Final verification:

```powershell
kubectl get deployment,pods,service
```

## 10. GitHub push

Create an empty GitHub repository first, then replace YOUR_USERNAME and YOUR_REPO.

```powershell
git init
git add .
git commit -m "MLOps experiment 3 Docker Kubernetes deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

If Git asks for authentication, use your GitHub authentication method (browser/Git Credential Manager or a Personal Access Token as applicable).

## Useful cleanup commands

```powershell
kubectl delete -f k8s\service.yaml
kubectl delete -f k8s\deployment.yaml
docker rm -f student-ml-api
```
