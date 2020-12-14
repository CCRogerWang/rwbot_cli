import click
import updateModule

@click.group()
def iosbot():
    pass

@iosbot.command()
def initdb():
    click.echo('Initialized the database')

@iosbot.command()
def dropdb():
    click.echo('Dropped the database')

@iosbot.command()
@click.option('-c', '--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    for x in range(count):
        click.echo('Hello %s!' % name)

# @click.option('-p', '--path', help='project path', prompt='Please enter project path')

# @iosbot.command()
# @click.argument('path')
# @click.argument('ssh_path')

@iosbot.command()
@click.option('-p', '--path', help='project path', prompt='Please enter project path')
@click.option('-sp', '--ssh_path', help='ssh path', prompt='Please enter ssh path')
def updatemodule(path, ssh_path):
    updateModule.main(path=path, ssh_path=ssh_path)


if __name__ == '__main__':
    iosbot()