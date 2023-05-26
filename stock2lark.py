import json
import urllib3

def get_stock_pricing(stock_code):
    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols":  stock_code + ",BTC-USD,EURUSD=X"}
    headers = {
        'x-api-key': "your api key" # get your api key at: https://financeapi.net/
    }

    http = urllib3.PoolManager()
    try:
        resp = http.request('GET', url, headers=headers, fields=querystring)
        data = json.loads(resp.data)['quoteResponse']['result']

        if len(data):
            regularMarketPrice = data[0]['regularMarketPrice']
            regularMarketDayRange = data[0]['regularMarketDayRange']
        else:
            print("An exception occurred: " + "null data!")
    except Exception as e:
        print("An exception occurred: " + str(e))

    Prcing = [regularMarketPrice, regularMarketDayRange]
    return Prcing

def send(content):
    webhook_url = "your webhook_url"

    data = json.dumps({
        "msg_type": "post",
        "content": {
            "post": {
                "zh-CN": {
                    "title": "TSLA: $" +  str(content[0]),
                    "content": [
                        [
                            {
                                "tag": "text",
                                "text": "regularMarketDayRange: $" + str(content[1])
                            }
                        ]
                    ]
                }
            }
        }
    })

    http = urllib3.PoolManager()
    response = http.urlopen("POST", webhook_url, body=data)

    print(response.data)  # for debug or oncall

if __name__ == '__main__':
    stock_code = "TSLA"
    Prcing = get_stock_pricing(stock_code)
    send(Prcing)
