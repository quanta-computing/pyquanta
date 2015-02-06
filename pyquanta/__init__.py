"""
Main module for pyquanta

Contains base class: Quanta

"""
import json
import logging
import requests

from .objects import get_obj_class
from .objects import Server, Analytics, Monitor


class Quanta:
    """
    The main class to interact with Quanta API

    """
    BASE_URL = "https://www.quanta-monitoring.com"
    API_URL = "/api"


    def __init__(self, url=None):
        """
        Initialize Quanta instance with different parameters

        """
        if url:
            self.url = url
        else:
            self.url = "{}{}".format(self.BASE_URL, self.API_URL)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }
        self.token = None
        self.cookies = requests.cookies.RequestsCookieJar()

        self.logger = logging.getLogger("pyquanta")
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(logging.StreamHandler())

        self.server = get_obj_class(Server, self, self.logger)
        self.monitor = get_obj_class(Monitor, self, self.logger)
        self.analytics = get_obj_class(Analytics, self, self.logger)


    def _get(self, route, jsonify=True, verify=True):
        """
        Retrieves information from quanta API

        """
        url = "{}{}".format(self.url, route)
        self.logger.debug("GET {}".format(url))
        r = requests.get(url,
                         headers=self.headers,
                         cookies=self.cookies,
                         verify=verify)
        self.logger.debug(json.dumps(r.json(), indent=2))
        if jsonify:
            return r.json()
        else:
            return r


    def _post(self, route, data, jsonify=True, verify=True):
        """
        Post information to quanta API

        """
        url = "{}{}".format(self.url, route)
        self.logger.debug("POST {}: {}".format(url, json.dumps(data)))
        r = requests.post(url,
                          data=json.dumps(data),
                          headers=self.headers,
                          cookies=self.cookies,
                          verify=verify)
        self.logger.debug(json.dumps(r.json(), indent=2))
        if jsonify:
            return r.json()
        else:
            return r


    def _put(self, route, data, jsonify=True, verify=True):
        """
        Update an object in the API

        """
        url = "{}{}".format(self.url, route)
        self.logger.debug("PUT {}: {}".format(url, json.dumps(data)))
        r = requests.put(url,
                         headers=self.headers,
                         cookies=self.cookies,
                         data=json.dumps(data),
                         verify=verify)
        self.logger.debug(json.dumps(r.json(), indent=2))
        if jsonify:
            return r.json()
        else:
            return r


    def _delete(self, route, jsonify=True, verify=True):
        """
        Delete an object from API

        """
        url = "{}{}".format(self.url, route)
        self.logger.debug("DELETE {}".format(url))
        r = requests.delete(url,
                            headers=self.headers,
                            cookies=self.cookies,
                            verify=verify)
        self.logger.debug(json.dumps(r.json(), indent=2))
        if jsonify:
            return r.json()
        else:
            return r


    def settings(self):
        """
        Returns the settings for current site

        """
        return self._get(self.site_route + '?q=settings')


    def connect(self, login, password):
        """
        Connect to the API with provided login and password
        This method will retrieve useful tokens and cookies

        """
        payload = {"user": {"email": login, "password": password}}
        r = self._get("/users/login.json", jsonify=False)
        self.token = str(r.json().pop("csrf_token"))
        self.headers['X-CSRF-Token'] = self.token
        self.cookies = r.cookies

        r = self._post("/users/login", payload, jsonify=False)
        self.token = str(r.json().pop("csrf_token"))
        self.headers['X-CSRF-Token'] = self.token
        self.cookies = r.cookies
        self.logger.info("Successfully connected with token: {}".format(self.token))


    @property
    def site_route(self):
        """
        Return the base URL route for the current site

        """
        return "/sites/{}".format(self.site)


    def use_site(self, site_id):
        """
        Set the current instance to use site_id

        """
        self.site = site_id
