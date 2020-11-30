import click


@click.command("hello")
@click.option("--name", help="The person to greet", required=False)
def hello(name):
	if name:
		click.echo('Hello %s!' % name)
	else:
		click.echo("Hello world! ")


def load():
	return [hello]
