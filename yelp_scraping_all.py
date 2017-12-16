
import pandas as pd
import re, csv
import requests
from bs4 import BeautifulSoup

csv_file = pd.read_csv("BJRI_locations.csv")


def yelp_spider(url, filename):
    # keeps track of when the pagination is over
    done = False

    # setup csv and good stuffs
    file = open(filename, 'w', newline='')
    csvfile = csv.writer(file)
    csvfile.writerow(
        ['Username', 'location', 'friend_count', 'review_count', 'photo_count', 'date', 'rating', 'review'])

    # wrapper around the friend, review and photocount
    def get_count(tag, count_type):
        try:
            return tag.find('li', class_=count_type).b.text.encode('ascii', 'ignore');
        except:
            return ''

    while not done:
        print('>>> Scraping {}'.format(url))
        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')

        reviews = soup.findAll('div', class_='review')[1:]

        for li in reviews:
            username = str(li.find('a', class_='user-display-name').text.encode('ascii', 'ignore')).strip().replace(
                '\n', ' ').replace(',', ' ')
            username = username.strip('b').strip('"').strip("'")

            location = str(li.find('li', class_='user-location').b.text.encode('ascii', 'ignore')).strip().replace('\n',
                                                                                                                   ' ').replace(
                ',', ' ')
            location = location.strip('b').strip('"').strip("'")

            friend_count = str(get_count(li, 'friend-count')).strip('b').strip("'")
            review_count = str(get_count(li, 'review-count')).strip('b').strip("'")
            photo_count = str(get_count(li, 'photo-count')).strip('b').strip("'")

            # look for anumber in the title.
            is_match = re.search('[0-9.]+', li.find('div', class_="i-stars")['title'])

            rating = is_match.group() if is_match else ''
            date = str(li.find('span', class_='rating-qualifier').text.strip().encode('ascii', 'ignore')).strip(
                'b').strip("'")

            review = str(li.find('p').text.encode('ascii', 'ignore')).strip().replace('\n', ' ').replace(',', ' ')
            review = review.strip('b').strip('"').strip("'").strip('\\')

            csvfile.writerow([username, location, friend_count, review_count, photo_count, date, rating, review])
        print("poen")
        try:
            next_url = soup.find('a', class_='next').get('href')
            if next_url:
                url = next_url
                print('>>> Moving to next page')
            else:
                done = True

        except:
            done = True

    file.close()


# if __name__ == '__main__':
#    yelp_spider('https://www.yelp.com/biz/ark-chinese-restaurant-alameda-2?osq=Ark+Restaurants', 'ark_restaurant.csv')


len(csv_file["Link"])

for i in range(len(csv_file["Link"])):
    my_string = csv_file["Link"][i]

    yelp_spider(my_string, "files/" + my_string.split("biz/", 1)[1] + ".csv")