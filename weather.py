# importing the requests library
import requests
from datetime import datetime
import rainHours
import sayIt

announcement=[]

def getWeather():
    announcement = []
    # api-endpoint
    URL = "http://dataservice.accuweather.com/forecasts/v1/daily/1day/11418_PC"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'apikey': 'aYzKuGPLTjMAdHEYaRUStA8Yra7HcGWq'}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    today = r.json()

    maxtemp = today['DailyForecasts'][0]['Temperature']['Maximum']['Value']
    mintemp = today['DailyForecasts'][0]['Temperature']['Minimum']['Value']
    announcement.append('Weather Headlines for this week\n {}\n'.format(today['Headline']['Text']))
    announcement.append('Todays max Temperature would be:{} and min would be {}\n'.format(
        maxtemp, mintemp))
    dayTimePhrase = today['DailyForecasts'][0]['Day']['IconPhrase']
    dayTimePrecipitation = 'precipitaion' if today['DailyForecasts'][
        0]['Day']['HasPrecipitation'] else 'no precipitation'
    nightTimePhrase = today['DailyForecasts'][0]['Night']['IconPhrase']
    nightTimePrecipitation = 'precipitation' if today['DailyForecasts'][
        0]['Night']['HasPrecipitation'] else 'no precipitation'
    announcement.append('Day time {} with {} and night time {} with {}\n'.format(
        dayTimePhrase, dayTimePrecipitation, nightTimePhrase, nightTimePrecipitation))

    URL = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/11418_PC?apikey=aYzKuGPLTjMAdHEYaRUStA8Yra7HcGWq"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'apikey': 'aYzKuGPLTjMAdHEYaRUStA8Yra7HcGWq'}

    # sending get request and saving the response as response object
    j = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    forecast = j.json()

    forecastMapped = list(map(mapForecast, forecast))

    rainChart = list(filter(getRain, forecastMapped))

    if(len(rainChart) > 0):
        announcement.append('Rain starts at {}\n'.format(rainChart[0]['time']))
        rainHours.getRainHours(forecastMapped, announcement)
    else:
        announcement.append('Rain is not expected in the next 12 hours\n')

    sayIt.say(' '.join(announcement))


def mapForecast(f):
    return {
        'timeStamp': f['EpochDateTime'],
        'time': datetime.fromtimestamp(f['EpochDateTime']).strftime('%I:%M %p'),
        'precipitation': f['HasPrecipitation'],
        'precipitationProbability': f['PrecipitationProbability']
    }

# function that filters precipitation


def getRain(p):
    return p['precipitation']
