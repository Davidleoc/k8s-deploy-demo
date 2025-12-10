# Código da aplicação exemplo
package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        msg := os.Getenv("WELCOME_MSG")
        if msg == "" {
            msg = "Mensagem padrão: variável não encontrada"
        }
        fmt.Fprintf(w, "Mensagem: %s", msg)
    })

    log.Println("Servidor rodando na porta 8080...")
    http.ListenAndServe(":8080", nil)
}
