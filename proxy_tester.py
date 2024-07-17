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