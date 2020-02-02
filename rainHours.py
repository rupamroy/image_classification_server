import sayIt

def mapRainData(p):
    return {
        'time': p['time'],
        'precipitationProbability': p['precipitationProbability']
    }


def getRainHours(forecastMapped, appendure):
    highestRain = sorted(forecastMapped, key = lambda i: i['precipitationProbability'],reverse=True)
    highestRainHours = map(mapRainData, highestRain[:3])
    appendure.append('Most rain is expected at ')
    for i in highestRainHours:
        appendure.append('{} with {}% probability,'.format(i['time'], i['precipitationProbability']))

# t = [{'timeStamp': 1580677200, 'time': '04:00 PM', 'precipitation': False, 'precipitationProbability': 0}, {'timeStamp': 1580680800, 'time': '05:00 PM', 'precipitation': True, 'precipitationProbability': 0.8}, {'timeStamp': 1580684400, 'time': '06:00 PM', 'precipitation': False, 'precipitationProbability': 0}, {'timeStamp': 1580688000, 'time': '07:00 PM', 'precipitation': True, 'precipitationProbability': 0.7}, {'timeStamp': 1580691600, 'time': '08:00 PM', 'precipitation': False, 'precipitationProbability': 0}, {'timeStamp': 1580695200, 'time': '09:00 PM', 'precipitation': False, 'precipitationProbability': 0}, {'timeStamp': 1580698800, 'time': '10:00 PM', 'precipitation': True, 'precipitationProbability': 0.5}, {'timeStamp': 1580702400, 'time': '11:00 PM', 'precipitation': False, 'precipitationProbability': 0}, {'timeStamp': 1580706000, 'time': '12:00 AM', 'precipitation': True, 'precipitationProbability': 0}, {'timeStamp': 1580709600, 'time': '01:00 AM', 'precipitation': False, 'precipitationProbability': 0}, {'timeStamp': 1580713200, 'time': '02:00 AM', 'precipitation': True, 'precipitationProbability': 0.2}, {'timeStamp': 1580716800, 'time': '03:00 AM', 'precipitation': False, 'precipitationProbability': 0}]

# toSay = []
# getRainHours(t, toSay)

# sayIt.say(' '.join(toSay))
