# Bitcoin-visualization
SI507 final project

Your GitHub repo must contain a README.md file that gives an overview of your project, including:

## Data sources:
You will need API key and API secrets from both [Coinbase](https://coinbase.com/settings/api) and [Okcoin](https://support.okcoin.com/hc/en-us/articles/360000715751-Create-API) after you log in to both platform.
the format of ```secrets.py``` file:

```
API_KEY_OKCOIN=''
API_SECRET_OKCOIN=''
API_KEY_COINBASE = ''
API_SECRET_COINBASE = ''
```


## Code Structure:


The ```dig_currency.py``` is used to retrieve data use API;
The ```visualize_dc.py``` include functions to process and generate presentations of data;
The ```app.py``` controls the flask structure and call codes from ```templates``` and ```statics``` directory.

The important data processing functions are mainly in ```visualize_dc.py```. 

* ```def boxplot(year)``` retrieve data from database and plot the price fluctuation of Bitcoin;
* ```def line_chart(year)``` retrieve data from database and plot the trend of Bitcoin;
* ```def area_depth(type)``` retrieve data from database and plot the current price depth of Bitcoin;
* ```def rate_bar(year)``` retrieve data from database and plot the changing rate of Bitcoin.

## Guide to run the program:

Please download all the library that needed for the program listed in the ```requirement.txt```
To run the program, please start the virtual environment and copy ```gunicorn app:app``` into terminal in Mac(That's all I know about) and go to [http://127.0.0.1:8000 ](http://127.0.0.1:8000) to run the interaction website!

