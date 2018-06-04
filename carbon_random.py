import time
import socket
import urllib2
import json
import random
import threading


ip = "0.0.0.0" #ip address for carbon and graphite
carbon_port = 2003 #Carbon Port
metric_search = "iops" #Metric Name to be searched 
random_value_lower = 1000000 #random value Lower 
random_value_upper = 9999999 #random value Upper  
push_interval = 10.0  #push metric Interval in seconds

def get_list():
  metrics = json.loads(urllib2.urlopen("http://" + ip + ":3000/api/datasources/proxy/1/metrics/index.json").read())
  filtered_metric = [metric for metric in metrics if metric_search in metric]
  return filtered_metric

def collect_metric(name, value, timestamp):
  sock = socket.socket()
  sock.connect((ip, carbon_port))
  sock.send("%s %d %d\n" % (name, value, timestamp))
  sock.close()

def now():
  return int(time.time())

def main():
  for filtered_metric in get_list():
    random_number = random.randint(random_value_lower, random_value_upper)
    collect_metric(filtered_metric, random_number, now())
  
  print(metric_search + " Data Pushed")
  threading.Timer(push_interval, main).start()

if __name__ == '__main__':
  main()
