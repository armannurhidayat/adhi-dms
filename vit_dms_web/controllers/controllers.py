# -*- coding: utf-8 -*-
from odoo import http
import simplejson

class VitDmsWeb(http.Controller):

    @http.route('/vit_dms_web/index', auth='public',website=True)
    def index(self, **kw):
        return http.request.render('vit_dms_web.index', {
        })


    @http.route('/vit_dms_web/files', auth='public')
    def files(self, **kw):
        files = http.request.env['muk_dms.file'].search_read([])
        return simplejson.dumps(files)

    @http.route('/vit_dms_web/directories', auth='public')
    def directories(self, **kw):
        # print kw

        ######### get directories
        if 'id' in kw:
            directory_id = int(kw['id']) - 1000
            print directory_id
            domain=[('parent_directory','=', directory_id)]
            files = http.request.env['muk_dms.file'].search_read([('directory', '=', directory_id)])
        else:
            domain = [('is_root_directory','=', True)]
            files = []
            directory_id=False
        directories = http.request.env['muk_dms.directory'].search_read(domain)


        #### prepare final files combined directoris and files
        data=[]
        for dir in directories:
            data.append({
                'id': dir['id'] + 1000,
                'name': dir['name'],
                'state': 'closed',
                'parentId': str(directory_id),
                'type': 'directory'
            })
        for file in files:
            data.append({
                'id': str(file['id']),
                'name': file['name'],
                'state': 'open',
                'parentId': str(directory_id),
                'type': 'file',
            })

        return simplejson.dumps(data)


    @http.route('/vit_dms_web/reviews/read', auth='public', csrf=False)
    def review_read(self, **kw):
        reviews=[]

        if 'file_id' in kw:
            file_id = kw.get('file_id')
            domain=[('file_id','=', int(file_id))]
            reviews = http.request.env['muk_dms.review'].search_read(domain)
        return simplejson.dumps(reviews)