import time
import os
import json
import requests
from flask import Flask
from flask import request
import opentracing
from opentracing.ext import tags
from jaeger_client import Config
from flask import json
import logging
from opentracing_instrumentation.request_context import get_current_span, span_in_context
from lib.tracing import init_ms_tracer


app = Flask('ms')

@app.route('/hello')
def hello_world():
    '''
    a check function to see whether microservice is up or not
    '''
    return 'Hello from ' + MICROSERVICE_NAME +  ' Docker!'


@app.route("/",methods=['GET', 'POST'])
def from_client():
    '''
    function to receive http request from sender(client wrt to microservice)
    extract the span context for use and pass it further to the next microservice(NEXT_HOP) 
    extract the data in the request to send further for NEXT_HOP
    build the next microservice url fetching NEXT_HOP from environment variables
    sleep for configured DELAY -- to simulate some time taken for processing
    send the http request with DATA received to NEXT_HOP and
    finally set the recevied response from the POST to the span
    '''
    span_ctx = ms_tracer.extract(
        opentracing.Format.HTTP_HEADERS,
        request.headers,
    )
    with ms_tracer.start_active_span(
        'from-client',
        child_of=span_ctx,
        tags={tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER},
    ) as scope:
        data_received = json.dumps(request.json)
        print("data_received ==== ",data_received)
        print("microservice_ip ----- ",NEXT_HOP)
        microservice_ip = "http://" + NEXT_HOP + ":5000/"
        processing_delay = float(DELAY)
        #print("processing_delay ----- ",processing_delay, type(processing_delay))
        time.sleep(processing_delay)
        resp_ms = post_data(microservice_ip,data_received)
        scope.span.set_tag('response', resp_ms)
        return resp_ms

def post_data(url, data_received):
    '''
    function to send http request to next microservice
    also inject span context information in the http header to build a single end2end single span for jaeger
    '''
    with ms_tracer.start_active_span('post_data', child_of=get_current_span()) as scope:
        
        scope.span.set_tag(tags.HTTP_URL, url)
        scope.span.set_tag(tags.HTTP_METHOD, 'POST')
        scope.span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_SERVER)
        headers = {'Content-type': 'application/json'}
        ms_tracer.inject(
            scope.span.context, 
            opentracing.Format.HTTP_HEADERS,
            headers,
        )
        r = requests.post(url, data=data_received, headers=headers)
        assert r.status_code == 200
        return r.text

if __name__ == "__main__":
    
    MICROSERVICE_NAME = os.environ.get('MS_NAME')
    JAGER_AGENT_HOST = os.environ.get('JAGER_HOST')
    JAGER_AGENT_PORT = os.environ.get('JAGER_PORT')
    NEXT_HOP = os.environ.get('NEXT_HOP')
    DELAY = os.environ.get('DELAY')
    ms_tracer = init_ms_tracer(MICROSERVICE_NAME,JAGER_AGENT_HOST,JAGER_AGENT_PORT)
    app.run(host="0.0.0.0", debug=True) #will run on flask default port 5000
    
    #the hardcoded section if uncommented, helps the application to run on localhost
    """
    MICROSERVICE_NAME = "ms01"
    JAGER_AGENT_HOST = "localhost"
    JAGER_AGENT_PORT = 6831
    NEXT_HOP = "127.0.0.1"
    DELAY = "2"
    ms_tracer = init_ms_tracer(MICROSERVICE_NAME,JAGER_AGENT_HOST,JAGER_AGENT_PORT)
    app.run(port=8080)
    """