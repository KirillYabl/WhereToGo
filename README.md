# Where to go

### Overview
The site is an interactive map with an expandable (in the admin panel) collection of places (for example, interesting places)
which have a title, description and a set of images.

[Working example](http://kirilliablunovskii.pythonanywhere.com/)

### How to install
Python3 should already be installed. Then use pip to install the dependencies ([virtual environment](https://docs.python.org/3/library/venv.html) is recommended):
```
pip install -r requirements.txt
```

You also need to update the database:
```
python manage.py migrate
```

Optionally (**You can run the site for yourself without this file**) create a `.env` file in `where_to_go` directory with the following options:
- `SECRET_KEY` - [secret key](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) for you site
- `DEBUG` - boolean(true/false) parameter which turn on/off the debug mode. [More](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEBUG)
- `ALLOWED_HOSTS` - is a comma-separated list of IP addresses or URLs that the server can serve. [More](https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts)

Sample contents of `.env` file:
```
SECRET_KEY=5n$@&*)3%586*j=jshty#uak(oi%(%_1^-3xh#pkz+=0m#(4b6
DEBUG=true
ALLOWED_HOSTS=127.0.0.1
```

That's all, you can start the server! Your site will be running at `127.0.0.1:8000`.
```
python manage.py runserver
```

### How to load data
There is a file `init_places.txt` with links to place data.
To download the data, after successfully installing the application, you can enter the following command to download the initial 28 locations:
```
python manage.py load_place init_places.txt -f
```

`load_place` usage:
`python manage.py load_place [url_or_path] [-f] [-fu]`

Where `url_or_path` is a positional argument that is the URL of a single location file or a file with multiple URLs.

The command `load_place` has next options:
- `-f`, `--file` - enter this option if you want to download a file with many location URLs, otherwise the command will wait for a URL with location data
- `-fu`, `--force_update` - the command will update the location with the same title if you enter this option, otherwise the program will ask you

#### How to use admin part of site
Stop the server if it is running.

Create a superuser and follow the command instructions
```
python manage.py createsuperuser
```

Start the server and navigate to `127.0.0.1:8000/admin`.

Enter the login and password that you created earlier while creating the superuser and that's it!

### Features
#### Place pictures
The first image will be displayed permanently and the rest of the images will be displayed on the slider bar.
You can set the image order in the site admin when adding a new location.

#### ![WYSIWYG editor](https://en.wikipedia.org/wiki/WYSIWYG)
A long description of a place can be easily customized in the site admin using the WYSIWYG editor.

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
