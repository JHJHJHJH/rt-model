# Project Title

A brief description of what this project does and who it's for.

## 
Nearest weather station : Hong Kong Park
https://colab.research.google.com/drive/1D1EHKsKSAgyYJ7YM3pw6ZnMHXwMmEDi7#scrollTo=Qg26AK7w51OJ
## Changelog
| Attempt | Changelog | Features | Building(s) | NRMSE |
| ------------- |-------------|-------------|-------------|-------------|
| 1.| Feature engineer datetime | 'hour_of_day', 'day_of_week', 'month', 'is_weekend' | A | 0.272324029077967 |
| 2.| Remove rows where 'Total Cooling Load' is 0 kW |'hour_of_day', 'day_of_week', 'month', 'is_weekend' | A | 0.760444006251237 |
| 3.| Reinstate rows where 'Total Cooling Load' is 0 kW. Add 'season','day_of_month' features. | 'hour_of_day', 'day_of_week', 'month', 'is_weekend', 'season', 'day_of_month' | A | 0.27278177369591 |
| 4.| Replace Random Forest with XGBoost model | 'hour_of_day', 'day_of_week', 'month', 'is_weekend', 'season', 'day_of_month' | A | 0.24401739049425 |  
| 5.| Add features - 'humidity', 'temperature' | 'hour_of_day', 'day_of_week', 'month', 'is_weekend', 'season', 'day_of_month', 'humidity', 'temperature' | A | 0.26268367643862 |
| 6.| Remove features - 'day_of_week', 'month', 'day_of_month'| 'hour_of_day', 'is_weekend', 'season', 'humidity', 'temperature'  | A | 0.231354844346216 |
| 7.| Remove features - 'humidity', 'temperature'| 'hour_of_day', 'is_weekend', 'season'  | A | 0.170950607971046 |
| 8.| Add feature - 'is_business_hour', chiller off from 6pm-730am | 'hour_of_day', 'is_weekend', 'season', 'is_business_hour' | A | 0.17083490150497 |
| 9.| Add features - 'is_holiday' | 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday' | A | 0.156259368721473 |
| 10. | Reinstate 'temperature', 'humidity' & add weather features - 'solar' , 'temperature', 'humidity'| 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity' | A | 0.216272799454793
| 11. | Early stopping to prevent overfitting | 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity'| A | 0.20528351341103
| 12. | Add features - 'wind', 'rain'| 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity', 'wind', 'rain' | A | 0.203494898452382
| 13. | Interpolate - 'humidity', 'temperature' due to 15m vs 1h intervals| 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity', 'wind', 'rain'  | A | 0.2237978076295
| 14. | Tune model param - increase max depth | 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity', 'wind', 'rain' | A | 0.229259198863011
| 15. | Discovered and fix interpolated data error from #13| 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity', 'wind', 'rain'  | A | 0.208219339460784
| 16. | Prepare, train, test Building B dataset separately| 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity', 'wind', 'rain'  | A & B | 0.2066380966636
| 17. | Remove booster from A | 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday','solar', 'temperature', 'humidity', 'wind', 'rain' | A & B | 0.203805870641031
| 18. | Reinstate booster. Attempt remove 'solar' due to high weightage, tune params to reduce overfitting| 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday', 'temperature', 'humidity', 'wind', 'rain'  | A & B | 0.213344195415542
| 19. | Debug model with importance chart. Remove 'solar', 'wind', 'rain', 'humidity' | 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday', 'temperature', 'humidity' | A & B | 0.21024732902238
| 20. | Remove 'temperature'| 'hour_of_day', 'is_weekend', 'season', 'is_business_hour', 'is_holiday' | A & B | 0.15415837836889
| 21. | Combine 'is_weekend' and 'is_holiday' to 'is_workday' | 'hour_of_day', ''season', 'is_business_hour', 'is_workday' | A & B | 

*6. Research question/ Hypothesis : Cooling load is affected by occupancy.
- Does it matter whether it is a Monday or Friday ? Or only weekend or weekday.
- Does it matter which month ? Or just affected by seasons.
- Does it matter which day of month (1-30)? 

*7. To compare with (5), why is adding humidity and temperature worst?
*15. Discovered data error on date vs temp/humidity interpolation

## Data
weather report : datetime, relative humidity, temperature, station
source : https://data.gov.hk/en-data/dataset/hk-hko-rss-current-weather-report

mean heat index : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-maximum-mean-heat-index

mean wind speed : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-mean-wind-speed

rainfall : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-total-rainfall

solar radiation : https://data.gov.hk/en-data/dataset/hk-hko-rss-daily-global-solar-radiation

hk holidays : https://data.gov.hk/en-data/dataset/hk-dpo-statistic-cal
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