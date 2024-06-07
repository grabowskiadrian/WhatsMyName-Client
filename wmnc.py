import argparse
import json
import sys
import requests

DEFAULT_REQUEST_TIMEOUT = 10
STANDARD_HEADERS = {
    "Accept": "text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-language": "en-US;q=0.9,en,q=0,8",
    "accept-encoding": "gzip, deflate",
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0;Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
}

COLOR_OKGREEN = '\033[92m'
COLOR_FAIL = '\033[91m'
COLOR_ENDC = '\033[0m'


def action_update_json():
    """
    Updates the JSON data by downloading it from the official GitHub repository.
    """
    func_download_file("https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data.json", "wmn-data.json")
    func_download_file("https://raw.githubusercontent.com/WebBreacher/WhatsMyName/main/wmn-data-schema.json", "wmn-data-schema.json")


def action_list_sites(list_path):
    """
    Displays the list of available websites and their categories.

    :param list_path: The path to the JSON file with website data.
    """
    sites = func_get_sites(list_path)

    print("|====================================================|======================|")
    print("| {:<50} | {:<20} |".format('Site Name', 'Category'))
    print("|====================================================|======================|")

    for site in sites:
        print("| {:<50} | {:<20} |".format(site['name'], site['cat']))

    print("|====================================================|======================|")
    print("| {:<50} | {:<20} |".format('Total', len(sites)))
    print("|====================================================|======================|")
    print("")


def action_list_categories(list_path):
    """
    Displays the list of website categories and the number of websites in each category.

    :param list_path: The path to the JSON file with website data.
    """
    sites = func_get_sites(list_path)
    categories = {}

    for site in sites:
        if site['cat'] in categories:
            categories[site['cat']] = categories[site['cat']] + 1
        else:
            categories[site['cat']] = 1

    print("|====================================================|======================|")
    print("| {:<50} | {:<20} |".format('Category', 'Sites count'))
    print("|====================================================|======================|")

    for name, count in categories.items():
        print("| {:<50} | {:<20} |".format(name, count))

    print("|====================================================|======================|")
    print("| {:<50} | {:<20} |".format('Total', len(sites)))
    print("|====================================================|======================|")
    print("")


def action_test(site_name, category_name, list_path):
    """
    Conducts tests on websites to verify that the website configuration is correct

    :param site_name: Website name (optional).
    :param category_name: Website category name (optional).
    :param list_path: The path to the JSON file with website data.
    """
    sites = func_get_sites(list_path)

    scope = []

    for site in sites:
        if site_name and site_name.lower() == site['name'].lower():
            scope.append(site)

        if category_name and category_name.lower() == site['cat'].lower():
            scope.append(site)

        if not site_name and not category_name:
            scope.append(site)

    if len(scope) == 0:
        print("No sites to process")

    print("| {:<50} | {:<31} | {:<31} |".format("Site name", "User found", "User not found"))
    print("|====================================================|=================================|=================================|")
    for site in scope:
        status_correct, url, message = func_check_website(site, site['known'][0])
        status_incorrect, url, message = func_check_website(site, "this-is-not-valid-username-mockup")

        if status_correct:
            test_correct = COLOR_OKGREEN + "PASSED" + COLOR_ENDC
        else:
            test_correct = COLOR_FAIL + "NOT PASSED" + COLOR_ENDC

        if not status_incorrect:
            test_incorrect = COLOR_OKGREEN + "PASSED" + COLOR_ENDC
        else:
            test_incorrect = COLOR_FAIL + "NOT PASSED" + COLOR_ENDC

        if not status_correct:
            test_incorrect = COLOR_FAIL + "???" + COLOR_ENDC

        print("| {:<50} | {:<40} | {:<40} |".format(site['name'], test_correct, test_incorrect))
    print("|====================================================|=================================|=================================|")


def action_find(username, site_name, category_name, list_path):
    """
    Searches websites to find a specific user.

    :param username: The username to search for.
    :param site_name: Website name (optional).
    :param category_name: Website category name (optional).
    :param list_path: The path to the JSON file with website data.
    """
    sites = func_get_sites(list_path)

    scope = []

    for site in sites:
        if site_name and site_name.lower() == site['name'].lower():
            scope.append(site)

        if category_name and category_name.lower() == site['cat'].lower():
            scope.append(site)

        if not site_name and not category_name:
            scope.append(site)

    if len(scope) == 0:
        print("No sites to process")

    for site in scope:
        status, url, message = func_check_website(site, username)

        if status:
            print(f"" + COLOR_OKGREEN + "[+]" + COLOR_ENDC + " Checking " + site['name'] + " : " + COLOR_OKGREEN + message + COLOR_ENDC + " : " + url)
        else:
            print(f"" + COLOR_FAIL + "[-]" + COLOR_ENDC + " Checking " + site['name'] + " : " + COLOR_FAIL + message + COLOR_ENDC)


def func_check_website(website_data, username):
    """
    Checks a website for the presence of a specific user.

    :param website_data: Website data in dictionary format.
    :param username: The username to check for.
    :return: A tuple (status, url, message).
    """
    requestHeaders = STANDARD_HEADERS

    if "headers" in website_data:
        requestHeaders.update(website_data['headers'])

    try:
        uri_check = website_data['uri_check'].format(account=username)

        if "post_body" in website_data:
            parameters = {}
            params = website_data['post_body'].split("&")
            for param in params:
                param_data = param.split("=")
                parameters[param_data[0]] = param_data[1].format(account=username)

            res = requests.post(uri_check, data=parameters, headers=requestHeaders, timeout=DEFAULT_REQUEST_TIMEOUT, allow_redirects=False)
        else:
            res = requests.get(uri_check, headers=requestHeaders, timeout=DEFAULT_REQUEST_TIMEOUT, allow_redirects=False)

        if "uri_pretty" in website_data:
            user_url = website_data['uri_pretty'].format(account=username)
        else:
            user_url = uri_check

        estring_pos = res.text.find(website_data["e_string"]) > 0
        estring_neg = res.text.find(website_data["m_string"]) > 0

        if website_data["e_string"] == "" and res.text == "":
            estring_pos = True

        if res.status_code == website_data['e_code'] and estring_pos:
            return True, user_url, "Found"
        elif res.status_code == website_data['m_code'] and estring_neg:
            return False, "", "Not found"
        else:
            return None, "", "Probably not found"

    except Exception as e:
        return False, "", "Problem with request"


