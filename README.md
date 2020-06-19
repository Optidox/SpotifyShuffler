# Shuffler for Spotify

Shuffler is a user-friendly flask webapp for creating random permutations of one or more Spotify playlists.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python 3 and a web browser are all that's necessary for a local copy of Shuffler, but I highly suggest using PyCharm or your preferred IDE as well.

### Installing

To create a working copy of Shuffler on your machine, do the following:

1. Clone this repository with git
```git clone https://github.com/optidox/SpotifyShuffler```
2. Install the packages listed in [requirements.txt](requirements.txt)
```pip install -r requirements.txt```
3. Create a .flaskenv file with the following structure:

```
FLASK_APP=SpotifyShuffler.py
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
SECRET_KEY=your-secret-key
```

For more information on the Spotify environment variables, visit https://developer.spotify.com.

## Running the tests

Once all the above steps are complete, navigate to your project directory in a command line and use the following commands to initialize the database and run the application:

```
flask db init
flask db migrate
flask db upgrade
flask run
```

Open your web browser and go to http://127.0.0.1:5000/ to use Shuffler.

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web framework; other palletsprojects were used to bridge Flask and other tools
* [SQLAlchemy](https://www.sqlalchemy.org/) - Object Relational Mapper
* [MySQL](https://dev.mysql.com/doc/) - Database
* [W3.CSS](https://www.w3schools.com/w3css/) - CSS framework
* [Spotify Web API](https://developer.spotify.com/documentation/web-api/) - Spotify integration

## Author

* **Matthew Sims** - [Optidox](https://github.com/Optidox)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thank you to the many folks whose code, tutorials, or resources were key to creating this project, especially:
* [Miguel Grinberg](https://github.com/miguelgrinberg)
* [Paul Lamere](https://github.com/plamere)
* Adam Quinlan

