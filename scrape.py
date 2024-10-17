import requests
from bs4 import BeautifulSoup
import os

url = "https://arcomoratalaz.com/cursos-de-iniciacion/"

def send_telegram_message(text):
    
    url = f"https://api.telegram.org/bot{os.environ.get('TOKEN')}/sendMessage"
    payload = {
        'chat_id': os.environ.get('CHAT_ID'),
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, data=payload)
    return response.json


def scrape_data():
    default_string = ' En estos momentos no hay fechas disponibles'
    try:
        response = requests.get(url, timeout=60)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        content = soup.find_all(string=default_string)

        if not content:
            caption = "HAY FECHA ABIERTAS PARA CURSO DE TIRO CON ARCO"
            send_telegram_message(text=caption)

    # Handle exceptions and pause before retrying
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    scrape_data()