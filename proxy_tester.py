from webdriver_handler import WebDriverHandler

def main():
    # Orquestra o fluxo de execução do script
    handler = WebDriverHandler()
    # Teste usando o hugme
    handler.login("https://app.hugme.com.br/","usuario", "senha")

if __name__ == "__main__":
    main()