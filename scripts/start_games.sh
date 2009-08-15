#!/bin/bash
python manage.py runserver --settings settings_main_site 0.0.0.0:8080 &> scripts/main_site.log &
echo $! > scripts/main_site.pid
python manage.py runserver --settings settings_games_site 0.0.0.0:8081 &> scripts/games_site.log &
echo $! > scripts/game_site.pid