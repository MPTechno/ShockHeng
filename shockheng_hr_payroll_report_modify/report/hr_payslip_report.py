# -*- coding: utf-8 -*-
from openerp import api, models
from openerp.report import report_sxw
from datetime import datetime


class hr_payslip_details_report(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context):
        super(hr_payslip_details_report, self).__init__(cr, uid, name, context)
        self.localcontext.update({
            'get_payslip_lines_allowance': self._get_payslip_lines_allowance,
            'get_payslip_lines_deductions': self._get_payslip_lines_deductions,
            'get_payslip_lines_salary': self._get_payslip_lines_salary,
            'get_payslip_lines_for_cpf_employer': self._get_payslip_lines_for_cpf_employer,
            'get_total_hours': self._get_total_hours,
            'get_payslip_lines_other_additional_payment': self._get_payslip_lines_other_additional_payment,
            'get_payslip_net_pay': self._get_payslip_net_pay,
            'get_currency': self._get_currency,
        })

    def _get_currency(self, object):
        result={}
        result.update({
                       'display_currency': object.company_id.currency_id.symbol
                       })
        return result

    def _get_payslip_lines_other_additional_payment(self, order):
        result = []

        def _get_other_additional_payment(object):
            payslip_input_obj = self.pool.get('hr.payslip.input')
            payslip_line_id = payslip_input_obj.search(self.cr, self.uid,[('id','in',object.input_line_ids.ids)]) 
            payslip_line_ids = payslip_input_obj.browse(self.cr, self.uid,payslip_line_id)
            total_additional_payment = 0.00
            if payslip_line_ids:
                for line in payslip_line_ids:
                    res = {}
                    total_additional_payment += line.amount
                    res['code'] = line.code or ''
                    res['amount'] = line.amount or 0.00
                    result.append(res)
                result[0].update({'total_additional_payment':total_additional_payment})
                return result
        additional_payment = _get_other_additional_payment(order)
        return additional_payment

    def _get_payslip_lines_allowance(self, order):
        result = []

        def _get_allowance(object):
            payslip_line_obj = self.pool.get('hr.payslip.line')
            payslip_line_id = payslip_line_obj.search(self.cr, self.uid,[('id','in',object.line_ids.ids),('category_id.code','=','ALW')]) 
            payslip_line_ids = payslip_line_obj.browse(self.cr, self.uid,payslip_line_id)
            total_allowance = 0.00
            if payslip_line_ids:
                for line in payslip_line_ids:
                    res = {}
                    total_allowance += line.total
                    res['code'] = line.code or ''
                    res['amount'] = line.total or 0.00
                    result.append(res)
                result[0].update({'total_allowance':total_allowance})
                return result
        allowance = _get_allowance(order)
        return allowance

    def _get_payslip_lines_deductions(self, order):
        result = []

        def _get_deductions(object):
            payslip_line_obj = self.pool.get('hr.payslip.line')
            payslip_line_id = payslip_line_obj.search(self.cr, self.uid,[('id','in',object.line_ids.ids),('category_id.code','in',['DED','CAT_CPF_EMPLOYEE','CATCPFAGENCYSERVICESEE'])]) 
            payslip_line_ids = payslip_line_obj.browse(self.cr, self.uid,payslip_line_id)
            total_deductions = 0.00
            if payslip_line_ids:
                for line in payslip_line_ids:
                    res = {}
                    total_deductions += line.total
                    res['code'] = line.code or ''
                    res['amount'] = line.total or 0.00
                    result.append(res)
                result[0].update({'total_deductions':total_deductions})
                return result
        deductions = _get_deductions(order)
        return deductions

    def _get_payslip_lines_salary(self, order):
        result = []
        overtime_pay = self._get_total_hours(order)
        def _get_salary(object):
            payslip_line_obj = self.pool.get('hr.payslip.line')
            payslip_line_id = payslip_line_obj.search(self.cr, self.uid,[('id','in',object.line_ids.ids),('category_id.code','in',['BASIC','SC102'])]) 
            payslip_line_ids = payslip_line_obj.browse(self.cr, self.uid,payslip_line_id)
            total_salary = 0.00
            if payslip_line_ids:
                for line in payslip_line_ids:
                    res = {}
                    total_salary += line.total
                    res['code'] = line.code or ''
                    res['amount'] = line.total or 0.00
                    result.append(res)
                result[0].update({'total_salary':total_salary + overtime_pay['overtime_pay'] or 0.00})
                return result
        salary = _get_salary(order)
        return salary

    def _get_payslip_lines_for_cpf_employer(self, order):
        result = []

        def _get_payslip_cpf_employer(object):
            payslip_line_obj = self.pool.get('hr.payslip.line')
            payslip_line_id = payslip_line_obj.search(self.cr, self.uid,[('id','in',object.line_ids.ids),('category_id.code','=','CAT_CPF_EMPLOYER')]) 
            payslip_line_ids = payslip_line_obj.browse(self.cr, self.uid,payslip_line_id)
            total_cpf_employer = 0.00
            if payslip_line_ids:
                for line in payslip_line_ids:
                    res = {}
                    total_cpf_employer += line.total
                    res['code'] = line.code or ''
                    res['amount'] = line.total or 0.00
                    result.append(res)
                result[0].update({'total_cpf_employer':total_cpf_employer})
                return result
        cpf_employer = _get_payslip_cpf_employer(order)
        return cpf_employer

    def _get_total_hours(self, payslip):
        res = {}
        contract_obj = self.pool.get('hr.contract')
        resource_obj = self.pool.get('resource.calendar')
        timesheet_obj = self.pool.get('hr.analytic.timesheet')
        total_timesheet_hours = 0.0
        if payslip.employee_id.user_id:
            timesheet_search_ids = timesheet_obj.search(self.cr, self.uid, [('user_id', '=', payslip.employee_id.user_id.id), 
                                           ('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to)])
            if timesheet_search_ids:
                for timesheet in timesheet_obj.browse(self.cr, self.uid, timesheet_search_ids):
                    total_timesheet_hours = total_timesheet_hours + timesheet.unit_amount or 0.0

        total_hours = 0.0
        if payslip.contract_id:
            contact_brw = contract_obj.browse(self.cr, self.uid, payslip.contract_id.id)
            if contact_brw.working_hours:
                total_hours = resource_obj.get_working_hours(self.cr, self.uid, contact_brw.working_hours.id, 
                             start_dt=datetime.strptime(payslip.date_from, '%Y-%m-%d'), 
                             end_dt=datetime.strptime(payslip.date_to, '%Y-%m-%d'), 
                             compute_leaves=True, resource_id=None, default_interval=None, context= None)

        total_overtime = 0.00
        overtime_pay = 0.00
        if total_timesheet_hours > total_hours:
            total_overtime = total_timesheet_hours - total_hours
        if total_overtime:
            overtime_pay = payslip.contract_id.overtime_pay * total_overtime

        res.update({
                    'total_timesheet_hours':total_timesheet_hours,
                    'total_hours': total_hours,
                    'overtime_hours': total_overtime,
                    'overtime_pay': overtime_pay
        })
        return res

    def _get_payslip_net_pay(self, order):
        dict = {}
        total_net_pay = 0.00
        salarys_amount = 0.00
        allowances_amount = 0.00
        deduction_amount = 0.00
        other_payment_amount = 0.00
        salarys = self._get_payslip_lines_salary(order)
        allowances = self._get_payslip_lines_allowance(order)
        deduction = self._get_payslip_lines_deductions(order)
        other_payment = self._get_payslip_lines_other_additional_payment(order)
        if salarys:
            salarys_amount = salarys[0]['total_salary'] or 0.00
        if allowances:
            allowances_amount = allowances[0]['total_allowance'] or 0.00
        if deduction:
            deduction_amount = deduction[0]['total_deductions'] or 0.00
        if other_payment:
            other_payment_amount = other_payment[0]['total_additional_payment']
        total_net_pay = salarys_amount + allowances_amount - deduction_amount + other_payment_amount
        dict.update({
                'total_net_pay': total_net_pay or 0.00,
                })
        return dict

class report_hr_payslip_details(models.AbstractModel):
    _name = 'report.shockheng_hr_payroll_report_modify.custom_hr_payslip_report'
    _inherit = 'report.abstract_report'
    _template = 'shockheng_hr_payroll_report_modify.custom_hr_payslip_report'
    _wrapped_report_class = hr_payslip_details_report