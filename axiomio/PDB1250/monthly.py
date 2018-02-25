
from api.database.models import *
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
import sqlalchemy

db = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI)

def createAccountBillingRecords(event, context):
    sqlstmt = text('''
                   INSERT INTO "AccountBilling" ("accountId", "billingAmount","billingDate")


                       SELECT "accountId",
                              SUM("totalUsers" * "userCost") "billingAmount",
                              current_timestamp
                        from "AccountUsage"  au cross join "BillingTiers" bt
                         where "activeUsers" between "userLowerLimit" and  "userUpperLimit"
                           and "usageDate" >= date_trunc('month',date_trunc('month', now()) - interval '1 day')
                           and "usageDate" < date_trunc('month', now())
                         group by "accountId"
                          ''')

    try:
        result = db.engine.execute(sqlstmt)
        return "Success"
    except:
        raise
