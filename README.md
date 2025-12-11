## Docker + Kubernetes + Self-Hosted Runner

Este projeto demonstra um pipeline completo de CI/CD usando GitHub Actions, Docker Hub e Kubernetes, com foco em ambientes de rede interna. Para a demonstração foi usado um projeto simples em Go (feito por IA)

 ### O objetivo principal é automatizar todo o fluxo:

Fazer build da aplicação (é nescessário rodar ./run.sh localmente no diretório ~/actions-runner)

Criar a imagem Docker

Publicar a imagem no Docker Hub

Atualizar o Deployment no Kubernetes automaticamente

#### Solução: Self-Hosted Runner

O Github Actions não acessa servidores em rede interna. Para permitir que o pipeline acesse o cluster, configurei um Self-Hosted GitHub Runner dentro do servidor Ubuntu 22.04 que contem um cluster kubernetes feito com kaind.
Assim, ele consegue:

✔ Executar kubectl localmente
✔ Fazer o build da imagem
✔ Enviar para o Docker Hub
✔ Atualizar o Deployment no cluster

📍 Onde instalei o runner:

/home/github/actions-runner

📍 Permissões necessárias

Eu precisei copiar o kubeconfig para o usuário do runner:

sudo mkdir -p /home/github/.kube

sudo cp /root/.kube/config /home/github/.kube/config

sudo chown -R github:github /home/github/.kube

### 🔧 Arquitetura do Projeto

k8s-deploy-demo/

│

├── app/

│ ├── main.go

│ └── Dockerfile

│

├── k8s/

│ ├── deployment.yaml

│ └── service.yaml

│

└── .github/

└── workflows/

└── deploy.yaml

### 🐳 Docker

A imagem da aplicação é construída usando o Dockerfile dentro da pasta /app:

FROM golang:1.20-alpine
WORKDIR /app
COPY . .
RUN go build -o server
EXPOSE 8080
CMD ["./server"]


Eu faço push da imagem no meu Docker Hub com:

davidl05/k8s-demo:v1

### ☸️ Kubernetes

Eu utilizo um cluster Kubernetes local, rodando em servidores Linux dentro da minha rede interna.
Esse cluster foi criado usando kind (Kubernetes in Docker), a ideia foi fazer um kluster minimo para validar conceitos.

🖥️ Nodes

Um node é um servidor (ou container, no caso do kind) que executa workloads do Kubernetes.

No meu ambiente atual, tenho:

1 node atuando como control-plane

Nenhum node dedicado como worker (o próprio control-plane também executa os pods de aplicação)

A saída real do comando:

kubectl get nodes

Mostra:

NAME                     STATUS   ROLES           AGE     VERSION
k8s-demo-control-plane   Ready    control-plane   5h14m   v1.30.0


Ou seja: tudo — API Server, Scheduler, Controller Manager e até minha aplicação — roda no mesmo nó.

### 📦 Pods

Aqui está a lista real dos pods que estão rodando no meu cluster:

kubectl get pods -A

NAMESPACE            NAME                                             READY   STATUS    RESTARTS        AGE

default              demo-deployment-66c55f56c7-6n882                 1/1     Running   0               4h42m

default              demo-deployment-66c55f56c7-f27hm                 1/1     Running   0               4h42m

default              demo-deployment-66c55f56c7-tcfb4                 1/1     Running   0               4h43m

ingress-nginx        ingress-nginx-controller-6775c6fd56-snwqn        1/1     Running   1 (4h55m ago)   5h13m

kube-system          coredns-7db6d8ff4d-2xf6s                         1/1     Running   1 (4h55m ago)   5h14m

kube-system          coredns-7db6d8ff4d-nkzsf                         1/1     Running   1 (4h55m ago)   5h14m

kube-system          etcd-k8s-demo-control-plane                      1/1     Running   1 (4h55m ago)   5h14m

kube-system          kindnet-b829w                                    1/1     Running   1 (4h55m ago)   5h14m

kube-system          kube-apiserver-k8s-demo-control-plane            1/1     Running   1 (4h55m ago)   5h14m

kube-system          kube-controller-manager-k8s-demo-control-plane   1/1     Running   1 (4h55m ago)   5h14m

kube-system          kube-proxy-wzxjk                                 1/1     Running   1 (4h55m ago)   5h14m

kube-system          kube-scheduler-k8s-demo-control-plane            1/1     Running   1 (4h55m ago)   5h14m

local-path-storage   local-path-provisioner-988d74bc-9q4p6            1/1     Running   2 (4h54m ago)   5h14m


Informações importantes:

✔ 3 réplicas da minha aplicação (demo-deployment)
✔ Ingress NGINX funcionando corretamente
✔ Componentes core do cluster (coredns, etcd, apiserver, etc) estão estáveis
✔ Armazenamento padrão do kind (local-path-storage)

### 📖 Manifests Kubernetes usados

A aplicação é descrita com manifestos YAML:

deployment.yaml

3 réplicas

imagem atualizada automaticamente pelo pipeline

estratégia rolling update

service.yaml

Service do tipo ClusterIP para a aplicação

ingress.yaml

expõe a aplicação usando o ingress-nginx

permite acessar via URL interna

### 🌐 Como ocorre o deploy

Eu faço um git push origin main

O GitHub dispara o workflow

O self-hosted runner pega o código

Faz build da imagem Docker

Envia para o Docker Hub

Usa kubectl set image para atualizar o Deployment

O Kubernetes inicia o update

As novas réplicas entram no ar sem downtime

### ✅ Resultado final

CI/CD real funcionando

Deploy automático no meu cluster Kubernetes local

Pipeline rodando via self-hosted runner

Atualização contínua da imagem Docker

update sem interrupção
