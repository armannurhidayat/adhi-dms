# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
SESSION_STATES =[('draft','Draft'),('done','Done')]

class muk_dms(models.Model):
	_name = 'muk_dms.file'
	_inherit = 'muk_dms.file'

	name = fields.Char(string="Version")
	tanggal = fields.Date(string="Tanggal Draft", default=lambda self: time.strftime("%Y-%m-%d"))
	status = fields.Selection(string="Status", selection=[
			('Draft', 'Draft'),
			('Open', 'Open'),
			('Done', 'Done')])
	state = fields.Selection(selection=SESSION_STATES, string="State", required=False,
						readonly=True,
						default=SESSION_STATES[0][0], help="")
	review_ids = fields.One2many('muk_dms.review','file_id', string='Review')
	reviewer_ids = fields.One2many('muk_dms.reviewer','file_id', string='Reviewer')
	info_ids = fields.One2many('muk_dms.info','file_id', string='Info')

	@api.multi
	def action_draft(self):
		self.state = SESSION_STATES[0][0]

	@api.multi
	def action_done(self):
		self.state = SESSION_STATES[1][0]

class muk_dms_review(models.Model):
	_name = 'muk_dms.review'

	name = fields.Char(string="Bookmark",)
	tanggal_jam = fields.Date(string="Tanggal Jam", default=lambda self: time.strftime("%Y-%m-%d"))
	redaksi_asal = fields.Char(string="Redaksi Asal",)
	ulas = fields.Char(string="Ulasan",)
	file_id = fields.Many2one(comodel_name='muk_dms.file', string='File')
	user_id = fields.Many2one(comodel_name="res.users", string="Reviewer", required=False, default=lambda self: self.env.user.id)

class muk_dms_reviewer(models.Model):
	_name = 'muk_dms.reviewer'

	name = fields.Many2one(comodel_name="res.users", string="User", required=False,
							default=lambda self: self.env.user.id)
	file_id = fields.Many2one(comodel_name='muk_dms.file', string='Reviewer')

class muk_dms_info(models.Model):
	_name = 'muk_dms.info'

	name = fields.Char(string="Nomor Naskah")
	tanggal_naskah = fields.Date(string="Tanggal Naskah", default=lambda self: time.strftime("%Y-%m-%d"))
	partner = fields.Many2one(comodel_name="res.partner", string="Redaksi Asal")
	deskripsi = fields.Char(string="Deskripsi Naskah")
	file_id = fields.Many2one(comodel_name='muk_dms.file', string='File')