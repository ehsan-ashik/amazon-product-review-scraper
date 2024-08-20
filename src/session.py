from requests_html import HTMLSession

class Session(object):
  _instance = None

  def __new__(cls):
    if not cls._instance:
      cls._instance = HTMLSession()
    return cls._instance