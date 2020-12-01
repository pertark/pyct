import click
import requests
import json
from colors import Colors as c

@click.command("stocks", help="Stock information on a company")
@click.argument("company")
def stocks(company):
  click.echo(get_profile(company))


API_KEY = 'ed5445b55b84408f9164908d6dc890ee' # temporary and a bad idea
def get_profile(company):
  try:
    profile = json.loads(requests.get(f'https://financialmodelingprep.com/api/v3/company/profile/{company}?apikey={API_KEY}').text)
    real_time_price = json.loads(requests.get(f'https://financialmodelingprep.com/api/v3/stock/real-time-price/{company}?apikey={API_KEY}').text)
  except:
    return 'api down or bad api key'
  if len(profile) == 0:
    return 'Invalid Company Symbol'
  row_length = 40
  display = ('┌'+'─'*row_length+'┐\n'
            +'│'+c.BOLD+f' {profile["profile"]["companyName"]}'.ljust(row_length, ' ')+c.END+'│\n'
            +'├'+'─'*row_length+'┤\n'
            +'│'+c.BOLD+' Stock Details'.ljust(row_length, ' ')+c.END+'│\n'
            +'│'+f' * symbol: {profile["symbol"]}'.ljust(row_length, ' ')+'│\n'
            +'│'+f' * Exchange: {profile["profile"]["exchange"]}'.ljust(row_length, ' ')+'│\n'
            +'│'+c.BOLD+' Realtime data'.ljust(row_length, ' ')+c.END+'│\n'
            +'│'+f' * Latest Price: {real_time_price["price"]}'.ljust(row_length, ' ')+'│\n'
            +'│'+c.BOLD+' Hourly data'.ljust(row_length, ' ')+c.END+'│\n'
            +'│'+f' * 52 week range: {profile["profile"]["range"]}'.ljust(row_length, ' ')+'│\n'
            +'│'+f' * Price change: {profile["profile"]["changes"]}'.ljust(row_length, ' ')+'│\n'
            +'│'+f' * Price change %: {profile["profile"]["changesPercentage"]}'.ljust(row_length, ' ')+'│\n'
            +'│'+f' * Volume average: {profile["profile"]["volAvg"]}'.ljust(row_length, ' ')+'│\n'
            +'└'+'─'*row_length+'┘')
             
  return display

def load():
  return [stocks]
