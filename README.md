# movieticketnotification

## Pre-requisite

1. Python 3.6 or above
2. pip

## Running the project

1. Install the requirements.
```shell
pip install requirements.txt
```

2. Add email and password to use for sending emails in `config/__init__.py`


3. This step is needed for sending email through your google account via SMTP. 
> Google => Manage your Google Account => Security => Less secure app access => Turn on.

4. Run main.py
```shell
python3 main.py
```


## Monitoring a movie booking to open for a date

1. Goto bookmyshow.com and select the movie you want to monitor for your city.


2. Try to Book Tickets and select your desired screen with language.
Example : English, 3D


3. Copy the url. The url will look like `https://in.bookmyshow.com/buytickets/spider-man-no-way-home-patna/movie-patn-ET00319080-MT/20211216` 
where city is **Patna**, movie is **SpiderMan: No way Home** and date is **16 Dec 2021**.


4. Make a **POST** request to **/movies/monitor/booking-started** path with payload:
```json
{
    "url": "<url you copied>",
    "date": "<target date you want to book tickets for>",
    "email": "<your email where you'll get notified>"
}
```

#### Example
Endpoint: `http://127.0.0.1:5000/movies/monitor/booking-started`

Payload: 
```json
{
    "url": "https://in.bookmyshow.com/buytickets/spider-man-no-way-home-patna/movie-patn-ET00319080-MT/20211216",
    "date": "20211217",
    "email": "chaudhary.kc.kunal@gmail.com"
}
```