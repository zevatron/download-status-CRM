from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from user_agent import generate_user_agent
from math import ceil
from time import sleep
import csv
from random import randint

# class TestTeste():
#   def setup_method(self, method):
#     self.driver = webdriver.Chrome()
#     self.vars = {}
  
#   def teardown_method(self, method):
#     self.driver.quit()
  
#   def test_teste(self):
#     self.driver.get("https://portal.cfm.org.br/busca-medicos/")
#     self.driver.set_window_size(1061, 701)
#     self.driver.find_element(By.ID, "uf").click()
#     dropdown = self.driver.find_element(By.ID, "uf")
#     dropdown.find_element(By.XPATH, "//option[. = 'MG']").click()
#     self.driver.find_element(By.ID, "uf").click()
#     self.driver.find_element(By.XPATH, "//*[@id=\"buscaForm\"]/div/div[4]/div[2]/button").click()
#     results = self.driver.find_elements_by_class_name("busca-resultado")
#     for i in results:
#       print(i.text)

def setup():
  userAgent = generate_user_agent()

  options = Options()
  options.add_argument('--headless')
  options.add_argument(f'user-agent={userAgent}')
  options.add_argument('--disable-gpu')
  options.add_argument('--lang=pt_BR')
  # prefs = {"download.default_directory":path}   #path is a string containing the directory you want the downloaded songs stored
  # options.add_experimental_option("prefs",prefs)
  options.add_argument('--no-sandbox')
  options.add_argument("--disable-notifications")
  options.add_argument('--disable-dev-shm-usage')
  
  driver = webdriver.Chrome(options = options)
  driver.delete_all_cookies()
  driver.set_window_size(1061, 701)

  try:
    driver.get("https://portal.cfm.org.br/busca-medicos/")
  except Exception as e:
    # raise e
    print(e)
    driver.quit()
    driver.get("https://portal.cfm.org.br/busca-medicos/")
    sleep(randint(2,4))
  else:
    sleep(3)   

  

  aceitoCookies = wait(driver,'//*[@id="page"]/div[4]/div[2]/button')
  aceitoCookies.click()

  return driver;

def buscarPorCRM(driver,crm,uf):
  inputCRM = wait(driver,'//*[@id="buscaForm"]/div/div[1]/div[3]/div/input')
  inputCRM.send_keys(crm) 
  sleep(randint(1,3))
  dropdown = driver.find_element(By.ID, "uf")
  # dropdown.find_element(By.XPATH, "//option[. = 'MG']").click()
  wait(dropdown,"//option[. = '{}']".format(uf)).click()
  sleep(randint(1,4))
  
  buscar = wait(driver,'//*[@id="buscaForm"]/div/div[4]/div[2]/button')
  buscar.click()
  
  sleep(randint(1,4))
  
  result = driver.find_element(By.CLASS_NAME,"card-body")
  medico = retornaStatusCRM(result)
  return medico


def retornaStatusCRM(result):
  nome = result.find_element(By.TAG_NAME,'h4').text
  crm = result.find_element(By.XPATH,'./div[1]/div[1]').text.split(': ')[1].split('-')[0]
  situacao = result.find_element(By.XPATH,'./div[2]/div[2]').text.split(': ')[1]
  medico = dict(nome = nome, crm = crm, situacao = situacao)
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
  totalDeResultados = wait(driver,'//*[@id="resultados"]/div')
  total = int(totalDeResultados.text.split(' ')[0])
  print("Total de registros encontrados: " + str(total) + ' em ' + str(ceil(total/10)) + ' páginas')







# medicosStatus = []

with open('medicosStatus.csv','w',newline='') as csvfilewriter:
  fields = ['nome','crm','uf','situacao']
  writer = csv.DictWriter(csvfilewriter,fieldnames = fields)
  writer.writeheader()

  # for m in medicosStatus:
  #   writer.writerow(m)


  with open('MEDICOS_CRM.csv',newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
      crm = row['NUM_CONSELHO']
      uf = row['UF_CONSELHO']

      print(row)

      driver = setup()

      try:
        medico = buscarPorCRM(driver,crm,uf)
      except Exception as e:
        # raise e
        driver.quit()
        print(e)
        # medico = dict(nome=e)
        # writer.writerow(medico)
        # medicosStatus.append(medico)
      else:
        medico['nome'] = row['NOME']
        medico['uf'] = row['UF_CONSELHO']
        writer.writerow(medico)
        # medicosStatus.append(medico)
        driver.quit()
         