def func_get_sites(list_path):
    """
    Loads website data from a JSON file.

    :param list_path: The path to the JSON file with website data.
    :return: A list of websites.
    """
    if list_path is None:
        list_path = "wmn-data.json"

    with open(list_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        sites = data["sites"]

    return sites

def func_download_file(url, local_filename):
    """
    Downloads a file from the internet and saves it locally.

    :param url: The URL from which the file should be downloaded.
    :param local_filename: The name of the file to be saved.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(local_filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"" + COLOR_OKGREEN + "[+]" + COLOR_ENDC + f" {local_filename} updated")
    except requests.exceptions.RequestException as e:
        print(f"" + COLOR_FAIL + "[-]" + COLOR_ENDC + f" Failed to download {local_filename}: {e}")

# wrapper
if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'update':
            parser = argparse.ArgumentParser(prog='python3 wmnc.py update',
                                             description="Download the newest version of wmn-data.json from the official GitHub repository.")
            args, unknown = parser.parse_known_args()

            action_update_json()
            exit(0)

        if len(sys.argv) > 1 and sys.argv[1] == 'test':
            parser = argparse.ArgumentParser(prog='python3 wmnc.py test',
                                             description="Run tests on websites to verify that the website configuration is correct")
            parser.add_argument("-s", "--site", help="")
            parser.add_argument("-c", "--category", help="")
            parser.add_argument("-l", "--list", help="Specify the path to a JSON file with the websites list (optional).")
            args, unknown = parser.parse_known_args()

            action_test(args.site, args.category, args.list)
            exit(0)

        if len(sys.argv) > 1 and sys.argv[1] == 'find':
            parser = argparse.ArgumentParser(prog='python3 wmnc.py find',
                                             description="Search all websites in the Project WhatsMyName database for a specific username.")
            parser.add_argument("action", help="")
            parser.add_argument("username", help="Specify the username to search for.")
            parser.add_argument("-s", "--site", help="Specify the name of the website to search (optional).")
            parser.add_argument("-c", "--category", help="Specify the name of the website category to search (optional).")
            parser.add_argument("-l", "--list", help="Specify the path to a JSON file with the websites list (optional).")
            args, unknown = parser.parse_known_args()

            action_find(args.username, args.site, args.category, args.list)
            exit(0)

        if len(sys.argv) > 1 and sys.argv[1] == 'list-sites':
            parser = argparse.ArgumentParser(prog='python3 wmnc.py list-sites',
                                             description="List all websites from the wmn-data.json file.")
            parser.add_argument("-l", "--list", help="Specify the path to a JSON file with the websites list (optional).")
            args, unknown = parser.parse_known_args()

            action_list_sites(args.list)
            exit(0)

        if len(sys.argv) > 1 and sys.argv[1] == 'list-categories':
            parser = argparse.ArgumentParser(prog='python3 wmnc.py list-categories',
                                             description="List all website categories from the wmn-data.json file.")
            parser.add_argument("-l", "--list", help="Specify the path to a JSON file with the websites list (optional).")
            args, unknown = parser.parse_known_args()

            action_list_categories(args.list)
            exit(0)

        print("""░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░▒█░░▒█░█░░░░█▀▀▄░▀█▀░█▀▀░▒█▀▄▀█░░░░░░▒█▄░▒█░█▀▀▄░█▀▄▀█░█▀▀░
░▒█▒█▒█░█▀▀█░█▄▄█░░█░░▀▀▄░▒█▒█▒█░█▄▄█░▒█▒█▒█░█▄▄█░█░▀░█░█▀▀░
░▒▀▄▀▄▀░▀░░▀░▀░░▀░░▀░░▀▀▀░▒█░░▒█░▄▄▄▀░▒█░░▀█░▀░░▀░▀░░▒▀░▀▀▀░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░▒█▀▀▄░█░░░▀░░█▀▀░█▀▀▄░▀█▀░░░░░    WhatsMyName-Client   ░░░░
░▒█░░░░█░░░█▀░█▀▀░█░▒█░░█░░░░░░ v0.1 by grabowskiadrian ░░░░
░▒█▄▄▀░▀▀░▀▀▀░▀▀▀░▀░░▀░░▀░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░

Look: https://github.com/WebBreacher/WhatsMyName""")

        print("")

        print("usage: python3 wmnc.py COMMAND [-h]")
        print("\nCommands:")
        print("  update           Download the newest version of wmn-data.json from the official GitHub repository.")
        print("  find USERNAME    Search for a specific USERNAME across all websites in the Project WhatsMyName database (wmn-data.json).")
        print("\nDevelopment:")
        print("  list-sites       List all websites from the wmn-data.json file.")
        print("  list-categories  List all website categories from the wmn-data.json file.")
        print("  test             Run tests on websites to verify that the website configuration is correct.")
    except KeyboardInterrupt:
        print("")
        print("Script stopped")
        sys.exit(0)
