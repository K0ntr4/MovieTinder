# 🎬 MovieTinder

Welcome to **MovieTinder** – your ultimate movie night planning companion! 🚀

Ever struggled to decide on a movie with friends? MovieTinder is here to save the day! Inspired by the swipe-based magic of Tinder, our Python desktop application makes choosing a movie as fun and easy as swiping right! 🍿

## Project Origin
This project was created during day 3 of a hackathon organized by Kevin Chromik.

## Features
- **Connect with Friends:** Link up with your movie buddies, whether it's one friend or a whole group!
- **Swipe Away:** Browse through movies by swiping. Each movie displays essential details like the logo and release date.
- **Find Your Matches:** See which movies both you and your friends have liked. Perfect for planning a movie night that everyone will enjoy!

## How It Works
1. **Connect:** Start by connecting with your friends in the app.
2. **Swipe:** Browse through the movie collection, swiping right to like or left to pass.
3. **Match:** Check out the list of movies that you and your friends both liked – your perfect movie night line-up!

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/K0ntr4/MovieTinder.git
    cd MovieTinder
    ```
2. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Setup your own MySQL-Database
    ```db.sql
    Import the db.sql in MySql
    set your database login credentials in config\dbconfig.json
    ```
4. Get your API-KEY
    ```API-KEY
    go to [themoviedb.org](https://www.themoviedb.org/), sign up and go to settings. To to API tab and request your API-KEY.
    Now you have to copy the API-Token for reading access.
    ``` 
5. Setup a environment variable
    ```Environment variable
    go to your enviroment variable editor and add a variable called: TOKEN
    as value you set your API-Token that you copied in step 4
    ```
6. Run the application:
    ```bash
    python .\src\main.py
    ```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

Happy swiping and enjoy your movie night! 🍿🎥
