import re
from argparse import ArgumentParser

import requests

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--email', default='')
    parser.add_argument('--password', default='')

    args = parser.parse_args()

    session = requests.Session()

    form_data = {
        'Email': args.email,
        'Password': args.password,
        'RememberMe': True,
    }

    login_response = session.post('https://id.foody.vn/dang-nhap', data=form_data)
    if login_response.status_code != 200:
        raise Exception('Failed to login id.foody.vn (1st step)')
    login_response_raw_content = login_response.content

    # parse validate url
    try:
        search_pattern = r'\"(https\:\/\/www\.now\.vn\:443.*?)\"'
        validate_uri = re.search(search_pattern, login_response_raw_content).group(1)
    except IndexError:
        raise Exception(
            'Failed to parse validate uri in login response (response: %s)' % login_response_raw_content)
    except AttributeError:
        raise Exception('Maybe wrong email or password')

    # validate token --> token returned in Cookie
    validate_response = session.get(validate_uri)
    validate_result = validate_response.content
    if validate_response.status_code != 200 or validate_result != 'done':
        raise Exception('Failed to validate token')

    response = session.post('https://www.now.vn/Order/GetShareLink', json={"deliveryId": 22220})
    if response.status_code == 200:
        user_id = session.cookies.get('hostId')
        if not user_id:
            raise Exception('User id not found despite request is ok!')

        print("Your Foody ID: {}".format(user_id))
    else:
        raise Exception('Failed to obtain user_id')
