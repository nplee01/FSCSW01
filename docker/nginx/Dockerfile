# syntax=docker/dockerfile:1

# Build our nginx image for backtest
# MUST run ./manage.py collectstatic before build
FROM nginx:1.20-alpine
WORKDIR /html/prod
# copy all static files to be served
COPY ./prod /html/prod/
# Our config file
COPY ./docker/nginx/thecube.conf /etc/nginx/conf.d/
# Command to run (unless overridden) when container starts
CMD ["nginx", "-g", "daemon off;"]
