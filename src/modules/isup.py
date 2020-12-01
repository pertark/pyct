import click
import requests
from colors import Colors as c


@click.command("isup", help="Checks if a website is up")
@click.argument("url")
def isup(url):
  if url.startswith("http://"):
    url = url[7:]
  elif url.startswith("https://"):
    url = url[8:]
  response = requests.get(f"https://isitup.org/{url}.json").json()
  if response["status_code"] == 1:
    click.echo(c.BOLD + c.GREEN + f"Yay! {url} is up! " + c.END)
    click.echo(c.GREEN + f"It took {response['response_time']} ms for a {response['response_code']} code with an ip of {response['response_ip']}" + c.END)
  elif response["status_code"] == 2:
    click.echo(c.BOLD + c.RED + f"{url} seems to be down. :(" + c.END)
  elif response["status_code"] == 3:
    click.echo(c.BOLD + c.RED + "Please provide a valid url! " + c.END)

def load():
  return [isup]