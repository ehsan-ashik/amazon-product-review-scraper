from src.helpers.request_params import AmazonReviewFilter

class AppConfig:
    # input products and keywords
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
    
    # include filter by star reviews in the scraping task
    filtered_reviews = False # if True, scraper will scrape reviews based on specified `filters`, ignoring the keywords
    filters = [AmazonReviewFilter.FilterByStar.POSITIVE_REVIEWS,
               AmazonReviewFilter.FilterByStar.CRITICAL_REVIEWS]