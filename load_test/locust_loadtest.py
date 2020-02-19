import json
from locust import HttpLocust, TaskSet, task, constant
#from locust_influx import expose_metrics

#expose_metrics(influx_host='localhost',influx_port= 8086,user='admin',pwd='admin',interval_ms=1000)

class MyTaskSet(TaskSet):
        
    @task
    def put_tests(self):
        headers = {'content-type': 'application/json'}
        self.client.post("/",data= json.dumps({
            "msgid": "1",
            "data": "load_testing"
            }), 
        headers=headers, 
        name = "post request")
        

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    #host= "http://127.0.0.1:8080/"
    wait_time= constant(0)
