from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Academico:

    def __init__(self, login=None, password=None):
        self.driver = webdriver.Chrome()
        self.logged = False
        self.login = login
        self.password = password
    
    def __del__(self):
        self.driver.close()

    def acad_login(self):
        self.driver.get("https://academico.iff.edu.br/qacademico/index.asp?t=1001")

        login_field = self.driver.find_element_by_name('LOGIN')
        login_field.send_keys(self.login)

        password_field = self.driver.find_element_by_name('SENHA')
        password_field.send_keys(self.password)

        password_field.send_keys(Keys.RETURN)

        self.logged = True

    def parse_diario_name(self, table_row):
        try:
            info = table_row.find_element_by_tag_name('strong')
            return info.get_attribute('innerHTML')
        except:
            pass

    def parse_diario_description(self, table_row):
        data = table_row.find_elements_by_tag_name('tr')
        description = []
        keys = ['', 'info', 'peso', 'nota']

        for i in range(len(data)):
            description.append({})
            dump = data[i].find_elements_by_tag_name('td')
            for j in range(1, 4):
                description[i][keys[j]] = ' '.join(dump[j].get_attribute('innerHTML').split())
        
        return description

    def parse_diario_info(self, info_row, description_row):
        resource = {}
        name = self.parse_diario_name(info_row)
        tmp = name.split('-')
        tmp = [x.strip() for x in tmp]

        resource['cod']         = tmp[0]
        resource['turma']       = tmp[1]
        resource['materia']     = tmp[2]
        resource['professor']   = tmp[3]

        if description_row: 
            description = self.parse_diario_description(description_row)
            resource['description'] = description
        
        return resource

    def parse_diario(self):
        if not self.logged:
            self.acad_login()

        self.driver.get("https://academico.iff.edu.br/qacademico/index.asp?t=2071")

        path = '/html/body/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/table[2]/tbody/tr/td[2]/p/table[2]/tbody/tr'
        rows  = self.driver.find_elements_by_xpath(path)
        diario_description = {}

        for i in range(len(rows)):
            if rows[i].get_attribute('class') in ['rotulo', 'conteudoTexto']:
                continue
            
            try:
                if rows[i + 1].get_attribute('class') == 'conteudoTexto':
                    diario_description[rows[i]] = rows[i + 1]
                else:
                    diario_description[rows[i]] = None
            except:
                continue
        
        resource = []
        for k in diario_description:
            resource.append(
                self.parse_diario_info(k, diario_description[k])
            )
        return resource