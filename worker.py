import requests
import psycopg2
import psycopg2.extras
from datetime import datetime
import logging
from keys import api_token
from keys import db_password

def fetch_data():
    url='http://api.wunderground.com/api/'+ api_token + '/conditions/q/CA/San_Francisco.json'
    r=requests.get(url).json()
    data=r['current_observation']

    location = data['observation_location']['full']
    weather = data['weather']
    wind_str = data['wind_string']
    temp = data['temp_f']
    humidity = data['relative_humidity']
    precip = data['precip_today_string']
    icon_url = data['icon_url']
    observation_time = data['observation_time']

    #open_db
    try:
        conn=psycopg2.connect(dbname='dnv8cbobu4801', user='qojeyngzlsbhlw', host='ec2-184-72-228-128.compute-1.amazonaws.com', password='6bf8ec6cc31d7be39afbac4f33f0fa3dde89d705b61645b269b3ef0479bba4a0')
        # conn=psycopg2.connect(dbname='mysite', user='postgres', host='localhost', password=db_password)
        print('Opened DB successfully')
    except:
        print(datetime.now(),"Unable to connect to the database")
        logging.exception("Unable to open the database")
        return
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    #write data to server
    cur.execute("""INSERT INTO polls_reading(location, weather, wind_str, temp, humidity, precip, icon_url, observation_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (location, weather, wind_str, temp, humidity, precip, 
                                                            icon_url, observation_time))

    conn.commit()
    cur.close()
    conn.close()

    
    print('Data written', datetime.now())

fetch_data()    
