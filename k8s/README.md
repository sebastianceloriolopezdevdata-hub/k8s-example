# Kubernetes manifests for Minikube

## 1) Point Docker to Minikube
```bash
minikube start
minikube docker-env
# Linux/macOS
 eval $(minikube docker-env)
# PowerShell
 minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

## 2) Build images inside Minikube
```bash
docker build -t skyroute/weather-service:1.0.0 ./weather-service
docker build -t skyroute/users-service:1.0.0 ./users-service
docker build -t skyroute/frontend:1.0.0 ./frontend
```

Alternative:
```bash
minikube image build -t skyroute/weather-service:1.0.0 ./weather-service
minikube image build -t skyroute/users-service:1.0.0 ./users-service
minikube image build -t skyroute/frontend:1.0.0 ./frontend
```

## 3) Deploy
```bash
kubectl apply -f k8s/all-in-one.yaml
```

Or with kustomize:
```bash
kubectl apply -k k8s
```

## 4) Validate
```bash
kubectl get all -n skyroute
kubectl get pods -n skyroute
kubectl describe pod -n skyroute <pod-name>
```

## 5) Open the app
```bash
minikube service frontend -n skyroute --url
```

You can also test the internal APIs:
```bash
kubectl port-forward -n skyroute svc/weather-service 8001:8000
kubectl port-forward -n skyroute svc/users-service 8002:8000
```

## 6) Scale a service
```bash
kubectl scale deployment weather-service --replicas=2 -n skyroute
```

## 7) Delete everything
```bash
kubectl delete -f k8s/all-in-one.yaml
```
