# Amazon Product Review Scraper - Python App (v0.1.0)
This Python application scrapes product and user review data from Amazon and parse the collected information in `csv/JSON` format.

### Description:
As described in the project configuration, this application focuses on retrieving user reviews for Amazon products. The reviews can be scraped based on multiple applied filters that Amazon supports alongside support for retrieving reviews based on provided keywords. The application also parse the scraped data into json/csv files.

### Features:
* Can scrape product and review data from a list of Amazon products within a given category.
* Supports proxies in the scraping request. Currently the code supports `SmartProxy` and `Oxylabs Web Unblocker` proxies. Proxy subscription and `username` and `password` required. For other proxies, update `proxy.py` accordingly.
* Extracts user reviews and associated information (user rating, review title, review text, review place and date etc.).
* Supports Amazon's review filters based on keywords, category, and minimum rating (optional) in the scraping job.
* Parse and saves scraped data as csv/JSON file for easy access and analysis.

### Requirements:
* [Python 3.12](https://www.python.org/downloads/)
* [Beautiful Soup 4](https://pypi.org/project/beautifulsoup4/)
* Additional dependencies (See `pyproject.toml`) for advanced scraping and user-agent simulation.

### Installation:
1. Clone or download this repository.
2. Install the required libraries:
    * `pip install poetry`
    * `poetry install` 

### Usage:
1.  **Modify the `config.py` file with your desired scraping parameters:**
    * `product_category`: Indicate the base category of the products to scrape. This will be used to save the scraped files under `generated_data/html_data/{product_category}`.
    * `product_asins`: list of product ASINs that need to be scraped. 
    * `keywords`: A list of keywords to search for in product titles (optional).
    * `scrape_task`: `True` indicates that the data need to be scraped. Set to `False` if data has been previously scraped and only parsing is needed. 
    * `parse_task`: `True` indicates that the scraped data need to be parsed. 
    * `use_csv_parser`: Set it to `True` if the parsed data should be saved in a csv file. If `False` the parsed data will be saved to json. 
    * `use_proxy`: `True` if proxy should be used while scraing (proxy subscription required), otherwise set it to `False`
    * Others configs are available to set expected filter based on Amazon's review filters.
2.  **Run the script:**
    * `poetry run app`

This will scrape product and review data based on your settings and save the results to the csv/json. Please see `example_generated_data` directory for scraping and parsing example outputs. 

#### Example `config.py`:
```python
    # product category, ASINs and keywords
    product_category = 'oyster_sauce'
    product_asins = ['B00842LTE2']
    keywords = ['taste']
    
    # choose scraping parameters
    scrape_task = True
    use_proxy = True # indicate if proxies should be used.

    # choose parsing parameters
    parse_task = True
    use_csv_parser = False # if false, will use json parser

    # choose scraping filters
    reviewer_type = AmazonReviewFilter.ReviewerType.VERIFIED_ONLY
    sort_by = AmazonReviewFilter.SortBy.MOST_RECENT
    filter_by_star = AmazonReviewFilter.FilterByStar.ALL_STARS
    only_english_reviews = True
    
    # include `filter by star` reviews in the scraping task
    filtered_reviews = False # if True, scraper will scrape reviews based on specified `filters`, ignoring the keywords
    filters = [AmazonReviewFilter.FilterByStar.POSITIVE_REVIEWS,
               AmazonReviewFilter.FilterByStar.CRITICAL_REVIEWS]
  ```
  
### Disclaimer:
This application is for educational purposes only. Please respect Amazon's terms of service and avoid excessive scraping that may overload their servers. Be responsible and ethical in your scraping practices.

### Contributing:
Contributions are welcome to improve this application. Feel free to fork the repository and submit pull requests with your enhancements.

### License:
This project is licensed under the MIT License.


### Additional Notes:
* The specific dependencies used beyond core scraping libraries are listed within the pyproject.toml file for reference.
* Consider reviewing the documentation for `requests-html` and `my-fake-useragent` to ensure responsible scraping practices.