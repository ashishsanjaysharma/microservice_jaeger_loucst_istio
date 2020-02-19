import logging
import opentracing
from jaeger_client import Config


def init_ms_tracer(service,JAGER_AGENT_HOST,JAGER_AGENT_PORT):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'local_agent': {
                'reporting_host': JAGER_AGENT_HOST,
                'reporting_port': JAGER_AGENT_PORT,
            },
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service,
    )
    return config.initialize_tracer()


def flask_to_scope(flask_tracer, request):
    return opentracing.tracer.scope_manager.activate(
        flask_tracer.get_span(request),
        False,
    )
