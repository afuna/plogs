Frontend
---------

Make sure you have npm and grunt-cli installed. Then do:

    npm install
    grunt dist

If you make any modifications to JS/CSS, then run:

    grunt dist
    python manage.py collectstatic --noinput


Server
-------

    heroku local