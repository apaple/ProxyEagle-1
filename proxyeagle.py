from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from concurrent.futures import Future
import socket
from sys import exit,argv
import os.path
from os import cpu_count

# Author: Z3NTL3
# Studios: Pix4Devs
# Contact: www.pix4.dev

cores = (cpu_count() * 2) -2

def Usage():
    print(f"""
[Usage]
> python3 {__file__} timeout file.txt protocol

[Example]
> python3 {__file__} 6 proxies.txt http
> python3 {__file__} 6 proxies.txt https
> python3 {__file__} 6 proxies.txt socks
""")
goods = ""
def Logo():
    print("""
\033[38;5;206m╔═╗╦═╗╔═╗═╗ ╦╦ ╦  ╔═╗╔═╗╔═╗╦  ╔═╗
\033[38;5;207m╠═╝╠╦╝║ ║╔╩╦╝╚╦╝  ║╣ ╠═╣║ ╦║  ║╣ 
\033[38;5;206m╩  ╩╚═╚═╝╩ ╚═ ╩   ╚═╝╩ ╩╚═╝╩═╝╚═╝
 \033[38;5;206mMade by Pix4Devs - Pix4.dev
 \033[38;5;207mby Z3NTL3\033[0m
""")

try:
    int(argv[1])
    str(argv[2])

    if "http" or "https" or "socks" or "socks4" or "socks5" in argv[3]:
        pass
    else:
        raise RuntimeError()
except:
    Logo()
    Usage()
    exit(-1)

def FileRead(file = argv[2]):
    rox = ""
    if os.path.exists(argv[2]):
        with open(f"{argv[2]}","r")as file:
            content = file.read().strip(" ").split("\n")
        for q in content:
            rox += q+"\n"
        return rox.strip("\n")
    else:
        return False

def ProxyConnector(**info):
    global goods
    sockInit = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        if info['protocol'] == "http":
            hp = 80
            header = f"""GET / HTTP/1.1\r\n"""
            header += f"Host: google.com:{hp}\r\n\r\n"

        elif info['protocol'] == "https":
            hp = 443
            header = f"""GET / HTTP/1.1\r\n"""
            header += f"Host: google.com:{hp}\r\n\r\n"
        else:
            hp = 80
            header = f"""GET / HTTP/1.1\r\n"""
            header += f"Host: google.com:{hp}\r\n\r\n"

        port = int(info['port'])
        sockInit.settimeout(int(argv[1]))
        sockInit.connect((f"{info['proxy']}",port))
        sended = sockInit.send(header.encode("utf-8"))
        response = sockInit.recv(1042).decode()

        succes_codes = [x for x in range(200,299+1)]
        info_codes = [x for x in range(100,199+1)]
        red_codes = [x for x in range(300,399+1)]

        workingProxy = False

        for sc in succes_codes:
            if str(sc) in response:
                workingProxy = True

        for sc in info_codes:
            if str(sc) in response:
                workingProxy = True

        for sc in red_codes:
            if str(sc) in response:
                workingProxy = True

        if workingProxy:
            #print(response)
            goods += f"{info['proxy']}:{info['port']}\n"
            with open('goods.txt',"a+")as file:
                file.write(f"{info['proxy']}:{info['port']}\n")
            return f"\033[32mGood proxy: \033[33m{info['proxy']}:{info['port']}\033[0m"
        else:
            return f"\033[31mBad proxy: \033[33m{info['proxy']}:{info['port']}\033[0m"
    except Exception as e:
        if e == KeyboardInterrupt:
            return "keyboard"
        return f"\033[31mBad proxy: \033[33m{info['proxy']}:{info['port']}\033[0m"
    finally:
        sockInit.close()
def CheckFile(data):
    invalid = False
    for check in data:
        if ":" not in check:
            invalid = True
            break
    if invalid:
        return False
    else:
        return True
def Main():
    ct = FileRead()

    if type(ct) is list:
        pass
    elif type(ct) is bool:
        print(f"\033[31mFile: \033[33m\'{argv[2]}\'\033[0m does not exist in the current directory\033[0m")
        exit(-1)
    
    pool = ThreadPoolExecutor(max_workers=int(cores))
    hosts = []
    ports = []
    proxyWhiteSpaceFix = ct.split("\n")
    destroy = False
    for proxy in proxyWhiteSpaceFix:
        try:
            h,p = proxy.split(":")
        except:
            destroy = True
            break
        hosts.append(h)
        ports.append(p)
    if destroy:
        print("\033[31mYour proxy file contains not a correct format!\nFormats needs to be like proxy:port in each line\033[0m")
        return exit(-1)

    checkX = CheckFile(ct.split("\n"))
    if checkX == False:
        print("\033[31mYour proxy file contains not a correct format!\nFormats needs to be like proxy:port in each line\033[0m")
        return exit(-1)
    else:
       pass

    ftrs = [pool.submit(ProxyConnector,proxy=Worker[0],port=Worker[1],protocol=argv[3]) for Worker in zip(hosts,ports)]
    try:
        for f in as_completed(ftrs):
            if f.result() == "keyboard":
                f.cancel()
                break
            print(f.result())
        pool.shutdown(wait=False,cancel_futures=True)
    except:
        pool.shutdown(wait=False,cancel_futures=True)

if __name__ == "__main__":
    Main()

    
