# imports required
from enum import StrEnum


# amazon review filters to use
class AmazonReviewFilter:
	# override to restrict instantiation
	def __new__(cls, *args, **kwargs):
		if cls is AmazonReviewFilter:
			raise TypeError(f"'{cls.__name__}' cannot be instantiated")
		return object.__new__(cls, *args, **kwargs)

	# enum for reviewer type
	class ReviewerType(StrEnum):
		ALL = 'all_reviews'
		VERIFIED_ONLY = 'avp_only_reviews'

	# enum for sort by
	class SortBy(StrEnum):
		MOST_RECENT = 'recent'
		TOP_REVIEWS = 'helpful'

	# enum for filter by
	class FilterByStar(StrEnum):
		ALL_STARS = 'all_stars'
		FIVE_STAR_ONLY = 'five_star'
		FOUR_STAR_ONLY = 'four_star'
		THREE_STAR_ONLY = 'three_star'
		TWO_STAR_ONLY = 'two_star'
		ONE_STAR_ONLY = 'one_star'
		POSITIVE_REVIEWS = 'positive'
		CRITICAL_REVIEWS = 'critical'



# get parameters for the HTTPS request based on expected filters
def get_params(page: int = 1, 
			   reviewer_type: AmazonReviewFilter.ReviewerType = AmazonReviewFilter.ReviewerType.VERIFIED_ONLY, 
			   sort_by: AmazonReviewFilter.SortBy = AmazonReviewFilter.SortBy.MOST_RECENT,
			   filter_by_star: AmazonReviewFilter.FilterByStar = AmazonReviewFilter.FilterByStar.ALL_STARS,
			   keyword: str = ""):
	# if keyword does not exist, do not add it in the param
	if not keyword or keyword == "":
		return {
			'ie': 'UTF8',
			'reviewerType': str(reviewer_type),
			'sortBy': str(sort_by),
			'filterByStar': str(filter_by_star),
			'pageNumber': str(page),
		}
	else:
		return {
			'ie': 'UTF8',
			'reviewerType': str(reviewer_type),
			'sortBy': str(sort_by),
			'filterByStar': str(filter_by_star),
			'filterByKeyword': keyword,
			'pageNumber': str(page),
		}
	

def set_page_number(params: dict[str, str], page: int):
	params['pageNumber'] = page