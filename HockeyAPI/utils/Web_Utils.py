import requests
from bs4 import BeautifulSoup, ResultSet, Tag

PARSER = 'html.parser'

"""
A utility module for fetching and parsing web content.
Provides functions to fetch HTML content from URLs and parse it using BeautifulSoup.
Args:
    html_body (str): The HTML content of the web page.
    element_id (str): The ID of the HTML element to retrieve.
Returns:
    BeautifulSoup | None: The HTML element with the specified ID, or None if not found.
"""
def get_element_by_id(html_body: str, element_id: str) -> BeautifulSoup | None:
    soup = BeautifulSoup(html_body, PARSER)
    element = soup.find(id=element_id)
    return element

"""
Get all elements by class name
Args:
    html_body (str): The HTML content of the web page.
    class_name (str): The class name of the HTML elements to retrieve.
Returns:
    ResultSet[Tag] | None: A list of HTML elements with the specified class name, or None if not found.
"""
def get_elements_by_class(html_body: str, class_name: str) -> ResultSet[Tag] | None:
    soup = BeautifulSoup(html_body, PARSER)
    elements = soup.find_all(class_=class_name)
    return elements

"""
Get all elements by tag name
Args:
    html_body (str): The HTML content of the web page.
    tag_name (str): The tag name of the HTML elements to retrieve.
Returns:
    ResultSet[Tag] | None: A list of HTML elements with the specified tag name, or None if not found.
"""
def get_elements_by_tag_name(html_body: str, tag_name: str) -> ResultSet[Tag] | None:
    soup = BeautifulSoup(html_body, PARSER)
    elements = soup.find_all(tag_name)
    return elements

"""
Get all elements by CSS selector
Args:
    html_body (str): The HTML content of the web page.
    selector (str): The CSS selector of the HTML elements to retrieve.
Returns:
    ResultSet[Tag] | None: A list of HTML elements matching the CSS selector, or None if not found.
"""
def get_query_selector(html_body: str, selector: str) -> ResultSet[Tag] | None:
    soup = BeautifulSoup(html_body, PARSER)
    elements = soup.select(selector)
    return elements

"""
Internal function to perform HTTP GET request
Args:
    url (str): The URL to fetch.
Returns:
    requests.Response | str: The HTTP response object or an error message.
"""
def _fetch(url) -> requests.Response | str:
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, allow_redirects=True)
        response.raise_for_status()  # Raise an error for bad responses
        return response
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

"""
Internal function to perform HTTP POST request
Args:
    url (str): The URL to post to.
    body (str): The body of the POST request.
Returns:
    requests.Response | str: The HTTP response object or an error message.
"""
def _post(url: str, body: str, headers: dict) -> requests.Response | str:
    try:
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()  # Raise an error for bad responses
        return response
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

"""
Fetch the body of a URL as text
Args:
    url (str): The URL to fetch.
Returns:
    requests.Response | str: The body of the HTTP response as text or an error message.
"""
def fetch_body(url: str) -> requests.Response | str:
    return _fetch(url).text

"""
Fetch the content of a URL as bytes or string
Args:
    url (str): The URL to fetch.
Returns:
    requests.Response | str: The content of the HTTP response as bytes or string, or an error message.
"""
def fetch_content(url: str) -> bytes | str:
    return _fetch(url).content

"""
Post a body to a URL and get the response as text
Args:
    url (str): The URL to post to.
    body (str): The body of the POST request.
Returns:
    requests.Response | str: The body of the HTTP response as text or an error message.
"""
def post_body(url, body: str) -> requests.Response | str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/json;charset=utf-8'
    }
    return _post(url, body, headers).text

def post_body_no_headers(url, body: str) -> requests.Response | str:
    return _post(url, body, {}).text