locust -f locust_loadtest.py --host=http://127.0.0.1:8080/ --no-web -c 10 -r 1 -t 1m --csv=stats_csv

host = the host to be put on load
c = no of clients
r = rate at which clients will send request
t = for how long client will send request (1m, 30s, any time interval)


