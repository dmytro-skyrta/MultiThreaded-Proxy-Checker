import sys
import requests                                                                                                         # Importing the requests module for making HTTP requests
import concurrent.futures                                                                                               # Importing concurrent.futures for working with threads and processes
import threading                                                                                                        # Importing threading for working with threads
from loguru import logger
logger.remove()

# Proxy_checker manual settings:
LINK = "https://ipv4.icanhazip.com/"                                                                                    # Site for checking IP
MAX_THREADS = 10                                                                                                        # Define the maximum number of threads
TIMEOUT = 60                                                                                                            # Stop checking proxies after n seconds
lock = threading.Lock()                                                                                                 # Only one thread works at a time
write_to_file = "02 Working proxies.txt"                                                                                # File to write working proxies to
proxy_list_small = "03 Proxy list short.txt"                                                                            # File containing a small list of proxies
proxy_list_big = "04 Proxy list long.txt"                                                                               # File containing a big list of proxies

def check_one_proxy(proxy) :
    proxy = proxy.lower()

    if "://" in proxy :                                                                                                 # Create a dictionary for the proxy
        proxy_dict = {
            "http": f"{proxy}",
            "https": f"{proxy}",
            "ftp": f"{proxy}",
            "ftps": f"/{proxy}",
            "socks": f"{proxy}",
            "socks4": f"{proxy}",
            "socks4a": f"{proxy}",
            "socks5": f"{proxy}",
            "socks5h": f"{proxy}"
            }
    else :
        proxy_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}",
            "ftp": f"ftp://{proxy}",
            "ftps": f"ftps://{proxy}",
            "socks": f"socks://{proxy}",
            "socks4": f"socks4://{proxy}",
            "socks4a": f"socks4a://{proxy}",
            "socks5": f"socks5://{proxy}",
            "socks5h": f"socks5h://{proxy}"
        }

    try:
        response = requests.get(LINK, proxies=proxy_dict, timeout=TIMEOUT)
        ip_address = response.text.strip()
        with lock:
            logger.info(f"Proxy is working: {proxy} ; IP: {ip_address}")
        return proxy
    except requests.exceptions.Timeout:
        with lock:
            logger.info(f"Timeout occurred while checking proxy: {proxy}")
    except requests.exceptions.RequestException:
        with lock:
            logger.info(f"Proxy is invalid: {proxy}")

def check_proxy_list(proxies_list) :
    working_proxies_list = []                                                                                           # Create a list of ONLY working proxies
    leng_from = len(proxies_list)
    logger.info(f"Received {leng_from} proxies. Starting checks in {MAX_THREADS} threads with a timeout of {TIMEOUT} seconds:")
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:                                    # Create a thread pool for parallel execution of checks
        results = executor.map(check_one_proxy, proxies_list)                                                           # Start checking for each proxy in the list
        for result in results:
            if result not in working_proxies_list and result is not None :                                              # If there is no working proxy in the list
                working_proxies_list.append(result)                                                                     # Add the proxy to the list of working proxies
    leng_to = len(working_proxies_list)
    logger.info(f"{leng_to} working proxies were found.")
    return(working_proxies_list)

def read_list_from_file(from_file) :
    with open(from_file, "r") as file :                                                                                 # Read the contents of the .txt file
        proxies_list = [line.strip() for line in file]                                                                  # Create a list of proxies for checking
    return proxies_list

def write_list_to_file(working_proxies_list, write_to_file) :
    leng_to = len(working_proxies_list)
    with lock:                                                                                                          # Use locking
        if working_proxies_list:                                                                                        # Write working proxies to a new file
            with open(write_to_file, "w") as output_file:
                for proxy in working_proxies_list:
                    output_file.write(proxy + "\n")
            logger.info(f"{leng_to} working proxies successfully written to the file {write_to_file}.")
        else:
            logger.info("No working proxies to write to the file.")

def get_connection_choice() :                                                                                           # The user must make a choice
    while True:                                                                                                         # Loop until correct choice
        choice = input(
            "Connection choice. You would like to have connection trought:\n"
            "1 = proxy without a check of any lists of proxies \n"
            "2 = proxy with a check of a short list of proxies\n"
            "3 = proxy with a check of a long list of proxies\n"
            "4 = TOR\n"
            "Make your choice: "
        )
        if choice == "1" :
            logger.info("You chose 1: connection without a proxy list check.")
            working_proxies_list = read_list_from_file(write_to_file)
            return (working_proxies_list)
        elif choice == "2" :
            logger.info("You chose 2: connection through a proxy with a check of a short list of proxies. Starting the checking procedure: ")
            from_file = proxy_list_small
            working_proxies_list = check_proxy_list(read_list_from_file(from_file))
            write_list_to_file(working_proxies_list, write_to_file)
            return (working_proxies_list)
        elif choice == "3" :
            logger.info("You chose 3: connection through a proxy with a check of a long list of proxies. Starting the checking procedure: ")
            from_file = proxy_list_big
            working_proxies_list = check_proxy_list(read_list_from_file(from_file))
            write_list_to_file(working_proxies_list, write_to_file)
            return (working_proxies_list)
        elif choice == "4" :
            logger.info("You chose 4: connection through TOR. Starting the connection through TOR:")
            working_proxies_list = check_proxy_list(["socks5://127.0.0.1:9050"])
            return (working_proxies_list)
        else:
            logger.info("Incorrect input. Please choose only 1, 2, or 3.")

if __name__ == "__main__":
    logger.add(sys.stdout, level="TRACE")
    working_proxies_list = get_connection_choice()
