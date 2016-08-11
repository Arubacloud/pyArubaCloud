import requests


class Http(object):
    @staticmethod
    def _log_request(logger, data=None, headers=None):
        if logger is not None:
            if headers is not None:
                for header in headers:
                    logger.debug('request header: %s: %s', header, headers[header])
            if data is not None:
                logger.debug('request data:\n %s', data)

    @staticmethod
    def _log_response(logger, response):
        if logger is not None:
            logger.debug('[%d] %s', response.status_code, response.text)

    @staticmethod
    def get(url, data=None, logger=None, **kwargs):
        if logger is not None:
            Http._log_request(logger, data=data, headers=kwargs.get('headers', None))
        response = requests.get(url, data=data, **kwargs)
        Http._log_response(logger, response)
        return response

    @staticmethod
    def post(url, data=None, json=None, logger=None, **kwargs):
        if logger is not None:
            Http._log_request(logger, data=data, headers=kwargs.get('headers', None))
        response = requests.post(url, data=data, json=json, **kwargs)
        Http._log_response(logger, response)
        return response

    @staticmethod
    def put(url, data=None, logger=None, **kwargs):
        if logger is not None:
            Http._log_request(logger, data=data, headers=kwargs.get('headers', None))
        response = requests.put(url, data=data, **kwargs)
        Http._log_response(logger, response)
        return response

    @staticmethod
    def delete(url, data=None, logger=None, **kwargs):
        if logger is not None:
            Http._log_request(logger, data=data, headers=kwargs.get('headers', None))
        response = requests.delete(url, data=data, **kwargs)
        Http._log_response(logger, response)
        return response
