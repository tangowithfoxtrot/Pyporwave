# Pyporwave

A Python program to vaporwave-ify any song you want.

## Run

    docker image build -t pyporwave:latest .
    docker run -v $(pwd):/root -it pyporwave:latest "diana ross - your move"
