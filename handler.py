import json

import pandas
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def _get_data_from_wiki(article: str):
    url = f'https://en.wikipedia.org/w/index.php?title={article}&action=history'
    response = requests.get(url)

    parsed_html = BeautifulSoup(response.text, features="html.parser")
    dates = parsed_html.body.find_all('a', attrs={'class': 'mw-changeslist-date'})
    last_month = (datetime.today().replace(day=1) - timedelta(days=1)).month
    last_updates = []
    for i in dates:
        last_updates.append(datetime.strptime(i.text, '%H:%M, %d %B %Y'))

    last_month_updates = list(filter(lambda x: x.month == last_month, last_updates))

    if last_month_updates:

        result = {
            "article": article,
            "latest_update_time": last_month_updates[0].isoformat(),
            "number_updates_last_month": len(last_month_updates)
        }
    else:
        result = {
            "article": article,
            "latest_update_time": None,
            "number_updates_last_month": 0
        }
    return result


def lambda_handler(event, context):

    articles = event['articles']
    updates_info = [_get_data_from_wiki(article) for article in articles]

    with open('result.json', 'w') as file:
        json.dump(updates_info, file)

    json_file = pandas.read_json('result.json')
    filtered_dataset = json_file.drop(json_file.query('number_updates_last_month < 2').index)  # I've changed this one cause  don't see any purpose of riding with updates > 2
    sum_of_updates = filtered_dataset['number_updates_last_month'].sum()
    mean_of_updates = filtered_dataset['number_updates_last_month'].mean()
    result_dataframe = pandas.DataFrame.from_dict({'sum_of_updates': sum_of_updates,
                                                   'mean_of_updates': mean_of_updates}, orient='index')
    result_dataframe.to_json('pandas_output.json')
