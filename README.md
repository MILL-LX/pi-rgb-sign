# Pi RGB Sign

This project expands upon the [pi-rgb-slot-machine](https://github.com/MILL-LX/pi-rgb-slot-machine) project. It implements a web application that thas been upgraded to support more types of animations that the slot machine. It also handles requests asynchronously rather than waiting the duration of the selected animation to return to the HTTP client.

## Cloning the repository

This project depends on our fork of the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library. It is included as a submodule in the [dependencies](dependencies) folder of this project. As such, make sure to use the `--recursive` option when cloning this repo onto your Raspberry Pi:

`git clone --recursive https://github.com/MILL-LX/pi-rgb-sign.git`

## Install rpi-rgb-led-matrix in the Pipenv environment

In the top level directory of this project: 

```bash
pipenv install
pipenv shell
cd  ./dependencies/rpi-rgb-led-matrix
make build-python PYTHON=$(which python)
sudo make install-python PYTHON=$(which python)
```

## Installing the application as a Systemd Service

Consult these instructions for starting this application when your Pi boots: [app/systemd/README.md](app/systemd/README.md)

## Running on your dev machine

You can run this code on your development machine using the [RGBMatrixEmulator](https://github.com/ty-porter/RGBMatrixEmulator) library which allows you to develop the python animations using a simulated RGB LED Display. The application will attempt to use this library if it detects that it is not running on a Raspberry Pi.

