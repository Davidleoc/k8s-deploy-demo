## Docker + Kubernetes + Self-Hosted Runner

Este projeto demonstra um pipeline completo de CI/CD usando GitHub Actions, Docker Hub e Kubernetes, com foco em ambientes de rede interna.

 ### O fluxo automatiza:

Build da imagem Docker

Push para o Docker Hub

Atualização automática do Deployment no Kubernetes

Uso de um GitHub Runner hospedado dentro da rede local

### ✅ Solução: Self-Hosted Runner

Para permitir que o pipeline acesse o cluster, configuramos um Self-Hosted GitHub Runner dentro do mesmo servidor que executa o Kubernetes.
Assim, ele consegue:

✔ Executar kubectl localmente
✔ Fazer o build da imagem
✔ Enviar para o Docker Hub
✔ Atualizar o Deployment no cluster
