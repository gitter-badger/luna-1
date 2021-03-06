# coding=utf8

import inspect

from . import app, config, logger
from .decorators import jsonify
from .hooks import hooks_manager
from flask import jsonify as flask_jsonify, request
from flask.views import MethodView


def init_app():
    app.config.update(config['app'])
    exclude = [pair[0] for pair in inspect.getmembers(MethodView)]
    exclude.extend(['get', 'post', 'put', 'delete', 'options', 'head', 'router'])

    api_loader = hooks_manager.get_hook("api_loader")
    for api in api_loader():
        ins = api()

        # Merge default decorator list
        decorators = [] # Default
        decorators.extend(api.decorators)
        decorators = list(set(decorators))
        api.decorators = [jsonify]
        api.decorators.extend(decorators)

        # Get all extra methods
        methods = inspect.getmembers(api)
        for key, method in methods:
            if key.startswith('_') or key in exclude or not inspect.ismethod(method):
                continue

            # Bind all decorator to instance method.
            ins_method = getattr(ins, key)
            for decorator in ins.decorators:
                ins_method = decorator(ins_method)

            # Get decorator.router options to the methods of MethodView
            options = getattr(ins_method, "options", {})
            rule = getattr(ins_method, "rule", key)

            # Bind extra methods to app url_map
            app.add_url_rule(
                '/'.join([api.router, rule]),
                view_func=ins_method,
                **options
            )
        app.add_url_rule(api.router, view_func=api.as_view(api.__name__))


    @app.errorhandler(Exception)
    def exception_handler(e):
        logger.exception(e)
        return flask_jsonify(dict(
            exception=e.__class__.__name__,
            message=e.message,
            code=getattr(e, 'error_code', 0)
        )), 500

    @app.after_request
    def crossdomain(response):
        h = response.headers

        h['Access-Control-Allow-Origin'] = "*"
        h['Access-Control-Allow-Methods'] = "HEAD, GET, POST, PUT, DELETE, OPTIONS"
        h['Access-Control-Max-Age'] = 21600
        return response


def run_app():
    init_app()
    from pprint import pprint
    from operator import attrgetter

    url_map = list(app.url_map.iter_rules())
    url_map.sort(key=attrgetter('rule'))
    pprint(url_map)
    app.run(host=app.config.get('host') or '127.0.0.1',
            port=app.config.get('port') or 3000)


if __name__ == '__main__':
    run_app()
