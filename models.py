from dateutil import parser, tz
from datetime import datetime
import facebook
import time

PAGEID = "1481694711905295"

# TODO: Do not hardcode tokens in the app
PAGE_ACCESS_TOKEN = "EAAXTypm3VzwBAJdNiKgVApRBtye4jVvR4n64BOBX5ZAxZAJRFCSzdELYlxsZClzp2WUVOOpXGWjz9OCpM8AFL4EaiSxZBICWYGiCQhFa8Yn7BDOmCZAdBe6isNGt9sZBTou0hIDm2bmH2mVZB5dZCnvyh5nzgzD8CLXNlBC7yYlvaQZDZD"
USER_ACCESS_TOKEN = "EAAXTypm3VzwBACOUiiiSCCOhKrEVatnreVXQC3dP5Esjlvy1S7s4onKlVTuZCDyZB9zuokZCEt8XRk5SzZA3qbB5FAeHZAJZAKtQ7tg0ayo0ZB5J5w9o5SgtrUHxD7pFuW2dKZAbS6er7e08hL0nizMrO4txgq64xymQ1pVzQ9xgrQZDZD"
GRAPH_API_VERSION = "2.10"

def create_post(text, publish=True):
    """
    Create a new post

    Inputs:
        publish - Set to False if the post must not be published. Default is True
    """
    try:
        api = facebook.GraphAPI(PAGE_ACCESS_TOKEN, version=GRAPH_API_VERSION)
        api.put_object("me", "feed", message=text, published=publish)
    except Exception as e:
        print e

def get_posts(unpublished=False):
    """
    Retrieve existing posts along with the number of views for each post

    Inputs:
        unpublished - Set to True to retrieve unpublished posts. Will retrieve published posts by default

    Returns:
        A list of posts
    """
    posts = []

    try:
        api = facebook.GraphAPI(PAGE_ACCESS_TOKEN, version=GRAPH_API_VERSION)
        if unpublished:
            posts = api.get_connections(PAGEID, "promotable_posts", is_published="false").get("data", [])
        else:
            posts = api.get_connections(PAGEID, "posts").get("data", [])

        for post in posts:
            # Get number of views for each post
            post["views"] = 0
            data = api.get_connections(post["id"], "insights/post_impressions").get("data", [])
            for item in data:
                if item["period"] == "lifetime":
                    post["views"] = item["values"][0]["value"]

            # Provide a sortable datetime
            created_time = post.get("created_time")
            if created_time:
                post["created_time"] = parser.parse(created_time).astimezone(tz.tzlocal())
                post["created_time_sorted"] = _convert_datetime_to_unix_timestamp(post["created_time"])
    except Exception as e:
        print e

    return posts

def get_page_info():
    """
    Retrieve basic info about the page

    Returns:
        A dict with info about the page
    """
    try:
        api = facebook.GraphAPI(PAGE_ACCESS_TOKEN, version=GRAPH_API_VERSION)
        page = api.get_connections(PAGEID, "/", fields="id,name,about,link")
    except Exception as e:
        print e

    return page

def _convert_datetime_to_unix_timestamp(dt):
    """
    Helper function to convert a datetime object to a unix timestamp
    """
    if dt:
        return time.mktime(dt.timetuple())

