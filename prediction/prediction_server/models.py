from typing import List, Dict

import arrow
from werkzeug.datastructures import ImmutableMultiDict


def checkParameters(
        args: ImmutableMultiDict,
        parametersList: List[str],
        parameterType: Dict[str, List[type]] = None,
        parameterOptions: Dict[str, List[str]] = None):
    if parameterOptions is None:
        parameterOptions = {}

    missing_parameter = []
    for parameter in parametersList:
        if parameter not in args:
            missing_parameter.append(parameter)
    if missing_parameter:
        return {
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': 100,
                'errorInfo': 'Missing parameters',
                'missingParameters': missing_parameter
            }
        }

    invalid_type_parameters = []
    for k, v in parameterType.items():
        if type(args.get(k)) not in v:
            invalid_type_parameters.append(k)
    if invalid_type_parameters:
        return {
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': 102,
                'errorInfo': 'Invalid parameter type',
                'invalidParametersType': [{'parameter': ele, 'types': [e.__name__ for e in parameterType[ele]]} for ele
                                          in invalid_type_parameters]
            }
        }

    invalid_parameter = []
    for k, v in parameterOptions.items():
        if args.get(k) not in v:
            invalid_parameter.append(k)
    if invalid_parameter:
        return {
            'type': 'error',
            'time': arrow.utcnow().isoformat(),
            'error': {
                'errorCode': 101,
                'errorInfo': 'Invalid parameter value',
                'invalidParameters': invalid_parameter
            }
        }

    return None
