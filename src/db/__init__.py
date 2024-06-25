"""
Import all the models, so that Base has them before being
imported by Alembic. Also, we account for
SQLAlchemy mapper error when seeding the database.
See more at https://stackoverflow.com/a/46349722 and https://stackoverflow.com/a/71751680
"""
import src.modules.todo_categories.models  # noqa: F401
