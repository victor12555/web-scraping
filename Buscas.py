# criar um navegador
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
class Buscas:
    def __init__(self, produto, termos_banidos, preco_minimo, preco_maximo):
        self.produto = produto
        self.termos_banidos = termos_banidos
        self.preco_minimo = preco_minimo
        self.preco_maximo = preco_maximo
        self.lista_ofertas_google = []
        self.lista_ofertas_buscape = []


    def busca_google_shopping(self):
        # Entrando no google
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")

        # tratar os valores que vieram da tabela
        produto = self.produto.lower()
        termos_banidos = self.termos_banidos.lower()
        lista_termos_banidos = self.termos_banidos.split(" ")
        lista_termos_produto = self.produto.split(" ")
        preco_minimo = float(self.preco_minimo)
        preco_maximo = float(self.preco_maximo)
        # pesquisar o nome do  no google
        driver.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys(produto)
        driver.find_element(By.XPATH, '//*[@id="APjFqb"]').send_keys(Keys.ENTER)

        # clicar na aba shopping
        time.sleep(5)
        driver.find_element(By.XPATH, '//*[@id="cnt"]/div[5]/div/div/div[1]/div[1]/div/a[1]').click()

        # pegar a lista de resultados da busca no google shopping
        time.sleep(1)
        driver.execute_script(f"window.scroll(0, 1350);")
        time.sleep(1)
        lista_resultados = driver.find_elements(By.CLASS_NAME, 'sh-dgr__gr-auto')

        # para cada resultado, ele vai verificar se o resultado corresponde a todas as nossas condicoes
        lista_ofertas = []  # lista que a função vai me dar como resposta
        for resultado in lista_resultados:
            nome = resultado.find_element(By.CLASS_NAME, 'tAxDx').text
            nome = nome.lower()
            # verificacao do nome - se no nome tem algum termo banido
            tem_termos_banidos = False
            for palavra in lista_termos_banidos:
                if palavra in nome:
                    tem_termos_banidos = True
            # verificar se no nome tem todos os termos do nome do 
            tem_todos_termos_produto = True
            for palavra in lista_termos_produto:
                if palavra not in nome:
                    tem_todos_termos_produto = False

            if not tem_termos_banidos and tem_todos_termos_produto:  # verificando o nome
                try:
                    preco = resultado.find_element(By.CLASS_NAME, 'a8Pemb').text
                    preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                    if preco == ' ':
                        pass
                    else:
                        preco = float(preco)
                    # verificando se o preco ta dentro do minimo e maximo
                    if preco_minimo <= preco <= preco_maximo:
                        elemento_link = resultado.find_element(By.CLASS_NAME, 'aULzUe')
                        elemento_pai = elemento_link.find_element(By.XPATH, '..')
                        link = elemento_pai.get_attribute('href')
                        lista_ofertas.append((nome, preco, link))
                        self.lista_ofertas_google.append((nome, preco, link))
                except:
                    continue
        for i in lista_ofertas:
            print(f'{i}\n')


    def Busca_Google_Excel(self,nome='GoogleOfertas',show=False):
        if not self.lista_ofertas_google:
            print('Nenhuma oferta foi encontrada,tente novamente.')
        elif show == True:
            tabela_google_shopping = pd.DataFrame(self.lista_ofertas_google, columns=['produto', 'preco', 'link'])
            tabela_google_shopping.to_excel(f'{nome}.xlsx',index=False)
            print('Tabela de produtos do google shopping criada e exportada para o excel com sucesso!!!')
            print(tabela_google_shopping)
        else:
            tabela_google_shopping = pd.DataFrame(self.lista_ofertas_google, columns=['produto', 'preco', 'link'])
            tabela_google_shopping.to_excel(f'{nome}.xlsx',index=False)
            print('Tabela de produtos do google shopping criada criada e exportada para o excel com sucesso!!!')


    def busca_buscape(self):
        # tratar os valores da função
        preco_maximo = float(self.preco_maximo)
        preco_minimo = float(self.preco_minimo)
        produto = self.produto.lower()
        termos_banidos = self.termos_banidos.lower()
        lista_termos_banidos = termos_banidos.split(" ")
        lista_termos_produto = self.produto.split(" ")

        # entrar no buscape
        driver = webdriver.Chrome()
        driver.get("https://www.buscape.com.br/")

        # pesquisar pelo  no buscape
        driver.find_element(By.CLASS_NAME, 'AutoCompleteStyle_input__HG105').send_keys(produto, Keys.ENTER)

        # pegar a lista de resultados da busca do buscape
        time.sleep(5)
        driver.execute_script(f"window.scroll(0, 1350);")
        time.sleep(1)
        lista_resultados = driver.find_elements(By.CLASS_NAME, 'Paper_Paper__HIHv0')

        # para cada resultado
        lista_ofertas = []
        for resultado in lista_resultados:
            try:
                preco = resultado.find_element(By.CLASS_NAME, 'Text_MobileHeadingS__Zxam2').text
                nome = resultado.find_element(By.CLASS_NAME, 'SearchCard_ProductCard_NameWrapper__Gv0x_').text
                nome = nome.lower()
                elemento_link = resultado.find_element(By.CLASS_NAME, 'SearchCard_ProductCard_SuperiorTags__Ua2qE')
                elemento_pai = elemento_link.find_element(By.XPATH, '..')
                link = elemento_pai.get_attribute('href')

                # verificacao do nome - se no nome tem algum termo banido
                tem_termos_banidos = False
                for palavra in lista_termos_banidos:
                    if palavra in nome:
                        tem_termos_banidos = True

                        # verificar se no nome tem todos os termos do nome do 
                tem_todos_termos_produto = True
                for palavra in lista_termos_produto:
                    if palavra not in nome:
                        tem_todos_termos_produto = False

                if not tem_termos_banidos and tem_todos_termos_produto:
                    preco = preco.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
                    preco = float(preco)
                    if preco_minimo <= preco <= preco_maximo:
                        lista_ofertas.append((nome, preco, link))
                        self.lista_ofertas_buscape.append((nome, preco, link))
            except:
                continue
        for i in lista_ofertas:
            print(f'{i}\n')

    def Buscape_Excel(self,nome='BuscapeOfertas',show=False):
        if not self.lista_ofertas_buscape:
            print('Nenhuma oferta foi encontrada,tente novamente.')
        elif show == True:
            tabela_buscape = pd.DataFrame(self.lista_ofertas_buscape, columns=['produto', 'preco', 'link'])
            tabela_buscape.to_excel(f'{nome}.xlsx',index=False)
            print('Tabela de produtos do Buscapé criada e exportada para o excel com sucesso!!!')
            print(tabela_buscape)
        else:
            tabela_google_shopping = pd.DataFrame(self.lista_ofertas_google, columns=['produto', 'preco', 'link'])
            tabela_google_shopping.to_excel(f'{nome}.xlsx',index=False)
            print('Tabela de produtos do Buscapé criada e exportada para o excel com sucesso!!!')

