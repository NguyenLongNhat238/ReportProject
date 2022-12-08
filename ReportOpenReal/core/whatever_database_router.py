# whatever_database_router.py
class WhateverDatabaseRouter:  # tên tuổi méo quan trọng, dễ hiểu là được
    # với request đọc
    route_app_labels = {'report','property'}

    def db_for_read(self, model, **hint):
        # nếu nó được gắn mác 'report', thì gọi đến database 'report'
        if model._meta.app_label == 'report':
            return 'report'

        # nếu nó được gắn mác 'admin', thì gọi đến database 'admin'
        # if model._meta.app_label == 'app1':
        return 'default'

        # nếu nó không có mác, gọi đến database 'default'
        # return None

    # với request ghi
    def db_for_write(self, model, **hint):
        return 'default'

    # với request migrate
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        # if app_label in self.route_app_labels:
        #     return db == 'auth_db'
        return 'default'

    # với request check quan hệ
    def allow_relation(self, obj1, obj2, **hints):
        # nếu nó được gắn mác 'cars', thì gọi đến database 'cars'
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None
