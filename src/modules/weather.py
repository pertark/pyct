import click
import requests

@click.command("weather", help="Weather information")
def weather():
  click.echo(get_weather())

def get_weather():
  return requests.get('https://locale.wttr.in').text


def load():
  return [weather]
