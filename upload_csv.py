# Download csv file for each asx
import urllib


def download_csv(url,destination):
    urllib.request.urlretrieve(url, destination)
