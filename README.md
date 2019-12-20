# Pyporwave

A Python program to vaporwave-ify any song you want.

## Run

    docker image build -t pyporwave:1.0 .
    docker run -v $(pwd):/home/jovyan -it pyporwave:1.0 "diana ross - your move"
