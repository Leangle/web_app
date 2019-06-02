#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/5/19

@author: Lawrence
"""
import config_default


class Dict(dict):
    """
    Simple dict but support accesss as x.y style.
    """
    def __init(self, names=(), values=(), **kwargs):
        super().__init__(**kwargs)
        for key, value in zip(names, values):
            self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'Dict' object has no attribute {key}")

    def __setattr__(self, key, value):
        self[key] = value


def merge(defaults, overrides):
    ret = {}
    for key, value in defaults.items():
        if key in overrides:
            if isinstance(value, dict):
                ret[key] = merge(value, overrides[key])
            else:
                ret[key] = overrides[key]
        else:
            ret[key] = value
    return ret


def to_dict(d):
    ret_dict = {}
    for key, value in d.items():
        ret_dict[key] = to_dict(value) if isinstance(value, dict) else value
    return ret_dict


configs = config_default.configs
try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass
