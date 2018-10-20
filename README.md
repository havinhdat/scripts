# scripts
Control lunch ordering behaviour in VNRnD Teamx

## Requirements:
- python2.7
- pip10.0.1


## Installation:
`pip install -r < requirements.txt`
Install `Chrome Selenium WebDriver`for your OS here http://chromedriver.chromium.org/downloads


### Lunch Ordering from Now
- Adjust your config in `config.py`.
- Set crontab on your "server" 

`*  *  *  *  1-5  /usr/local/bin/python2.7 /Users/xxx/scripts/lunch_ordering.py --env=prd`
- Create your `config.py` from `config.py.example`

That's it.
