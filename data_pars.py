import requests
import pandas as pd
from datetime import datetime, timedelta
from bs4 import BeautifulSoup


def get_usd_rate_history(days=180):
    date_end = datetime.now()
    date_start = date_end - timedelta(days=days)
    date_start_str = date_start.strftime('%Y-%m-%d')
    date_end_str = date_end.strftime('%Y-%m-%d')
    url = f"https://cbr.ru/scripts/XML_dynamic.asp"
    params = {
        "date_req1": date_start.strftime('%d/%m/%Y'),
        "date_req2": date_end.strftime('%d/%m/%Y'),
        "VAL_NM_RQ": "R01235"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"API ЦБ вернул ошибку: {response.status_code}")
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.content)
    records = []
    for record in root.findall('Record'):
        date_str = record.get('Date')
        nominal = float(record.find('Nominal').text.replace(',', '.'))
        value = float(record.find('Value').text.replace(',', '.'))
        records.append({
            'date': pd.to_datetime(date_str, format='%d.%m.%Y'),
            'nominal': nominal,
            'rate': value / nominal  # Курс за 1 доллар (ЦБ даёт за номинал, обычно 1)
        })
    df = pd.DataFrame(records)
    df = df.sort_values('date').reset_index(drop=True)
    return df[['date', 'rate']]


def get_key_rate_history(days=365):
    date_end = datetime.now()
    date_start = date_end - timedelta(days=days)
    url = "https://www.cbr.ru/hd_base/KeyRate/"
    params = {
        "UniDbQuery.Posted": "True",
        "UniDbQuery.From": date_start.strftime('%d.%m.%Y'),
        "UniDbQuery.To": date_end.strftime('%d.%m.%Y')
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Ошибка доступа: {response.status_code}")
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='data')
    if not table:
        raise Exception("Таблица с данными не найдена")
    dates, rates = [], []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 2:
            try:
                date_obj = datetime.strptime(cols[0].text.strip(), '%d.%m.%Y')
                rate_val = float(cols[1].text.strip().replace(',', '.'))
                dates.append(date_obj)
                rates.append(rate_val)
            except (ValueError, IndexError):
                continue
    df = pd.DataFrame({'date': dates, 'rate': rates})
    return df.sort_values('date').reset_index(drop=True)
