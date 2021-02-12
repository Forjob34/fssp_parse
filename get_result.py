import requests
import json
import datetime
from settings import token, base_url


date = datetime.date

list_of_regions = [55, 25]
list_of_names = ['МП Г. ОМСКА "ТЕПЛОВАЯ КОМПАНИЯ"', 'Примтеплоэнерго']


def get_default_choise(region=None, name=None):
    region = int(input('Select default pattern 1 or 2: '))
    if region == 1:
        region = list_of_regions[0]
        name = list_of_names[0]
        return region, name
    elif region == 2:
        region = list_of_regions[1]
        name = list_of_names[1]
        return region, name
    else:
        raise Exception('WRONG NUMBER!')


default_choise = get_default_choise()
region = default_choise[0]
name = default_choise[1]
print(name)


def get_task(token, region, name):
    """ Creating a task for APi processing """

    params = {'token': token,
              'region': region,
              'name': name
              }

    r = requests.get(base_url + 'search/legal', params=params)
    resp_data = r.json()
    task = resp_data['response']['task']
    return task


task = get_task(token, region, name)
print(task)


def get_task_status(token, task):
    """ Obtaining the task status to form a result """

    params = {'token': token,
              'task': task
              }

    r = requests.get(base_url + 'status', params=params)
    task_status = r.json()

    if task_status['response']['status'] != 0:
        print('TASK not ready yet, wait pls')
        while task_status['response']['status'] != 0:
            r = requests.get(base_url + 'status', params=params)
            task_status = r.json()

        return task_status['response']['status']
    else:
        print('Your Task is ready')
        return task_status['response']['status']


task_status = get_task_status(token, task)

print(f'Your Task status is: {task_status}')


def get_result(token, task):
    """ getting a result from a task """

    params = {'token': token,
              'task': task
              }

    r = requests.get(
        'https://api-ip.fssprus.ru/api/v1.0/result', params=params)
    result = r.json()
    if region == 55:
        with open('result/fssp-OMSK-{}.json'.format(date.today().strftime('%d.%m.%Y')), 'w', encoding='utf-8') as write_file:
            json.dump(result, write_file)
    else:
        with open('result/fssp-VLD-{}.json'.format(date.today().strftime('%d.%m.%Y')), 'w', encoding='utf-8') as write_file:
            json.dump(result, write_file)


result = get_result(token, task)
print('all done')
