import requests
import threading

from colorama import Fore

def check_proxy(proxy, working_proxies, verbose):
    try:
        response = requests.get('http://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            if verbose == "y":
                print(f"{Fore.GREEN}Working proxy found: {proxy}{Fore.RESET}")
            working_proxies.append(proxy)
        elif response.status_code != 200:
            if verbose == "y":
                print(f"{Fore.RED}This proxy doesn't work: {proxy}{Fore.RESET}")
    except:
        pass

def get_proxies(source):
    if source == "1":
        url = "https://www.sslproxies.org/"
    elif source == "2":
        url = "https://www.us-proxy.org/"
    elif source == "3":
        url = "https://free-proxy-list.net/"
    else:
        print("You need to make a choice !")

    r = requests.get(url)
    proxies = []

    if source == "1" or source == "2":
        for row in r.text.split('\n')[1:]:
            if row:
                column = row.split(':')
                if len(column) >= 2:
                    proxy = f"http://{column[0]}:{column[1]}"
                    proxies.append(proxy)
    else:
        for row in r.text.split('\n')[1:]:
            if row:
                column = row.split(':')
                if len(column) >= 2:
                    proxy = f"http://{column[0]}:{column[1]}"
                    proxies.append(proxy)

    return proxies

def main():
    working_proxies = []

    help = """
    %s
      _____                      _____                                      
     |  __ \                    / ____|                                     
     | |__) | __ _____  ___   _| (___   ___ _ __ __ _ _ __  _ __   ___ _ __ 
     |  ___/ '__/ _ \ \/ / | | |\___ \ / __| '__/ _` | '_ \| '_ \ / _ \ '__|
     | |   | | | (_) >  <| |_| |____) | (__| | | (_| | |_) | |_) |  __/ |   
     |_|   |_|  \___/_/\_\\__, |_____/ \___|_|  \__,_| .__/| .__/ \___|_|   
                           __/ |                     | |   | |              
                          |___/                      |_|   |_|              
    %s
                          
    %s[1] use sslProxy           (https://www.sslproxies.org/)%s

    %s[2] use us-proxy           (https://www.us-proxy.org/)%s

    %s[3] use free-proxy-list    (https://free-proxy-list.net/)%s
    
    """ % (Fore.CYAN, Fore.RESET, Fore.YELLOW, Fore.RESET,Fore.YELLOW, Fore.RESET,Fore.YELLOW, Fore.RESET)

    print(help)

    select = input(f"{Fore.RED}┌─[root@proxy]─[/home/????/?!?!?!?\n└──╼{Fore.RESET} select: ")
    verbose = input(f"{Fore.RED}┌─[root@proxy]─[/home/????/?!?!?!?\n└──╼{Fore.RESET} verbose? (y/n): ")

    if verbose == "n":
        print(f"{Fore.YELLOW} /!\ Scrapping of all available proxies ...{Fore.RESET}")

    proxies = get_proxies(select)

    threads = []
    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy, working_proxies, verbose))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\nWorking proxies found ({len(working_proxies)}):")

    save_proxies = input(f"{Fore.RED}┌─[root@proxy]─[/home/????/?!?!?!?\n└──╼{Fore.RESET} Do you want to save the working proxies? (y/n): ")

    if save_proxies == 'y':

        name = input(f"{Fore.RED}┌─[root@proxy]─[/home/????/?!?!?!?\n└──╼{Fore.RESET} Enter the file name: ")
        with open(name, "w") as outfile:
            outfile.write("\n".join([p.replace("http://", "").replace("https://", "") for p in working_proxies]))

def run():
    while True:
        main()
        retry = input(f"{Fore.RED}┌─[root@proxy]─[/home/????/?!?!?!?\n└──╼{Fore.RESET} Do you want to get more proxies? (y/n): ")
        if retry != "y":
            print(f"{Fore.YELLOW} Bye! {Fore.RESET}")
            break
        run()

if __name__ == '__main__':
    run()
