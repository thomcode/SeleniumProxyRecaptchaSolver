import logging
import os
import time
import random
import json
import asyncio
import aiohttp
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuração do logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

proxy_list_url = "https://sunny9577.github.io/proxy-scraper/proxies.json"
proxy_file = "functional_proxies.json"
proxy_expiry_days = 30

# Função para obter a lista de proxies do Brasil
async def get_proxies():
    async with aiohttp.ClientSession() as session:
        async with session.get(proxy_list_url) as response:
            if response.status == 200:
                proxies = await response.json()
                brazil_proxies = [proxy for proxy in proxies if proxy.get('country') and 'Brazil' in proxy['country']]
                return brazil_proxies
            else:
                print("Falha ao obter a lista de proxies")
                return []

# Função para verificar se o proxy está funcionando em múltiplos sites
async def is_proxy_working(proxy):
    sites = ["https://app.hugme.com.br", "https://www.nopecha.com", "https://api.nopecha.com", "ttps://developers.nopecha.com"]
    proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
    async with aiohttp.ClientSession() as session:
        for site in sites:
            try:
                logger.info(f"Testando proxy {proxy_url} no site {site}")
                async with session.get(site, proxy=proxy_url, timeout=3, headers={'User-Agent': 'Mozilla/5.0'}) as response:
                    if response.status != 200:
                        logger.info(f"Proxy {proxy_url} falhou no site {site}")
                        return False
            except Exception as e:
                logger.error(f"Erro ao testar o proxy {proxy_url} no site {site}: {e}")
                return False
    logger.info(f"Proxy {proxy_url} aprovado!")
    return True

# Função para testar todos os proxies e guardar os funcionais
async def test_all_proxies():
    proxies = await get_proxies()
    if not proxies:
        raise Exception("Nenhum proxy disponível do Brasil")

    tasks = [is_proxy_working(proxy) for proxy in proxies]
    results = await asyncio.gather(*tasks)

    functional_proxies = [proxy for proxy, result in zip(proxies, results) if result]

    if not functional_proxies:
        raise Exception("Nenhum proxy funcional encontrado")

    save_proxies_to_file(functional_proxies)
    return functional_proxies

# Função para salvar proxies em um arquivo
def save_proxies_to_file(proxies):
    data = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "proxies": proxies
    }
    with open(proxy_file, 'w') as f:
        json.dump(data, f)
    logger.info(f"Proxies funcionais salvos em {proxy_file}")

# Função para carregar proxies de um arquivo
def load_proxies_from_file():
    if not os.path.exists(proxy_file):
        return None

    with open(proxy_file, 'r') as f:
        data = json.load(f)

    file_date = datetime.strptime(data["date"], "%Y-%m-%d")
    if datetime.now() - file_date > timedelta(days=proxy_expiry_days):
        return None

    return data["proxies"]

class WebDriverHandler:
    def __init__(self):
        proxies = load_proxies_from_file()
        if not proxies:
            proxies = asyncio.run(test_all_proxies())
        self.proxies = proxies
        self.driver = self.initialize_driver()

    def initialize_driver(self):
        if not self.proxies:
            raise Exception("Nenhum proxy funcional disponível")

        # Escolher um proxy funcional aleatoriamente
        chosen_proxy = random.choice(self.proxies)

        # Configura o ChromeDriver usando webdriver-manager
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  # Inicia o navegador maximizado

        # Caminho para a extensão do RecaptchaSolver
        extension_resolver = fr"{os.getcwd()}\RecaptchaSolver"
        options.add_argument(f'--load-extension={extension_resolver}')  # Carrega a extensão do RecaptchaSolver

        # Adiciona o proxy
        options.add_argument(f'--proxy-server=http://{chosen_proxy["ip"]}:{chosen_proxy["port"]}')

        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()  # Garante que o driver seja encerrado corretamente

    def login(self, url, username, password):
        try:
            # Acessa a página de login e realiza o login com usuário e senha
            logger.info("Acessando a página de login")
            self.driver.get(url)
            time.sleep(2)
            logger.info("Inserindo o nome de usuário")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "vo.email"))
            ).send_keys(username)
            time.sleep(2)
            logger.info("Clicando no botão de verificação")
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "verify-sso-button"))
            ).click()
            time.sleep(2)
            logger.info("Inserindo a senha")
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "vo.senha"))
            ).send_keys(password)
            time.sleep(2)

            # Aguarda até que o reCAPTCHA seja resolvido
            logger.info("Aguardando resolução do reCAPTCHA")
            time.sleep(10)
            self.wait_for_recaptcha_solution()
        except Exception as e:
            logger.error(f"Erro ao tentar realizar o login: {e}")
        finally:
            self.quit_driver()

    def wait_for_recaptcha_solution(self):
        solved = False
        attempts = 0
        while not solved and attempts < 5:
            time.sleep(30)
            WebDriverWait(self.driver, 5)
            solved = self.isSolved()
            attempts += 1
        if solved:
            logger.info("reCAPTCHA resolvido")
        else:
            logger.error("Falha ao resolver o reCAPTCHA após 5 tentativas.")

    def isSolved(self):
        try:
            self.driver.switch_to.default_content()
            time.sleep(10)
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, 'iframe[title="reCAPTCHA"]'))
            )
            recaptcha_checkmark = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'recaptcha-checkbox-checkmark'))
            )
            return "style" in recaptcha_checkmark.get_attribute('outerHTML')
        except Exception as e:
            logger.error(f"Exception during CAPTCHA check: {e}")
            return False


