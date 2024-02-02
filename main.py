# testing here
from src.scraper import WikipediaScraper
import json, requests

if __name__ == "__main__":
    url = "https://country-leaders.onrender.com"
    country_endpoint = "/countries"
    leaders_endpoint = "/leaders"
    cookies_endpoint = "/cookie"
    status_endpoint = "/status"

    scrap = WikipediaScraper(
        base_url= url,
        country_endpoint= country_endpoint,
        leaders_endpoint= leaders_endpoint,
        cookies_endpoint= cookies_endpoint,
        status_endpoint = status_endpoint)

    # Check status API before starting
    # If output "Alive"
    print("Checking API status...")
    print("Status API: ", scrap.check_status())
    print("Continuing...")
    if scrap.check_status():
        print("Checking cookies...")
        if scrap.check_cookie().status_code == 200:
            print(scrap.check_cookie().text)
            countries = scrap.get_countries().json()

            all_leaders= {}
            for country in countries:
                # Creates a dictionary per country with the leaders' data and stores it back in the leaders_data
                scrap.get_leaders(country)
                all_leaders[country] = scrap.leaders_data
                scrap.leaders_data = all_leaders

            '''
            Now there is a dictionary per country that contains the original leader data:
            A list of dictionaries with all the leader features
            The next step is to access the country dictionary, access the value, which is the original list of leader data
            and retrieve the wiki URL
            '''

            # Iterate over the countries in dictionary
            for country in scrap.leaders_data.values():
                # Access the value of each country -> a list of leaders
                for leader in country:
                    link = leader.get("wikipedia_url")
                    leader["wikipedia_info"] = scrap.get_first_paragraph(link) 

            # Save to file..
            scrap.to_json_file("leaders_data.json")

        else:
            # if cookies invalid return cookie check message
            print(scrap.check_cookie().text)