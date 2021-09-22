import django.db.backends.mysql.base as mysql_base
from django.db.backends.mysql.base import DatabaseWrapper as MysqlDatabaseWrapper
from django.db.backends.mysql.schema import DatabaseSchemaEditor

from .pool import Database

mysql_base.Database = Database


class MysqlSchemaEditor(DatabaseSchemaEditor):
    # by wangsheng
    sql_alter_column_comment = (
        "ALTER TABLE %(table)s MODIFY COLUMN %(field)s %(changes)s"
    )

    def _column_comment_sql(self, model, field, include_default=False):
        sql, params = super().column_sql(model, field, include_default)
        if sql and field.verbose_name:
            sql += " COMMENT %s"
            params.append(field.verbose_name)
        return sql, params

    def column_sql(self, model, field, include_default=False):
        """
        原生orm不会根据verbose_name去生成字段的comment注释信息
        这里改一改，增加了comment注释
        """
        sql, params = self._column_comment_sql(model, field, include_default)
        return sql, params

    def _alter_field(
        self,
        model,
        old_field,
        new_field,
        old_type,
        new_type,
        old_db_params,
        new_db_params,
        strict=False,
    ):
        """
        修改注释也是个麻烦事，没有单独修改这个属性的，只能modify，
        暂时只能这样，后续要是添加了这个功能，该处代码优化优化
        """
        super()._alter_field(
            model,
            old_field,
            new_field,
            old_type,
            new_type,
            old_db_params,
            new_db_params,
            strict,
        )
        if old_field.verbose_name == new_field.verbose_name:
            return

        sql, params = self._column_comment_sql(model, new_field, True)
        if not sql:
            return
        self.execute(
            self.sql_alter_column_comment
            % {
                "table": self.quote_name(model._meta.db_table),
                "field": self.quote_name(new_field.column),
                "changes": sql,
            },
            params,
        )


class DatabaseWrapper(MysqlDatabaseWrapper):
    SchemaEditorClass = MysqlSchemaEditor

    def get_connection_params(self):
        kwargs = super().get_connection_params()
        kwargs["POOL"] = self.settings_dict.get("POOL", {})
        return kwargs
