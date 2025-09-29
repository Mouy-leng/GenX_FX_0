#!/bin/sh

# Start the Gunicorn server in the background
gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 api.main:app &

# Start the Node.js server in the foreground
npm start