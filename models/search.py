""""SEARCH DATA"""
# -*- coding: utf-8 -*-


from odoo import models, fields


class SearchData(models.Model):
    """ Search the details given and write output to 'search.model'."""
    _name = 'search.data'
    _rec_name = 'search'
    _description = 'Search Data'

    search = fields.Char('search string', required=True)
    search_model = fields.Many2one('ir.model')
    data_ids = fields.One2many("search.model", 'search_data_id')

    def search_data(self):
        """
        Search Button function.
        Checks for search details given and calls insert_data() with the data
        to be searched.
        """

        self.env['search.model'].sudo().search([]).unlink()
        if self.search_model:
            for rec in self.env['ir.model.fields'].sudo().search(
                    [('model', '=', self.search_model.model)]):
                self.insert_data(rec)
        else:
            cr = self._cr
            cr.execute("""SELECT table_name FROM information_schema.tables
                      WHERE table_schema='public'""")
            data = cr.dictfetchall()
            for values in data:
                for value in values:
                    for rec in self.env['ir.model.fields'].sudo().search(
                            [('model', '=', values[value].replace("_", "."))]):
                        self.insert_data(rec)

    def insert_data(self, *rec):
        """
            Writes the data passed from search_data() to search_model by
            checking the search details available in database.
            ::text : to convert all types to text format to check, and
            ->> 'en_US' : to get value from dictionary of column type jsonb
                          with key 'en_us'.
        """
        rec = rec[0]
        if rec.ttype == 'char' and rec.store and not rec.model == 'search.model' and not rec.model == 'search.data':
            search = '%' + self.search + '%'
            model = rec.model.replace(".", "_")
            cr = self._cr
            column_type = """select pg_typeof(%s.%s) from %s""" % (
                model, rec.name, model)
            cr.execute(column_type)
            data_type = cr.fetchone()
            if data_type == ('jsonb',):
                query = """select %s ->> 'en_US' from %s where upper(%s->>'en_US') 
                like upper('%s')""" % (
                    rec.name, model, rec.name, search)
            else:
                query = """select %s.%s from %s where upper(%s.%s::text) like 
                upper('%s')""" % (
                    model, rec.name, model, model, rec.name, search)
            cr.execute(query)
            data = cr.dictfetchall()
            if data:
                for values in data:
                    for value in values:
                        self.data_ids.create({
                            'data_field_id': rec.id,
                            'data_name': values[value],
                            'search_data_id': self.id
                        })


class SearchModel(models.Model):
    """ Displays the search output. """
    _name = 'search.model'
    _description = 'Search Model'

    data_field_id = fields.Many2one('ir.model.fields')
    data_name = fields.Char('Value')
    search_data_id = fields.Many2one('search.data')
