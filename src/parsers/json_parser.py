import json
import os.path
from bs4 import BeautifulSoup
from src.helpers.constants import Constants
from src.models.product_data_model import Product, ProductReview, UserReview
from src.helpers.utils import export_to_file, format_text, get_product_filename, get_reviews_filename

class JSONParser:
    _product: Product
    _category: str
    _product_data: list[Product]

    def __init__(self, product_category: str = ""):
        self._category = product_category
        self._product_data = []
    
    def dump_to_json(self):
        """Get the json data associated with product object
        
        Params: None

        Returns: json object for the product
        """
        json_data = json.dumps(self._product_data, default = lambda x: x.__dict__)

        return json_data



    def save_json(self):
        """Save the Product data in a json file
        
        Params: None

        Returns: None
        """
        json_data = self.dump_to_json()

        filename = 'review_data_' + self._category + '.json'

        filename = os.path.join('./src/generated_data/json_data', filename)

        export_to_file(filename, json_data)
    


    def parse_product_info(self, product_asin: str):
        """Parse product information and set to the product object
        
        Params: product asin

        Returns: None
        """        

        self._product = Product(product_asin=product_asin, 
                               review_url=Constants.BASE_URL + product_asin, product_reviews=[])
        
        filename = get_product_filename(dir=self._category, product_asin=product_asin)

        with open(filename, 'r') as file:
            try:
                html_data = file.read()
            except:
                raise BaseException(f"Could not read file with filename: {filename}")
        
        if not html_data or html_data == "":
            raise BaseException(f"No data present in the file with filename: {filename}")
        
        html_data = BeautifulSoup(html_data, 'lxml')

        # get product name
        try:
            product_name = html_data.select_one('[data-hook="product-link"]').text.strip()
            product_short_name = product_name.split(',')[0].strip()
        except:
            raise BaseException(f"Could not parse `product_name` attribute from the data...")
        
        # get total ratings
        try:
            total_ratings = html_data.select_one('[data-hook="total-review-count"]').text.split(' ')[0].strip()
        except:
            raise BaseException(f"Could not parse `total_ratings` attribute from the data...")
        
        # get average rating
        try:
            overall_rating = html_data.select_one('[data-hook="average-star-rating"]').text.split(' ')[0].strip()
        except:
            raise BaseException(f"Could not parse `overall_rating` attribute from the data...")
        
        # update product model 
        self._product.product_name = product_short_name
        self._product.total_ratings = total_ratings
        self._product.overall_rating = overall_rating
        self._product.product_category = self._category

        self._product_data.append(self._product)

    

    def parse_product_reviews(self, product_asin: str, keyword: str, only_english_reviews: bool):
        """Parse product reviews for the keyword of the product 
        
        Params: None

        Returns: None
        """ 
        product_review = ProductReview(keyword = keyword, user_reviews=[])

        filename = get_reviews_filename(dir=self._category, product_asin=product_asin, keyword=keyword)

        with open(filename, 'r') as file:
            try:
                html_data = file.read()
            except:
                raise BaseException(f"Could not read file with filename: {filename}")
        
        if not html_data or html_data == "":
            raise BaseException(f"No data present in the file with filename: {filename}")
        
        html_data = BeautifulSoup(html_data, 'lxml')

        review_divs = html_data.select('div[data-hook="review"]')

        # get all user reviews
        for review_div in review_divs:
            # get user_rating
            try:
                user_rating = review_div.select_one('[data-hook="review-star-rating"]')
                user_rating = user_rating.text.split(' ')[0].strip() if user_rating else 'N/A'
            except:
                raise BaseException(f"Could not parse `user_rating` attribute from the review data...")
            
            # review date and place
            try:
                review_date_place = review_div.select_one('[data-hook="review-date"]').text.strip()
                review_date = review_date_place.split('on')[-1].strip()
                review_place = review_date_place.split('on')[0].split('the')[-1].strip()
            except:
                raise BaseException(f"Could not parse `review_date_place` attribute from the review data...")
            
            # get review_title
            try:
                review_title = review_div.select_one('[data-hook="review-title"]').text.split('\n')[1].strip()
                review_title = format_text(review_title)
            except:
                raise BaseException(f"Could not parse `review_title` attribute from the review data...")

            # get review_text
            try:
                review_text = review_div.select_one('[data-hook="review-body"]').text.strip()
                review_text = format_text(review_text)
            except:
                raise BaseException(f"Could not parse `review_text` attribute from the review data...")

            # get finds_helpful if available
            try:
                finds_helpful = review_div.select_one('[data-hook="helpful-vote-statement"]').text.split(' ')[0].strip() if review_div.select_one('[data-hook="helpful-vote-statement"]') else "0"
                # replace One to numeric 1
                finds_helpful = finds_helpful.replace('One', '1')
            except:
                raise BaseException(f"Could not parse `finds_helpful` attribute from the review data...")
            
            # check and set whether the review is in english
            try:
                review_in_english = False if review_div.select_one('[data-hook="cr-translate-this-review-link"]') else True
            except:
                raise BaseException(f"Could not parse `review_in_english` attribute from the review data...")

            # if only english reviews to be parsed, do not proceed
            if only_english_reviews and not review_in_english:
                continue
                
            # if no rating generated remove them
            if user_rating == 'N/A':
                continue

            # initialize the UserReview object
            user_review = UserReview(user_rating=user_rating,
                                     review_date=review_date, 
                                     review_place=review_place,
                                     review_title=review_title,
                                     review_text=review_text,
                                     finds_helpful=finds_helpful,
                                     review_in_english=review_in_english
                                     )
            
            # add to the product_review
            product_review.user_reviews.append(user_review)
        
        print(f"Review parsed for {keyword}:", len(product_review.user_reviews))
    
        self._product.product_reviews.append(product_review)