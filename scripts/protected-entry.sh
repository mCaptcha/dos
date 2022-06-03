#!/bin/bash

source venv/bin/activate && cd protected && locust $@
