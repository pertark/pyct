import click
import requests
import json

@click.command("stocks")
@click.argument("company")
def stocks(company):
  click.echo(get_profile(company))


API_KEY = 'ed5445b55b84408f9164908d6dc890ee' # temporary and a bad idea
def get_profile(company):
  try:
    profile = json.load(requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey={API_KEY}').text)
    real_time_price = json.load(requests.get(f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{company}?apikey={API_KEY}').text)
  except:
    return 'api down or bad api key'
  if len(profile) == 0:
    return 'Invalid Company Symbol'
  row_length = 10
  display = ('┌'+'─'*row_length
            +'│'+f' {profile["profile"]["companyName"]}'
            +'├'+'─'*row_length
            +'│'+' Stock Details'
            +'│'+f' * symbol: {profile["symbol"]}'
            +'│'+f' * Exchange: {profile["profile"]["exchange"]}'
            +'│'+' Realtime data'
            +'│'+f' * Latest Price: {real_time_price["price"]}'
            +'│'+' Hourly data'
            +'│'+f' * 52 week range: {profile["profile"]["range"]}'
            +'│'+f' * Price change: {profile["profile"]["changes"]}'
            +'│'+f' * Price change %: {profile["profile"]["changesPercentage"]}'
            +'│'+f' * Volume average: {profile["profile"]["volAvg"]}'
            +'└'+'─'*row_length)
             


def load():
  return [stocks]
