from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from user_agent import generate_user_agent
from math import ceil
from time import sleep
import datetime
import csv
from random import randint


def setup():
    userAgents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; ServiceUI 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/89.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux riscv64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
        ]
    # userAgent = generate_user_agent(device_type="desktop")

    options = Options()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={userAgents[randint(0, len(userAgents) - 1)]}')
    options.add_argument('--disable-gpu')
    options.add_argument('--lang=pt_BR')
    # prefs = {"download.default_directory":path}   #path is a string containing the directory you want the downloaded songs stored
    # options.add_experimental_option("prefs",prefs)
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-notifications")
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME,
        options=options)

    # driver = webdriver.Chrome(options = options)
    driver.delete_all_cookies()
    driver.set_window_size(1061, 701)

    try:
        driver.get("https://portal.cfm.org.br/busca-medicos/")
    except Exception as e:
        # raise e
        print(e)
        driver.quit()
        sleep(randint(2, 4))
    else:
        print(driver.execute_script("return navigator.userAgent"))
        sleep(randint(3, 7))

    aceitoCookies = wait(driver, '//*[@id="page"]/div[4]/div[2]/button')
    aceitoCookies.click()

    sleep(3)

    return driver;


def buscarPorCRM(driver, crm, uf):
    inputCRM = wait(driver, '//*[@id="buscaForm"]/div/div[1]/div[3]/div/input')
    inputCRM.send_keys(crm)
    sleep(randint(1, 3))
    dropdown = driver.find_element(By.ID, "uf")
    # dropdown.find_element(By.XPATH, "//option[. = 'MG']").click()
    wait(dropdown, "//option[. = '{}']".format(uf)).click()
    sleep(randint(1, 4))

    buscar = wait(driver, '//*[@id="buscaForm"]/div/div[4]/div[2]/button')
    buscar.click()

    sleep(randint(1, 4))

    result = driver.find_element(By.CLASS_NAME, "card-body")
    medico = retornaSituacaoCRM(result)
    return medico


def buscarVariosPorCRMs(driver, crms, uf):
    crms = ','.join(crms)
    inputCRM = wait(driver, '//*[@id="buscaForm"]/div/div[1]/div[3]/div/input')
    inputCRM.send_keys(crms)
    sleep(randint(3, 7))
    dropdown = driver.find_element(By.ID, "uf")
    # dropdown.find_element(By.XPATH, "//option[. = 'MG']").click()
    wait(dropdown, "//option[. = '{}']".format(uf)).click()
    sleep(randint(3, 5))

    buscar = wait(driver, '//*[@id="buscaForm"]/div/div[4]/div[2]/button')
    buscar.click()

    sleep(randint(4, 7))

    results = driver.find_elements(By.CLASS_NAME, "card-body")
    return results


def retornaSituacaoCRM(result):
    nome = result.find_element(By.TAG_NAME, 'h4').text
    crm = result.find_element(By.XPATH, './div[1]/div[1]').text.split(': ')[1].split('-')[0]
    situacao = result.find_element(By.XPATH, './div[2]/div[2]').text.split(': ')[1]
    especialidade = result.find_element(By.XPATH, './div[5]/div').text.replace('\n',' / ')
    data_hora_atualizacao = datetime.datetime.now().strftime("%d/%m/%Y %X")
    medico = dict(nome=nome, crm=crm, situacao=situacao,especialidade=especialidade,data_hora_atualizacao=data_hora_atualizacao)
    return medico


def wait(driver, x):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, x))
    )
    return element


# def retornaVariosResultados(results):
#   for i in results:
#     medico = i.find_element(By.TAG_NAME,'h4').text
#     crm = i.find_element(By.XPATH,'./div[1]/div[1]').text.split(': ')[1].split('-')[0]
#     situacao = i.find_element(By.XPATH,'./div[2]/div[2]').text.split(': ')[1]
#     print(medico + ';' + crm + ';' + situacao)


def retornaTotalRegistro():
    totalDeResultados = wait(driver, '//*[@id="resultados"]/div')
    total = int(totalDeResultados.text.split(' ')[0])
    print("Total de registros encontrados: " + str(total) + ' em ' + str(ceil(total / 10)) + ' páginas')

hoje = datetime.datetime.now().strftime("%Y%m%d")
groupedCRM = {}

with open('MEDICOS_CRM.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        crm = row['NUM_CONSELHO']
        uf = row['UF_CONSELHO']
        if uf not in groupedCRM.keys():
            groupedCRM[uf] = [crm]
        else:
            groupedCRM[uf].append(crm)

with open('medicosStatus_{}.csv'.format(hoje), 'w', newline='') as csvfilewriter:
    fields = ['nome', 'crm', 'uf', 'situacao','especialidade','data_hora_atualizacao']
    writer = csv.DictWriter(csvfilewriter, fieldnames=fields)
    writer.writeheader()

    for uf, crms in groupedCRM.items():
        while len(crms) > 0:
            listaAleatoria = [crms.pop() for i in range(randint(6,10)) if len(crms) > 0]

            resultsOK = True
            while resultsOK:
                driver = setup()
                print('{} - {}'.format(uf, listaAleatoria))
                try:
                    results = buscarVariosPorCRMs(driver, listaAleatoria, uf)
                except Exception as e:
                    # raise e
                    driver.quit()
                    print(e)
                    resultsOK = True
                    # medico = dict(nome=e)
                    # writer.writerow(medico)
                    # medicosStatus.append(medico)
                else:
                    if len(results) > 0:
                        for r in results:
                            medico = retornaSituacaoCRM(r)
                            medico['uf'] = uf
                            print(medico)
                            writer.writerow(medico)
                        # medicosStatus.append(medico)
                        driver.quit()
                        resultsOK = False
                    else:
                        driver.quit()
                        resultsOK = True
