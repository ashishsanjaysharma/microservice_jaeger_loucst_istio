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

app = Flask('rx')

@app.route('/hellorx')
def hello_world():
    '''
    a check function to see whether receiver is up or not
    '''
    return 'Hello from RX docker!'

@app.route("/",methods=['GET', 'POST'])
def receiver_func():
    '''
    receiver function is the last microservice and receives the http request
    from the previous microservice, extracting span context and sending the span 
    information to jaeger. Also returns a 200 OK message to the sender via 
    in between microservices
    '''
    span_ctx = ms_tracer.extract(
        opentracing.Format.HTTP_HEADERS,
        request.headers,
    )
    with ms_tracer.start_active_span(
        'receiver_func',
        child_of=span_ctx,
        tags={tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER},
    ) as scope:
        return 'OK', 200

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
    MICROSERVICE_NAME = "rx"
    NEXT_HOP = "127.0.0.1"
    DELAY = "2"
    JAGER_AGENT_HOST = "localhost"
    JAGER_AGENT_PORT = "6831"
    ms_tracer = init_ms_tracer(MICROSERVICE_NAME,JAGER_AGENT_HOST,JAGER_AGENT_PORT)
    app.run(port=5000)
    """