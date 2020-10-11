import datetime
import pytz
import urllib.request
import pandas as pd 
from bs4 import BeautifulSoup

# URL request function for getting content data
def url_request(url):
    HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Accept-Language': 'uk-UA, ukr;q=0.5'})
    request = urllib.request.Request(url, headers=HEADERS)
    response = urllib.request.urlopen(request, timeout=5)
    status_code = response.status
    # if no error, then read the response contents
    if 200 <= status_code < 300:
    # read the data from the URL
        data_response = response.read().decode("utf8")
    return data_response

# timestamp for parsing date
def create_timestamp():
    # This timestamp is in UTC
    my_ct = datetime.datetime.now(tz=pytz.UTC)
    tz = pytz.timezone('Europe/Kiev')
    # Now convert it to another timezone
    new_ct = my_ct.astimezone(tz)
    timestamp = new_ct.strftime("%Y-%m-%d-%H-%M")
    return timestamp

# Function for saving results in a csv file
def create_csv(df, filename):
    file_timestamp = create_timestamp()
    csv_file = df.to_csv(f'result_csv/{filename}_{file_timestamp}.csv', index=False, encoding='utf-8')
    print(f"File 'result_csv/{filename}_{time_now}.csv' was created successfully!")
    return csv_file


# retrieve data from the internet
# URL for getting Kyiv city weather
url = "https://meteo.gov.ua/en/33345"

# Getting and parsing the data
data = url_request(url)
soup = BeautifulSoup(data, "html.parser")
city = soup.find("div", {"class": "hdr_fr_bl1_sity" }).get_text().strip()
current_weather = soup.find(id='curWeatherT').get_text().strip()

# Create timestamp for data
time_now = create_timestamp()

# Create dctionary and pandas Dataframe
weather_dict = [{'date': time_now, 'city': city, 'current_weather': current_weather}]
weather_df = pd.DataFrame(data=weather_dict, index=['date'])  

# Save csv file
create_csv(weather_df, "weather_kyiv")
