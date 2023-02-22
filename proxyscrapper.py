import json
import requests
import threading
import re
import argparse
import sys

from colorama import Fore

def check_proxy(proxy, working_proxies, verbose, all):
    try:
        response = requests.get('http://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            if all:
                location = get_proxies_location(proxy)
                latency_seconds = response.elapsed.total_seconds()
                latency = round(latency_seconds * 1000, 2)

                if verbose:
                    print(f"{Fore.GREEN}Working proxy found: {proxy} {location} {latency}'ms {Fore.RESET}")
                working_proxies.append(f"{proxy} {location} {latency}")
            else:
                if verbose:
                    print(f"{Fore.GREEN}Working proxy found: {proxy} {Fore.RESET}")
                working_proxies.append(f"{proxy}")

        elif response.status_code != 200:
            if verbose:
                print(f"{Fore.RED}This proxy doesn't work: {proxy}{Fore.RESET}")

    except:
        pass

def get_proxies_location(proxy):
    url = "http://ip-api.com/json/"

    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    match = re.search(ip_pattern, proxy)
    ip_address = match.group(0)

    r = requests.get(url + ip_address).content.decode('utf-8')
    values = json.loads(r)

    if values['status'] == "success":
        return values['country']
    else:
        print(f"{Fore.RED} I can't figure out where this proxy came from !")

def get_proxies(country):
    if country is not None:
        if country == "us" or country == "US":
            url = "https://www.us-proxy.org/"
        elif country == "uk" or country == "UK":
            url = "https://free-proxy-list.net/uk-proxy.html"
    else:
        url = "https://www.sslproxies.org/"

    r = requests.get(url)
    proxies = []

    for row in r.text.split('\n')[1:]:
        if row:
            column = row.split(':')
            if len(column) >= 2:
                proxy = f"http://{column[0]}:{column[1]}"
                proxies.append(proxy)
    return proxies

def main():
    working_proxies = []

    parser = argparse.ArgumentParser(description='ProxyScrapper')
    parser.add_argument('-c', '--country', type=str, help='Country of the proxy (e.g. "US" or "UK")')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print verbose output')
    parser.add_argument('-a', '--all', action='store_true', help='Save all information about proxies in your output file')
    parser.add_argument('-o', '--output', type=str, help='Output file')
    args = parser.parse_args()

    proxies = get_proxies(country=args.country)

    threads = []
    for proxy in proxies:
        t = threading.Thread(target=check_proxy, args=(proxy, working_proxies, args.verbose, args.all))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if len(working_proxies) >=1:
        print(f"{Fore.GREEN} There are {len(working_proxies)} proxies that seem to work perfectly! {Fore.RESET}")
        if args.output is not None:
            if args.all:
                with open(args.output, "w") as outfile:
                    for proxy_info in working_proxies:
                        proxy, rest = proxy_info.split(" ", 1)
                        country, latency = rest.rsplit(" ", 1)
                        outfile.write(f"{proxy} [{country}] [{latency}'ms]\n")
                    print(f"{Fore.GREEN} There are {len(working_proxies)} saved in {args.output}")
            else:
                with open(args.output, "w") as outfile:
                    outfile.write(
                        "\n".join([p.replace("http://", "").replace("https://", "") for p in working_proxies]))
                print(f"{Fore.GREEN} There are {len(working_proxies)} saved in {args.output}")
        else:
            for working_prox in working_proxies:
                print(f"{Fore.GREEN} {working_prox} [+] {Fore.RESET}")
            sys.exit()
    else:
        print(f"{Fore.RED} 0 proxy found! {Fore.RESET}")
        sys.exit()

if __name__ == '__main__':
    main()
