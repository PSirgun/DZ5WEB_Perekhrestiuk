import asyncio
import aiohttp
from datetime import datetime, timedelta
import sys



class ExhangeCurrency:
    def __init__(self) -> None:
        self.URL = f"https://api.privatbank.ua/p24api/exchange_rates?json&date="
        self.exchange_dict = {}

    async def get_exchange(self, date:datetime, currency):

        async with aiohttp.ClientSession() as session:
            url = f'{self.URL}{date}'
            async with session.get(url) as response:
                
                status_code = response.status
                if 400 <= status_code < 500:
                    print('Client error')
                if 500 <= status_code:
                    print ("Server error")

                json_dict = await response.json()
                for value in json_dict["exchangeRate"]:
                    if value["currency"] == currency:
                        self.exchange_dict = {
                                "purchase": value["purchaseRate"],
                                "sale": value["saleRate"]
                            }    
        return self.exchange_dict
    
async def get_all_currency(days):
    results = []
    today = datetime.today().date()
    date_range = [(today - timedelta(days=day)).strftime("%d.%m.%Y") for day in range(days)]
    print(date_range) #---------------------------------------------------------------------------------------
    
    exchange_currency = ExhangeCurrency()
    
    for date in date_range:
        rate = await asyncio.gather(exchange_currency.get_exchange(date, "EUR"),
                                    exchange_currency.get_exchange(date, "USD"))
        print (rate) #---------------------------------------------------------------------------------------
        result = {
            date: {
                "EUR": {
                    "purchase": rate[0]["purchase"],
                    "sale": rate[0]["sale"]
                },
                "USD": {
                    "purchase": rate[1]["purchase"],
                    "sale": rate[1]["sale"]
                }
            }
        }
        results.append(result)
    print (results) #---------------------------------------------------------------------------------------
    return results


def main():

    if not sys.argv[1].isdigit() or int(sys.argv[1]) > 10:
        print ("Wrong input.")
        return
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_all_currency(int(sys.argv[1])-1))
    print (result)
    return



if __name__ == '__main__':
    main()