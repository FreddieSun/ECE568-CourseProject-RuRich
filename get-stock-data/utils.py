# -*- coding:utf-8 -*-

import os


class Utils(object):
    @staticmethod
    def get_env(env: str):
        val = os.getenv(env)
        if val is None:
            raise EnvironmentError
        return val
