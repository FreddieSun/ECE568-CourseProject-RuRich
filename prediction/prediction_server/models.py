from typing import List

from werkzeug.datastructures import ImmutableMultiDict


def checkParameters(
        args: ImmutableMultiDict,
        parametersList: List[str],
        parameterOptions=None):
    if parameterOptions is None:
        parameterOptions = {}

    missing_parameter = []
    for parameter in parametersList:
        if parameter not in args:
            missing_parameter.append(parameter)
    if missing_parameter:
        return {
            'type': 'error',
            'error': {
                'errorCode': 100,
                'errorInfo': 'Missing parameters',
                'missingParameters': missing_parameter
            }
        }

    invalid_parameter = []
    for k, v in parameterOptions.items():
        if args.get(k) not in v:
            invalid_parameter.append(k)
    if invalid_parameter:
        return {
            'type': 'error',
            'error': {
                'errorCode': 101,
                'errorInfo': 'Invalid parameter value',
                'invalidParameters': invalid_parameter
            }
        }

    return None
