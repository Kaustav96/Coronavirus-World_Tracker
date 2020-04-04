import requests
import pandas
from csv import writer
from bs4 import BeautifulSoup
import json
import logging
import schedule
import time
from datetime import datetime
from slack_client import slacker
from slack_client import slacker_file
from telegram_client import send_notification
from tabulate import tabulate

SHORT_HEADERS = ['Total Cases', 'Total Deaths', 'Total Recovered']
SHORT_HEADERS_Country = ['Country', 'Total Cases', 'total Deaths', 'Total Recovered', 'Active Cases', 'Serious Cases']
FORMAT = '[%(asctime)-15s] %(message)s'
NEW_FILE_NAME = 'corona_world_data.json'
NEW_FILE_NAME_COUNTRY = 'corona_country_data.json'
logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename='bot.log', filemode='a')
current_time = datetime.now().strftime('%d/%m/%Y %H:%M')


def save_json(x):
    with open(NEW_FILE_NAME, 'w+') as f:
        if len(f.read()) == 0:
            f.write(json.dumps(x))
        else:
            f.write(',\n' + json.dumps(x))


def save_json_country(x):
    with open(NEW_FILE_NAME_COUNTRY, 'w+') as f:
        if len(f.read()) == 0:
            f.write(json.dumps(x))
        else:
            f.write(',\n' + json.dumps(x))


def load():
    with open(NEW_FILE_NAME, 'r') as f:
        res = json.load(f)
    return res


def load_country():
    with open(NEW_FILE_NAME_COUNTRY, 'r') as f:
        res = json.load(f)
    return res


