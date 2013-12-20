# -*- coding: UTF-8 -*-
import requests
import json

class FeedlyClient(object):
    def __init__(self, **options):
        self.client_id = options.get('client_id')
        self.client_secret = options.get('client_secret')
        self.sandbox = options.get('sandbox', True)
        if self.sandbox:
            default_service_host = 'sandbox.feedly.com'
        else:
            default_service_host = 'cloud.feedly.com'
        self.service_host = options.get('service_host', default_service_host)
        self.additional_headers = options.get('additional_headers', {})
        self.token = options.get('token')
        self.secret = options.get('secret')

    def get_code_url(self, callback_url):
        scope = 'https://cloud.feedly.com/subscriptions'
        response_type = 'code'
        
        request_url = '%s?client_id=%s&redirect_uri=%s&scope=%s&response_type=%s' % (
            self._get_endpoint('v3/auth/auth'),
            self.client_id,
            callback_url,
            scope,
            response_type
            )        
        return request_url
    
    def get_access_token(self,redirect_uri,code):
        params = dict(
                      client_id=self.client_id,
                      client_secret=self.client_secret,
                      grant_type='authorization_code',
                      redirect_uri=redirect_uri,
                      code=code
                      )
        
        quest_url=self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params)
        return res.json()
    
    def refresh_access_token(self,refresh_token):
        '''obtain a new access token by sending a refresh token to the feedly Authorization server'''
        params = dict(
                      refresh_token=refresh_token,
                      client_id=self.client_id,
                      client_secret=self.client_secret,
                      grant_type='refresh_token',
                      )
        quest_url=self._get_endpoint('v3/auth/token')
        res = requests.post(url=quest_url, params=params)
        return res.json()
    
    
    def get_user_subscriptions(self,access_token):
        '''return list of user subscriptions'''
        headers = {'Authorization': 'OAuth '+access_token}
        quest_url=self._get_endpoint('v3/subscriptions')
        res = requests.get(url=quest_url, headers=headers)
        return res.json()
    
    def get_feed_content(self,access_token,streamId,unreadOnly,newerThan):
        '''return contents of a feed'''
        headers = {'Authorization': 'OAuth '+access_token}
        quest_url=self._get_endpoint('v3/streams/contents')
        params = dict(
                      streamId=streamId,
                      unreadOnly=unreadOnly,
                      newerThan=newerThan
                      )
        res = requests.get(url=quest_url, params=params,headers=headers)
        return res.json()
    
    def mark_article_read(self, access_token, entryIds):
        '''Mark one or multiple articles as read'''
        headers = {'content-type': 'application/json',
                   'Authorization': 'OAuth ' + access_token
        }
        quest_url = self._get_endpoint('v3/markers')
        params = dict(
                      action="markAsRead",
                      type="entries",
                      entryIds=entryIds,
                      )
        res = requests.post(url=quest_url, data=json.dumps(params), headers=headers)
        return res

    def _get_endpoint(self, path=None):
        url = "https://%s" % (self.service_host)
        if path is not None:
            url += "/%s" % path
        return url
