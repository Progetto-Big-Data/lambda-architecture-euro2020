#!/bin/bash

# faust will do: from streaming.statistics.statistics_stream import app
faust -A streaming.statistics.statistics_stream worker -l info
