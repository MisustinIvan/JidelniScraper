# MORTY, MORTY, I TURNED MYSELF INTO A PICKLE! PICKLE RICK!
#import pickle
import lunch_scraper


def main():
    site_url = "https://www.strava.cz/strava5/Jidelnicky?zarizeni=0253"
    scraper = lunch_scraper.lunchScraper(site_url)

    # some code that tests the cursed and evil pickle module, it is a joke

        #pickled_scraper_file = open("./pickled_scraper", "wb")
        #pickle.dump(scraper, pickled_scraper_file)
        #pickled_scraper_file.close()

        #pickled_scraper_file = open("./pickled_scraper", "rb")
        #scraper = pickle.load(pickled_scraper_file)
        #pickled_scraper_file.close()


    print(scraper.lunches[0].date)
    print(scraper.lunches[0].soup)
    print(scraper.lunches[0].lunch)

if __name__ == "__main__":
    main()
