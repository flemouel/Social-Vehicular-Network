#!/bin/bash

jtrrouter --repair --ignore-errors -n data/RondPoint.net.xml -f data/RondPoint.flow.xml --turn-defaults "50,30,40" -o data/RondPoint.rou.xml
duarouter --repair --ignore-errors -n data/RondPoint.net.xml -f data/RondPointBus.flow.xml -o data/RondPointBus.rou.xml
./runner.py
