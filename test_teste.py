from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestTeste():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_teste(self):
    self.driver.get("https://portal.cfm.org.br/busca-medicos/")
    self.driver.set_window_size(1061, 701)
    self.driver.find_element(By.ID, "uf").click()
    dropdown = self.driver.find_element(By.ID, "uf")
    dropdown.find_element(By.XPATH, "//option[. = 'MG']").click()
    self.driver.find_element(By.ID, "uf").click()
    self.driver.find_element(By.XPATH, "//*[@id=\"buscaForm\"]/div/div[4]/div[2]/button").click()
    results = self.driver.find_elements_by_class_name("busca-resultado")
    for i in results:
      print(i.text)
  

def wait(dr, x):
    element = WebDriverWait(dr, 5).until(
        EC.presence_of_element_located((By.XPATH, x))
    )
    return element



driver = webdriver.Chrome()
driver.get("https://portal.cfm.org.br/busca-medicos/")
driver.set_window_size(1061, 701)
# driver.find_element(By.ID, "uf").click()
dropdown = driver.find_element(By.ID, "uf")
dropdown.find_element(By.XPATH, "//option[. = 'MG']").click()
# driver.find_element(By.ID, "uf").click()
driver.find_element(By.XPATH,'//*[@id="page"]/div[4]/div[2]/button').click()
driver.find_element(By.XPATH, '//*[@id="buscaForm"]/div/div[4]/div[2]/button').click()
driver.implicitly_wait(10)
# wait(driver, '//*[@id="buscaForm"]/div/div[4]/div[2]/button').click()
results = driver.find_elements(By.CLASS_NAME,"card-body")
for i in results:
  medico = i.find_element(By.TAG_NAME,'h4')
  print(medico.text)

driver.quit()