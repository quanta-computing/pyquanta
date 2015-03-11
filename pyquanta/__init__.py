"""
Main module for pyquanta

Contains base class: Quanta

"""
import json
import logging
import requests

from .resources import get_obj_class
from .resources import Scenario, Server, Endpoint, Account, Organization, Site

from .exceptions import APIError, AttrError


class Quanta:
    """
    The main class to interact with Quanta API

    """
    BASE_URL = "https://www.quanta-monitoring.com"
    API_URL = "/api"


    def __init__(self, url=None, debug=False):
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
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())

        self.sites = get_obj_class(Site, self, self.logger)
        self.organizations = get_obj_class(Organization, self, self.logger)
        self.scenarios = get_obj_class(Scenario, self, self.logger)
        self.servers = get_obj_class(Server, self, self.logger)
        self.magento_monitor = get_obj_class(Endpoint, self, self.logger)
        self.analytics = get_obj_class(Account, self, self.logger)


    def _request(self, route, data, method, jsonify=True, verify=True):
        """
        Executes an HTTP method on Quanta API

        """
        url = "{}{}".format(self.url, route)
        if data is not None:
            data = json.dumps(data)
        self.logger.debug("{} {}".format(method.__name__.upper(), url))
        r = method(url, headers=self.headers, data=data, cookies=self.cookies, verify=verify)
        if r.status_code != 200:
            try:
                r = r.json()
                err = r['error']
            except:
                err = 'HTTP Error {} returned from server'.format(r.status_code)
            finally:
                raise APIError(err)
        if jsonify:
            r = r.json()
            self.logger.debug(json.dumps(r, indent=2))
            if 'error' in r:
                raise APIError(r['error'])
        return r


    def _get(self, route, jsonify=True, verify=True):
        """
        Retrieves information from quanta API

        """
        return self._request(route, None, requests.get, jsonify, verify)


    def _post(self, route, data, jsonify=True, verify=True):
        """
        Post information to quanta API

        """
        return self._request(route, data, requests.post, jsonify, verify)


    def _put(self, route, data, jsonify=True, verify=True):
        """
        Update an object in the API

        """
        return self._request(route, data, requests.put, jsonify, verify)


    def _delete(self, route, jsonify=True, verify=True):
        """
        Delete an object from API

        """
        return self._request(route, None, requests.put, jsonify, verify)


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
        self.logger.debug("Successfully connected with token: {}".format(self.token))


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
