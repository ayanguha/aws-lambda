from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import DataBase
# an Engine, which the Session will use for connection
# resources

PDB1250_Testing_engine = DataBase.db.engine;
# create a configured "Session" class
Session = sessionmaker(bind=PDB1250_Testing_engine);
# create a Session
session = Session()

session.execute("""
--# Trigger for portal administrator to insert Auto generated alpha numeric ID
CREATE OR REPLACE FUNCTION public.fnPortalAdministrator()
RETURNS trigger AS
$BODY$
BEGIN NEW."PortalAdminID" := (select TO_CHAR(nextval('portaladmin_seq_autoid'::regclass),'"1xP"fm000000'));
RETURN NEW; 
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER TrgPortalAdministrator  
BEFORE INSERT ON portaladministrator
FOR EACH ROW
EXECUTE PROCEDURE fnportaladministrator();


-- Trigger for OrganisationAccount to insert Auto generated alpha numeric ID
CREATE OR REPLACE FUNCTION fnOrganisationAccount()
RETURNS trigger AS
$BODY$
BEGIN
NEW."AccountID" := (select TO_CHAR(nextval('account_seq_autoid'::regclass),'"1xA"fm000000'));
RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER TrgOrganisationAccount
BEFORE INSERT ON public.Organisationaccount
FOR EACH ROW
EXECUTE PROCEDURE fnOrganisationAccount();


-- Trigger for OrganisationAccount to insert Auto generated alpha numeric ID
CREATE OR REPLACE FUNCTION fnOrganisationAdministrator()
RETURNS trigger AS
$BODY$
BEGIN
NEW."OrgAdminID" := (select TO_CHAR(nextval('orgadmin_seq_autoid'::regclass),'"1OA"fm000000'));
RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER TrgOrganisationAdministrator
BEFORE INSERT ON public.Organisationadministrator
FOR EACH ROW
EXECUTE PROCEDURE fnOrganisationAdministrator();

--# Trigger for License to insert Auto generated alpha numeric ID
CREATE OR REPLACE FUNCTION fnLicenseOrder()
RETURNS trigger AS
$BODY$
BEGIN
NEW."LicenseOrderID" := (select TO_CHAR(nextval('licenses_seq_autoid'::regclass),'"1xL"fm000000'));
RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER TrgLicenseOrder
BEFORE INSERT ON public.Licenseorder
FOR EACH ROW
EXECUTE PROCEDURE fnLicenseOrder();

--# Trigger for Users to insert Auto generated alpha numeric ID
CREATE OR REPLACE FUNCTION fnUSERS()
RETURNS trigger AS
$BODY$
BEGIN
NEW."UserID" := (select TO_CHAR(nextval('user_seq_autoid'::regclass),'"1xU"fm000000'));
RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER TrgUSERS
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE PROCEDURE fnUSERS();

""")
session.commit()