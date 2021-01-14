import click
import socket
import os
from colors import Colors as c
import threading
import sys

@click.group(help="Send and recieve messages. ")
def msg():
    pass

def recieve(conn):
    while True:
        data = conn.recv(1028)
        if not data:
            break
        else:
            click.echo(c.CYAN + c.BOLD + "> " + c.END + data.decode())
    conn.close()

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
    recv = threading.Thread(target=recieve, args=(conn,))
    recv.daemon = True
    recv.start()
    while True:
        r = input()
        try:
            conn.send(r.encode())
        except:
            break
    click.echo(c.RED + c.BOLD + "Connection closed. ")
    sys.exit(0)


@click.command("conn", help="Connects to an address to create a chatroom. ")
@click.argument("ip")
def conn(ip):
    BUF = 1028
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        click.echo(c.YELLOW + c.BOLD + "Connecting... ")
        s.connect((ip, 69))
        click.echo(c.GREEN + c.BOLD + "Connected to " + ip + "!" + c.END)
        recv = threading.Thread(target=recieve, args=(s,))
        recv.daemon = True
        recv.start()
        while True:
            r = input()
            try:
                s.send(r.encode())
            except:
                break
        click.echo(c.RED + c.BOLD + "Connection closed. ")
        sys.exit(0)
    except socket.error:
        click.echo(c.RED + c.BOLD + "Socket error. Unable to connect to " + ip + ".")
        sys.exit(1)

msg.add_command(host)
msg.add_command(conn)


def load():
    return [msg]
