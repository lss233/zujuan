import requests

def download(url, num_retries=3, params=None, headers={'user-agent': 'Mozilla/5.0'}, cookies=None, proxy=None):
    try:
        if proxy == None:
            r = requests.get(url, params=params, headers=headers, cookies=cookies, timeout=4)
        else:
            proxies = {'http': proxy}
            r = requests.get(url, params=params, headers=headers, cookies=cookies, proxies=proxies)

        print("Downloading: ", r.url)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
    except TimeoutError:
        return None
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.ConnectTimeout:
        return None
    except:
        print("Download Error", r.status_code)
        if num_retries > 0:
            if 500 <= r.status_code < 600:
                download(url, num_retries-1)
            else:
                return None
        return None
    return r

def download_text(url, num_retries=3, params=None, headers={'user-agent': 'Mozilla/5.0'}, cookies=None, proxy=None):
    r = download(url, num_retries, params, headers, cookies, proxy)
    
    #test for true
    if r == None:
        return None

    return r.text