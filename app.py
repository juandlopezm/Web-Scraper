from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route('/scraper', methods=['GET'])
def scraper():
    options = Options()
    # options.add_argument('--headless')  # Desactivado para depuración visual
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://snies.mineducacion.gov.co/portal/ESTADISTICAS/Bases-consolidadas/")

    wait = WebDriverWait(driver, 30)  # Aumentado el tiempo de espera
    all_data = []

    while True:
        try:
            # Esperar la tabla completa, no solo las filas
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'table')))

            rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')
            print(f"Filas encontradas: {len(rows)}")

            for row in rows:
                try:
                    year = row.find_element(By.CSS_SELECTOR, 'td:nth-child(1)').text
                    link_element = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2) a')
                    link = link_element.get_attribute('href')
                    text = row.find_element(By.CSS_SELECTOR, 'td:nth-child(2)').text
                    all_data.append({'year': year, 'title': text, 'link': link})
                except Exception as e:
                    print(f"Error al procesar una fila: {e}")
            
            # Buscar botón "Siguiente"
            try:
                next_button = driver.find_element(By.LINK_TEXT, 'Siguiente')
                if 'disabled' in next_button.get_attribute('class'):
                    break
                next_button.click()
                wait.until(EC.staleness_of(rows[0]))  # Esperar recarga de la tabla
            except Exception as e:
                print("No hay más páginas o no se encontró el botón Siguiente.")
                break

        except Exception as e:
            print("Ocurrió un error esperando la tabla.")
            print(driver.page_source[:1000])  # Imprime parte del HTML para ver qué cargó
            print(f"Error: {e}")
            break

    driver.quit()
    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)
