import json

class UserReview:
    user_rating: str
    review_date: str
    review_place: str
    review_title: str
    review_text: str
    finds_helpful: str
    review_in_english: bool

    def __init__(self, user_rating: str = "",
                 review_date: str = "",
                 review_place: str = "",
                 review_title: str = "",
                 review_text: str = "",
                 finds_helpful: str = "",
                 review_in_english: bool = True):
        self.user_rating = user_rating
        self.review_date = review_date
        self.review_place = review_place
        self.review_title = review_title
        self.review_text = review_text
        self.finds_helpful = finds_helpful
        self.review_in_english = review_in_english
    

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
        


class ProductReview:
    keyword: str
    user_reviews: list[UserReview]

    def __init__(self, keyword: str = "",
                 user_reviews: list[UserReview] = []):
        self.keyword = keyword
        self.user_reviews = user_reviews
    

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)



class Product:
    product_name: str
    product_category: str
    product_asin: str
    review_url: str
    total_ratings: str
    overall_rating: str
    product_reviews: list[ProductReview]

    def __init__(self, product_name: str = "", 
                 product_category: str = "",
                 product_asin: str = "",
                 review_url: str = "",
                 total_ratings: str = "",
                 overall_rating: str = "",
                 product_reviews: list[ProductReview] = []):
        self.product_name = product_name
        self.product_category = product_category
        self.product_asin = product_asin
        self.review_url = review_url
        self.total_ratings = total_ratings
        self.overall_rating = overall_rating
        self.product_reviews = product_reviews
    

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)