import click
import socket
import os
from colors import Colors as c

@click.group(help="Send and recieve messages. ")
def msg():
    pass


@click.command("host", help="Hosts a connection between two people to chat. ")
@click.argument("ip")
def host(ip):
    BUF = 1028
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 69))
    s.listen(1)
    click.echo(c.YELLOW + c.BOLD + "Waiting for a connection... " + c.END)
    while True:
        conn, addr = s.accept()
        if addr[0] != ip:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
        else:
            break
    click.echo(c.GREEN + c.BOLD + "Connected to " + ip + "!" + c.END)
    while True:
        t = input("> ").encode()
        conn.send(t)
        print(conn.recv(BUF).decode())



@click.command("conn", help="Connects to an address to create a chatroom. ")
@click.argument("ip")
def conn(ip):
    BUF = 1028
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        click.echo(c.YELLOW + c.BOLD + "Connecting... ")
        s.connect((ip, 69))
        click.echo(c.GREEN + c.BOLD + "Connected to " + ip + "!" + c.END)
        while True:
            print(s.recv(BUF).decode())
            t = input("> ").encode()
            s.send(t)
    except socket.error:
        click.echo(c.RED + c.BOLD + "Socket error. Unable to connect to " + ip + ".")
        return

msg.add_command(host)
msg.add_command(conn)


def load():
    return [msg]
