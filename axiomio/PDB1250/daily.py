
from database.models import *
from flask import Response
from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime
from sqlalchemy import and_, or_, not_,text
import calendar
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import *
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
import settings

db = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)

def createAccountUsageRecords(event, context):
    sqlstmt = text('''
                   INSERT INTO "AccountUsage" ("accountId", "totalUsers","activeUsers","usageDate")
                       SELECT "accountId",
                              count("Users"."userId") "totalUsers",
                              sum(case when "userStatus"='ACTIVATED' then 1 else 0 end) "activeUsers",
                              current_timestamp "usageDate"
                        from "Users"
                        group by "accountId"
                          ''')

    try:
        result = db.engine.execute(sqlstmt)
        return "Success"
    except:
        raise
