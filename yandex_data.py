# -*- coding: utf8 -*-
import json
import time
import tokens
from urllib.request import urlopen

# Данные для изменнения. Города и фразы.
# – Если фраз будет > 10, то скрипт будет делать их в два этапа,
# так как яндекс ограничивает количество фраз.
# – Города указываются в виде ["название", код GeoID из яндекса].
# По названию города будет формироваться файл с данными по его запросам.
#############################################################################
CITIES = ['Москва', 'Ярославль', 'Казань']
PHRASES = ['КГУ кострома']
#############################################################################

url = 'https://api-sandbox.direct.yandex.ru/live/v4/json/'

token = tokens.yandex_direct_token
data_direct = "data_direct"
cities_id = {'архангельск': 20, 'назрань': 1092, 'астрахань': 37, 'нальчик': 30,
'барнаул': 197, 'нижний новгород': 47, 'белгород': 4, 'новосибирск': 65,
'благовещенск': 77, 'омск': 66, 'брянск': 191, 'орел': 10, 'великий новгород': 24,
'оренбург': 48, 'владивосток': 75, 'пенза': 49, 'владикавказ': 33, 'пермь': 50,
'владимир': 192, 'псков': 25, 'волгоград': 38, 'ростов-на-дону': 39, 'вологда': 21,
'рязань': 11, 'воронеж': 193, 'самара': 51, 'грозный': 1106, 'санкт-петербург': 2,
'екатеринбург': 54, 'саранск': 42, 'иваново': 5, 'смоленск': 12, 'иркутск': 63, 'сочи': 239,
'йошкар-ола': 41, 'ставрополь': 36, 'казань': 43, 'сургут': 973, 'калининград': 22,
'тамбов': 13, 'кемерово': 64, 'тверь': 14, 'кострома': 7, 'томск': 67, 'краснодар': 35,
'тула': 15, 'красноярск': 62, 'ульяновск': 195, 'курган': 53, 'уфа': 172, 'курск': 8,
'хабаровск': 76, 'липецк': 9, 'чебоксары': 45, 'махачкала': 28, 'челябинск': 56,
'москва+область': 1, 'черкесск': 1104, 'москва': 213, 'ярославль': 16, 'мурманск': 23,
'россия': 0}

# Функция для формирования отчета
def makeRep (phrases,geo_id):
    for phrase in phrases:
        phrase = '"' + phrase + '"'

    data = {
       'method': 'CreateNewWordstatReport',
       'token': token,
       'param': {
           # не более 10 фраз через запятую
          'Phrases': phrases,
           # нужный регион, если не указали - все регионы
          'GeoID': geo_id
          } }
    jdata = json.dumps(data, ensure_ascii=False)
    response = urlopen(url,jdata.encode())
    answer=json.loads(response.read().decode('utf-8'))
    print(answer)
    query_id = answer.get('data')
    return query_id

# Функция проверки готовности отчета
def checkRep ():
    data = {
        'method': 'GetWordstatReportList',
        'token': token
    }
    jdata = json.dumps(data, ensure_ascii=False)
    response = urlopen(url,jdata.encode())
    responsedata = json.loads(response.read().decode('utf-8', 'ignore'))

    return responsedata['data'][len(responsedata['data'])-1]['StatusReport']

# Чтение отчета
def readRep (query_id, filename):
    # Ожидание готовности отчёта
    while checkRep() != 'Done':
        print ('...')
        time.sleep(2)

    data = {
       'method': 'GetWordstatReport',
       'token': token,
       'param': query_id
    }

    jdata = json.dumps(data, ensure_ascii=False)
    response = urlopen(url,jdata.encode())
    responsedata = json.loads(response.read().decode('utf8'))

    # цикл для записи полученных фраз в файл, так как в консоли все фразы могут не поместиться
    i=0

    # with open( data_direct +"/"+ filename + '.txt', 'w') as f:
    #     f.write('Phrase;Shows' + '\n')
    city_query = []

    for x in responsedata['data']:
        print("!!!" + str(responsedata['data'][i]['SearchedWith']))
        #print(str(responsedata['data'][i]['SearchedWith'][1]))
        datt = responsedata['data'][i]['SearchedWith']
        if len(datt) > 1:
            print(str(datt[1]))
            city_query.append(datt[1])
        else:
            print(str(datt[0]))
            city_query.append(datt[0])
        # for ph in responsedata['data'][i]['SearchedWith']:
        #     print(ph)
        #     result.append(ph)
            # wordstat_item = ph['Phrase'] + ";" + str(ph['Shows'])
            # # print(wordstat_item)
            # f.write(wordstat_item+'\n')
        i=i+1
    res_dict = { 'city':filename, 'SearchedWith':city_query}
    return res_dict

# Удаление прочитанных отчетов
def delRep (query_id):
    data = {
       'method': 'DeleteWordstatReport',
       'token': token,
       'param': query_id
    }

    jdata = json.dumps(data, ensure_ascii=False)
    response = urlopen(url,jdata.encode())
    responsedata = json.loads(response.read().decode('utf8'))

# Запрос остатка баллов
def api ():
    data = {
       'method': 'GetClientsUnits',
       'token': token,
       'param': ['r.cudriavczev']
    }
    jdata = json.dumps(data, ensure_ascii=False)
    response = urlopen(url,jdata.encode())

    responsedata = json.loads(response.read().decode('utf8'))
    return responsedata['data'][0]['UnitsRest']

def run(filename,phrases,geo_id):
    with open("log.txt", "a") as f:
        f.write("\n" + str([filename,phrases,geo_id]))
    # first_score = api()
    # print("Осталось баллов: " + str(first_score))

    query_id = makeRep(phrases=phrases,geo_id=geo_id)
    print ("ID запроса: " + str(query_id))
    data = readRep (query_id, filename)
    delRep (query_id)

    # last_score = api()
    # print("Осталось баллов: " + str(last_score))
    # print("Потрачено: " + str(first_score-last_score))
    print ('-------------')

    return data

def get_city_number(city):
    try:
        return cities_id[city.lower()]
    except:
        return -1

def super_run(phrases, cities):
    result = []
    i = 0
    while i < len(phrases):
        for city in cities:
            city_number = get_city_number(city)
            if city_number != -1:
                res = run(filename=city, phrases=phrases[i:i+10], geo_id=[city_number])
                with open("log.txt", "a") as f:
                    f.write("\n" + str(res))
                result.append(res)
        i += 10
    return result

    print("all ok... END")

#print(super_run(phrases=PHRASES, cities=CITIES))
