from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Ruta para la página principal
@app.route('/')
def home():
    return "¡Bienvenido al Web Scraper! Ve a /scraper para obtener los datos."

# Ruta para el scraper
@app.route('/scraper', methods=['GET'])
def scraper():
    options = Options()
    # Desactivar headless para la depuración visual
    #options.add_argument('--headless=new')  # o '--headless=chrome' dependiendo de tu versión
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')  # Previene errores por memoria
    options.add_argument('--window-size=1920x1080')  # Simula una pantalla real
    options.add_argument('--start-maximized')        # Ayuda con JS que depende del tamaño
    

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://snies.mineducacion.gov.co/portal/ESTADISTICAS/Bases-consolidadas/")

    wait = WebDriverWait(driver, 30)  # Aumentado el tiempo de espera
    all_data = []

    try:
        while True:
            try:
                # Esperar la tabla completa
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
                    # Esperar recarga de la tabla
                    wait.until(EC.staleness_of(rows[0]))
                except Exception as e:
                    print("No hay más páginas o no se encontró el botón Siguiente.")
                    break
            except Exception as e:
                print("Ocurrió un error esperando la tabla.")
                print(driver.page_source[:1000])  # Imprime parte del HTML para ver qué cargó
                print(f"Error: {e}")
                break

    except Exception as general_error:
        print(f"Error general durante el scraping: {general_error}")
    finally:
        driver.quit()

    return jsonify(all_data)

if __name__ == '__main__':
    app.run(debug=True)
