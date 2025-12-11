## Docker + Kubernetes + Self-Hosted Runner

Este projeto demonstra um pipeline completo de CI/CD usando GitHub Actions, Docker Hub e Kubernetes, com foco em ambientes de rede interna. Para a demonstração foi usado um projeto simples em Go (feito por IA)

 ### O objetivo principal é automatizar todo o fluxo:

Fazer build da aplicação

Criar a imagem Docker

Publicar a imagem no Docker Hub

Atualizar o Deployment no Kubernetes automaticamente

#### ✅ Solução: Self-Hosted Runner

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

#### A estrutura está assim:

k8s-deploy-demo/
│
├── app/
│   ├── main.go
│   └── Dockerfile
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
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

O Deployment faz o deploy da imagem e expõe um Pod com 8080:

containers:
  - name: k8s-demo
    image: davidl05/k8s-demo:v1
    ports:
      - containerPort: 8080


Tenho também um Service para expor o Deployment internamente.
        
