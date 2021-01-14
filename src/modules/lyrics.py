import click
import requests
import json
from colors import Colors as c

@click.command("lyrics", help="Get lyrics of a song by an artist")
@click.option("--artist", "-a", required=True,
              help="Artist of song")
@click.option("--song", "-s", required=True,
              help="name of song")
def lyrics(artist, song):
  p = requests.get('https://api.lyrics.ovh/v1/{}/{}'.format(artist, song))
  click.echo(p.status_code)
  lyrics = p.json()['lyrics']
  click.echo(lyrics)


def load():
  return [lyrics]
