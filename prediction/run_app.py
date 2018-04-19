import os

from prediction_server import app

if __name__ == '__main__':
    # app.run()

    if os.getenv('MONGODB_USERNAME', False):
        app.config['MONGODB_USERNAME'] = os.getenv('MONGODB_USERNAME', False)
    else:
        raise EnvironmentError()

    if os.getenv('MONGODB_PASSWORD', False):
        app.config['MONGODB_PASSWORD'] = os.getenv('MONGODB_PASSWORD', False)
    else:
        raise EnvironmentError()

    if os.getenv('MONGODB_HOST', False):
        app.config['MONGODB_HOST'] = os.getenv('MONGODB_HOST', False)
    else:
        raise EnvironmentError()

    app.config['MONGODB_PORT'] = os.getenv('MONGODB_PORT', 27017)

    app.run(host='0.0.0.0', port=5001)
