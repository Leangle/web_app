#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2019/5/22

@author: Lawrence
"""
import re, time, json, logging, hashlib, base64, asyncio

import markdown2
from coroweb import get, post
from apis import APIValueError, APIResourceNotFoundError

from models import User, Comment, Blog, next_id
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def user2cookie(user, max_age):
    """
    Generate cookie str by user.
    :param user:
    :param max_age:
    :return:
    """
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = f"{user.id}-{user.password}-{expires}-{_COOKIE_KEY}"
    ret_list = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(ret_list)


@get('/')
def index(request):
    summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test Blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time()-3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time()-7200)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs,
    }


@get('/api/users')
async def api_get_users():
    users = await User.find_all(order_by='created_at desc')
    for u in users:
        u.password = '******'
    return dict(user=users)
