import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def lms_pos_has_price_change_authorization_group(self):
        """
        Indica si el usuario pertenece al grupo que puede autorizar
        cambios de precio en POS.
        """
        self.ensure_one()
        return self.has_group(
            "lms_security_base.group_lms_pos_price_change_authorizer"
        )

    def lms_pos_has_price_change_free_group(self):
        """
        Indica si el usuario puede cambiar precios en POS sin autorización.
        """
        self.ensure_one()
        return self.has_group(
            "lms_security_base.group_lms_pos_price_change_free"
        )

    def lms_pos_can_refund(self):
        """
        Indica si el usuario puede realizar reembolsos desde POS.
        """
        self.ensure_one()
        return self.has_group("lms_security_base.group_lms_pos_refund")

    def lms_pos_can_cancel_order(self):
        """
        Indica si el usuario puede cancelar órdenes desde POS.
        """
        self.ensure_one()
        return self.has_group("lms_security_base.group_lms_pos_cancel_order")

    def lms_pos_can_delete_order(self):
        """
        Indica si el usuario puede borrar/eliminar órdenes desde POS.
        """
        self.ensure_one()
        return self.has_group("lms_security_base.group_lms_pos_delete_order")

    def lms_pos_security_permissions(self):
        """
        Devuelve un paquete simple de permisos LMS para ser consumido
        por módulos POS en frontend/backend.

        Este método no bloquea acciones por sí solo; solo centraliza
        la lectura de permisos.
        """
        self.ensure_one()
        return {
            "is_lms_cashier": self.has_group("lms_security_base.group_lms_cashier"),
            "is_lms_supervisor": self.has_group("lms_security_base.group_lms_supervisor"),
            "is_lms_manager": self.has_group("lms_security_base.group_lms_manager"),
            "can_open_session": self.has_group("lms_security_base.group_lms_pos_open_session"),
            "can_close_session": self.has_group("lms_security_base.group_lms_pos_close_session"),
            "can_refund": self.lms_pos_can_refund(),
            "can_cancel_order": self.lms_pos_can_cancel_order(),
            "can_delete_order": self.lms_pos_can_delete_order(),
            "can_authorize_price_change": self.lms_pos_has_price_change_authorization_group(),
            "can_change_price_free": self.lms_pos_has_price_change_free_group(),
        }

    def lms_pos_validate_totp_code(self, totp_code):
        """
        Valida el código 2FA/TOTP del usuario.

        Usa el mecanismo nativo de Odoo cuando el módulo auth_totp
        está instalado.

        Retorna:
            True  -> código válido
            False -> código inválido o usuario sin 2FA configurado
        """
        self.ensure_one()

        if not totp_code:
            return False

        clean_code = str(totp_code).strip().replace(" ", "")

        if not clean_code.isdigit() or len(clean_code) != 6:
            return False

        try:
            # En Odoo con auth_totp, res.users dispone normalmente
            # de un método interno para validar el código TOTP.
            if hasattr(self, "_totp_check"):
                return bool(self.sudo()._totp_check(clean_code))

            _logger.warning(
                "LMS POS Price Control: el método _totp_check no está disponible para validar 2FA."
            )
            return False

        except Exception as error:
            _logger.warning(
                "LMS POS Price Control: error validando código TOTP para usuario %s: %s",
                self.id,
                error,
            )
            return False
