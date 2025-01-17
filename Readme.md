# Teste de Proxy e Gerenciador de WebDriver

[![Licença: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

Bem-vindo ao repositório de Teste de Proxy e Gerenciador de WebDriver! Este projeto ajuda você a:
- Testar múltiplos proxies para verificar sua funcionalidade
- Salvar proxies funcionais para uso futuro
- Utilizar o Selenium WebDriver com proxies funcionais para automação web

## 🚀 Funcionalidades
- **Teste de Proxy**: Testa uma lista de proxies para encontrar os funcionais.
- **Salvar Proxies Funcionais**: Salva os proxies funcionais em um arquivo para uso futuro.
- **Reutilizar Proxies**: Carrega proxies funcionais do arquivo para evitar testes repetidos.
- **WebDriver com Proxy**: Utiliza Selenium WebDriver com os proxies funcionais para tarefas automatizadas.
- **Manipulação de CAPTCHA**: Manipula reCAPTCHA usando Selenium WebDriver.

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- Google Chrome

### Instalar Dependências
```bash
pip install -r requirements.txt
```

## 📋 Uso


### 1. Exemplo Completo
Aqui está um exemplo completo que testa proxies, salva os funcionais e utiliza Selenium WebDriver para login:
```python
import asyncio
import logging
from webdriver_handler import WebDriverHandler

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():

    # Inicializar WebDriver e realizar login
    handler = WebDriverHandler()
    handler.login("https://app.hugme.com.br/", "usuario", "senha")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📁 Estrutura de Arquivos
```bash
.
├── proxy_tester.py          # Script para testar e salvar proxies funcionais
├── webdriver_handler.py     # Script para inicializar WebDriver com proxies funcionais e realizar login
├── functional_proxies.json  # Arquivo para armazenar proxies funcionais
├── README.md                # Este arquivo README
```

## 📜 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuindo
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/feature-incrivel`)
3. Commit suas alterações (`git commit -m 'Adiciona uma feature incrível'`)
4. Push para a branch (`git push origin feature/feature-incrivel`)
5. Abra um Pull Request

## 📧 Contato
Se você tiver alguma dúvida, sinta-se à vontade para entrar em contato:
- Email: [simeaothomas@gmail.com](mailto:simeaothomas@gmail.com)
- GitHub: [thomcode](https://github.com/thomcode)

---

Aproveite para testar seus proxies e automatizar tarefas com Selenium WebDriver! 🎉🚀
