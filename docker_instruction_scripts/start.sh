#!/bin/sh
docker run -it -p 8888:8888 -p 6901:6901 -e VNC_RESOLUTION=1360x768 -v ${PWD}:/root/Documents shhongoist/headless-vnc-neuron
