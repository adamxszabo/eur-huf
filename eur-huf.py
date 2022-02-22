import requests, datetime

#send email with mailgun api
def send_eurhuf(eur_huf):
    requests.post(
    		"https://api.eu.mailgun.net/v3/YOUR-DOMAIN/messages",
    		auth=("api", "YOUR-API-KEY"),
    		data={"from": "YOUR-NAME <YOUR-EMAIL-ADDRESS>",
    			"to": ["YOUR-EMAIL-ADDRESS"],
    			"subject": "Hi, your daily EURHUF rate is here",
    			"text": "EURHUF rate today: " + str(eur_huf)})

#get yesterday's currency exchange rates from exchangerates api
yesterday = datetime.datetime.now() - datetime.timedelta(1)
yesterdays_date = yesterday.strftime('%Y-%m-%d')
yesterdays_rates = requests.get("http://api.exchangeratesapi.io/v1/{0}?access_key=YOUR-API-KEY&base=EUR&symbols=HUF".format(yesterdays_date))
yesterdays_rates_json = yesterdays_rates.json()
yesterdays_currencies = yesterdays_rates_json["rates"]
yesterdays_eurhuf = yesterdays_currencies["HUF"]

#get today's currency exchange rates
todays_rates = requests.get("http://api.exchangeratesapi.io/v1/latest?access_key=YOUR-API-KEY&base=EUR&symbols=HUF")
todays_rates_json = todays_rates.json()
todays_currencies = todays_rates_json["rates"]
eur_huf = todays_currencies["HUF"]

#calculate change between yesterday's rate and today's rate
eurhuf_change = abs((eur_huf - yesterdays_eurhuf) / yesterdays_eurhuf)

#calculate weekday
weekdays = [0, 1, 2, 3, 4]
weekday_today = datetime.datetime.today().weekday()

#only call function on weekdays and only if the change from yesterday's rate is at least 0.5%
if weekday_today in weekdays and eurhuf_change > 0.005:
    send_eurhuf(eur_huf)
