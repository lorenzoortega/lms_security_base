from odoo import models, _
from odoo.exceptions import UserError, AccessError


class LMSSecurityMixin(models.AbstractModel):
    _name = 'lms.security.mixin'
    _description = 'LMS Security Mixin'

    def _check_group_or_raise(self, group_xmlid, message=None, error_type='user'):
        """
        Valida que el usuario actual pertenezca al grupo indicado.
        Si no pertenece, lanza UserError o AccessError.
        """
        if not self.env.user.has_group(group_xmlid):
            msg = message or _("No tienes permisos para realizar esta accion.")
            if error_type == 'access':
                raise AccessError(msg)
            raise UserError(msg)
        return True

    def _check_any_group_or_raise(self, group_xmlids, message=None, error_type='user'):
        """
        Valida que el usuario pertenezca a al menos uno de los grupos indicados.
        """
        if not any(self.env.user.has_group(group_xmlid) for group_xmlid in group_xmlids):
            msg = message or _("No tienes permisos para realizar esta accion.")
            if error_type == 'access':
                raise AccessError(msg)
            raise UserError(msg)
        return True

    def _check_all_groups_or_raise(self, group_xmlids, message=None, error_type='user'):
        """
        Valida que el usuario pertenezca a todos los grupos indicados.
        """
        if not all(self.env.user.has_group(group_xmlid) for group_xmlid in group_xmlids):
            msg = message or _("No tienes permisos para realizar esta accion.")
            if error_type == 'access':
                raise AccessError(msg)
            raise UserError(msg)
        return True