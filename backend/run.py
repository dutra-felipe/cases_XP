from app import create_app


app = create_app()

if __name__ == '__main__':
    # Esta linha inicia o servidor e o faz escutar em todas as interfaces de rede
    # o que é necessário para o Docker
    app.run(host='0.0.0.0', port=5000)