# Project Title

A brief description of what this project does and who it's for.

## 
Nearest weather station : Hong Kong Park

## Changelog
| Attempt | Log | Building(s) | NRMSE |
| ------------- |-------------|-------------|-------------|
| 1.| Feature engineer on given timestamps - 'hour_of_day', 'day_of_week', 'month', 'is_weekend' | A | 0.272324029077967 |
| 2.| Remove rows where 'Total Cooling Load' is 0 kW  | A | 0.760444006251237 |
| 3.| Reinstate rows where 'Total Cooling Load' is 0 kW. Add features - 'season', 'day_of_month' | A | 0.27278177369591 |
| 4.| Replace Random Forest with XGBoost model | A | 0.24401739049425 |  
| 5.| Add features - 'humidity', 'temperature' | A | 0.26268367643862 |
| 6.| Remove features - 'day_of_week', 'month', 'day_of_month' | A | 0.231354844346216 |
| 7.| Remove features - 'humidity', 'temperature' | A | 0.170950607971046 |


*6. Research question/ Hypothesis : Cooling load is affected by occupancy.
- Does it matter whether it is a Monday or Friday ? Or only weekend or weekday.
- Does it matter which month ? Or just affected by seasons.
- Does it matter which day of month (1-30)? 

*7. To compare with (5), why is adding humidity and temperature worst?

*8. 

## Data
weather report : datetime, relative humidity, temperature, station
source : https://data.gov.hk/en-data/dataset/hk-hko-rss-current-weather-report

global solar radiation : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-global-solar-radiation

mean heat index : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-maximum-mean-heat-index

mean wind speed : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-mean-wind-speed

rainfall : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-total-rainfall

solar radiation : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-global-solar-radiation
## Installation

Install the project and its dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

Provide instructions and examples for use.

```python
# Code example
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
