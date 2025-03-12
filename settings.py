BASEURL = ("https://onionoo.torproject.org/details?type=relay&running=true&recommended_version=true&"
           "fields=fingerprint,or_addresses,first_seen,country_name,guard_probability,advertised_bandwidth")
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
TIMEOUT = 10
OPEN_FILES = 1000