try:
    def main_work():
        info = []
        res_main = requests.get('https://www.worldometers.info/coronavirus/#countries')
        res_country = requests.get('https://www.worldometers.info/coronavirus/#countries')
        soup_main = BeautifulSoup(res_main.text, 'html.parser')
        soup_country = BeautifulSoup(res_country.text, 'html.parser')
        stats_main = []
        stats_country = []
        try:
            my_data_str = ''
            my_data_country = ''
            for tr in soup_country.find_all('tbody')[0].find_all('tr'):
                my_data_country += tr.get_text()
            last_data_updated = soup_main.find_all('div')[13].get_text()
            for tr in soup_main.find_all('h1'):
                my_data_str += tr.get_text()
            headers = my_data_str.split(':')[0:3]
            total_cases_span = ''
            total_death_span = ''
            total_recovered_span = ''
            for span in soup_main.find_all('span')[4:5]:
                total_cases_span += span.get_text()
            for span in soup_main.find_all('span')[5:6]:
                total_death_span += span.get_text()
            for span in soup_main.find_all('span')[6:7]:
                total_recovered_span += span.get_text()

            stats_main.append([total_cases_span, total_death_span, total_recovered_span])
            data = [
                {'Cornavirus Cases': total_cases_span, 'Deaths': total_death_span, 'Recovered': total_recovered_span}]
            past_data = load()
            data_set = my_data_country.split('\n')
            count_items = 0

            # Overview
            # for item in past_data:
            #     past_case, past_death, past_recover = item['Cornavirus Cases'], item['Deaths'], item['Recovered']
            #
            #     cur_case, cur_death, cur_recover = stats_main[0][0], stats_main[0][1], stats_main[0][2]
            #     past_str, cur_str = '', ''
            #     if past_case != cur_case:
            #         past_str += 'Total->' + str(past_case) + ','
            #         cur_str += 'Total->' + str(cur_case) + ','
            #     if past_death != cur_death:
            #         past_str += 'Deaths->' + str(past_death) + ','
            #         cur_str += 'Deaths->' + str(cur_death) + ','
            #     if past_recover != cur_recover:
            #         past_str += 'Recovered->' + str(past_recover)
            #         cur_str += 'Recovered->' + str(cur_recover)
            #     if len(past_str) > 0 and len(cur_str) > 0:
            #         info.append(f'Changes are : [{past_str}]->[{cur_str}]')
            # country data
            # print(len(data_set))
            new_dict = {'Country Name': [], 'Total Cases': [], 'Total Death': [], 'Total Recovered': [],
                        'Total Active Cases': [], 'Total Serious Cases': []}
            df = pandas.DataFrame(new_dict)

            df.to_csv('corona_country_data.csv')

            while count_items <= len(data_set) - 13:
                country_name = data_set[count_items: count_items + 13][1]
                country_total_cases = data_set[count_items: count_items + 13][2]
                country_total_death = data_set[count_items: count_items + 13][4]
                country_total_recovered = data_set[count_items: count_items + 13][6]
                country_total_active = data_set[count_items: count_items + 13][7]
                country_total_serious = data_set[count_items: count_items + 13][8]
                list_of_country = [country_name, country_total_cases, country_total_death, country_total_recovered,
                                   country_total_active, country_total_serious]
                with open('corona_country_data.csv', 'a+', newline='') as f:
                    csv_writer = writer(f)
                    csv_writer.writerow(list_of_country)

                stats_country.append(
                    [country_name, country_total_cases, country_total_death, country_total_recovered,
                     country_total_active, country_total_serious])
                count_items += 13

            past_data_country = load_country()
            cur_country = [(x[0]) for x in stats_country[0:len(stats_country)]]
            past_country = [(x[0]) for x in past_data_country[0:len(past_data_country)]]
            count_country, count_past_country = 0, 0
            for country in cur_country:
                if country not in past_country:
                    cur_total, cur_death, cur_recover, cur_active, cur_serious = stats_country[count_country][1], \
                                                                                 stats_country[count_country][2], \
                                                                                 stats_country[count_country][3], \
                                                                                 stats_country[count_country][4], \
                                                                                 stats_country[count_country][5]
                    cur_str = 'Total->' + str(cur_total) + ', Deaths->' + str(cur_death) + ', Recover->' + str(
                        cur_recover) + ', Active->' + str(cur_active) + ', Serious->' + str(cur_serious)
                    info.append(f'NEW COUNTRY - {country} got corona virus.{[cur_str]}')
                    count_country += 1
                else:

                    past_total, past_death, past_recover, past_active, past_serious = \
                        past_data_country[count_past_country][1], past_data_country[count_past_country][2], \
                        past_data_country[count_past_country][3], past_data_country[count_past_country][4], \
                        past_data_country[count_past_country][5]

                    cur_total, cur_death, cur_recover, cur_active, cur_serious = stats_country[count_country][1], \
                                                                                 stats_country[count_country][2], \
                                                                                 stats_country[count_country][3], \
                                                                                 stats_country[count_country][4], \
                                                                                 stats_country[count_country][5]
                    past_str, cur_str = '', ''
                    if past_total != cur_total:
                        past_str += 'Total->' + str(past_total) + ','
                        cur_str += 'Total->' + str(cur_total) + ','
                    if past_death != cur_death:
                        past_str += 'Death->' + str(past_death) + ','
                        cur_str += 'Death->' + str(cur_death) + ','
                    if past_recover != cur_recover:
                        past_str += 'Recovered->' + str(past_recover) + ','
                        cur_str += 'Recovered->' + str(cur_recover) + ','
                    if past_active != cur_active:
                        past_str += 'Active->' + str(past_active) + ','
                        cur_str += 'Active->' + str(cur_active) + ','
                    if past_serious != cur_serious:
                        past_str += 'Serious->' + str(past_serious)
                        cur_str += 'Serious->' + str(cur_serious)
                    if len(past_str) > 0 and len(cur_str) > 0:
                        # print(f'Change for {country}: [{past_str}]->[{cur_str}]')
                        info.append(f'Change for {country}: [{past_str}]->[{cur_str}]')
                    count_country += 1
                    count_past_country += 1
            table = tabulate(stats_main, headers=SHORT_HEADERS, tablefmt='psql')
            table1 = tabulate(stats_country, headers=SHORT_HEADERS_Country, tablefmt='simple')
            events_info = ''
            for event in info:
                logging.warning(event)
                events_info += '\n - ' + event.replace("'", "")
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print('Sent corona-virus update to the Slack App - ', dt_string)
            slack_text = f'Please find CoronaVirus Summary for World below:\n{last_data_updated}\n{events_info}\n```{table}```\nStay Home Stay Safe!!'
            slacker()(slack_text)
            slacker_file()
            send_notification(table)
            save_json(data)
        except Exception as e:
            slacker()(f'Exception occurred: [{e}]')
            print(f'Exception occurred : {e}')


    main_work()
except Exception as err:
    slacker()(f'Exception occurred: [{err}]')
    print(f'Exception occurred: {err}')

schedule.every(10).minutes.do(main_work)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    # print("Current time ran job at - ",time.time())
    schedule.run_pending()
    time.sleep(1)
