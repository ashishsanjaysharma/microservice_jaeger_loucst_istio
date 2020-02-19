#to run istio on local machine
the default profile is modified to run on 4gb ram and 4 cpus.

replace the original default profile with the modified default profile from the repo in install/kubernetes/operator/profiles


```
cd  istio-1.4.2
install/kubernetes/operator/profiles

```

#to run on minikube, istio requires specific version of kubernetes and one of them is v1.14.2
```
minikube start --memory=4064 --cpus=4 --kubernetes-version=v1.14.2 --vm-driver=virtualbox
```

#to get istio ns pods
```
kubectl get pods -n istio-system
```

#to get istio ns services
```
kubectl get svc -n istio-system
```

#to auto-inject isito sidecar
```
kubectl label namespace default istio-injection=enabled
```

#to generate the pods with default profile

```
cd istio-1.4.2
cd bin
./istioctl manifest apply --set profile=../install/kubernetes/operator/profiles/default.yaml  --set values.kiali.enabled=true \
    --set "values.kiali.dashboard.jaegerURL=http://jaeger-query:16686" \
    --set "values.kiali.dashboard.grafanaURL=http://grafana:3000"
```

#to delete the pods genereated by default profile
```
cd istio-1.4.2
cd bin
./istioctl manifest generate --set profile=../install/kubernetes/operator/profiles/default.yaml | kubectl delete -f -
```
