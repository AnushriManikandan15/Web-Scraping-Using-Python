

import csv

import logging

import time

 

import requests

from bs4 import BeautifulSoup

 



# Configure logging

logging.basicConfig(filename='scraper.log', level=logging.INFO)

 



def get_links_from_page(url):

    """

    Scrape the page at the given URL and extract all the links on the page.

    :param url: The URL of the page to scrape.

    :return: A list of links on the page.

    """

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.find_all('a')

    return [link.get('href') for link in links if link.get('href')]

 



def scrape_data_from_page(url):

    """

    Scrape the page at the given URL and extract the desired data.

    :param url: The URL of the page to scrape.

    :return: A list of dictionaries representing the scraped data.

    """

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    data = []

    for row in soup.find_all('tr'):

        cells = row.find_all('td')

        if len(cells) == 4:  # Only scrape rows with 4 columns

            item = {

                'name': cells[0].get_text(),

                'description': cells[1].get_text(),

                'price': cells[2].get_text(),

                'rating': cells[3].get_text(),

                'url': url

            }

            data.append(item)

    return data

 



def scrape_data_from_pages(urls):

    """

    Scrape the pages at the given URLs and extract the desired data.

    :param urls: A list of URLs to scrape.

    :return: A list of dictionaries representing the scraped data.

    """

    data = []

    for url in urls:

        try:

            logging.info('Scraping page: {}'.format(url))

            page_data = scrape_data_from_page(url)

            data.extend(page_data)

            time.sleep(1)  # Be polite and wait a second before scraping the next page

        except Exception as e:

            logging.warning('Error scraping page: {}. {}'.format(url, str(e)))

    return data

 



def write_data_to_csv(data, filename):

    """

    Write the scraped data to a CSV file.

    :param data: The data to write.

    :param filename: The name of the CSV file to create.

    """

    with open(filename, 'w', newline='') as csvfile:

        fieldnames = ['name', 'description', 'price', 'rating', 'url']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        writer.writerows(data)

 



def main():

    # URLs to scrape

    urls = [

        'https://example.com/page1',

        'https://example.com/page2',

        'https://example.com/page3',

    ]

 

    # Scrape the data

    data = scrape_data_from_pages(urls)

 

    # Write the data to a CSV file

    write_data_to_csv(data, 'data.csv')

 



if __name__ == '__main__':

    main()
