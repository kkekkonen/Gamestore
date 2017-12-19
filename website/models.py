from django.db import models

class RightsSupport(models.Model):

    class Meta:

        managed = False  # No database table creation or deletion operations \
                         # will be performed for this model.

        permissions = (
            ('developer_rights', 'developers can add games'),
            ('admin_rights', 'admins cannot do anything yet'),
            ('no_rights', ' '),
        )
