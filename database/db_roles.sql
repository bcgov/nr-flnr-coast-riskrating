CREATE USER PROXY_USER;

CREATE ROLE TMBR_PRICING_SCRPT_ROLE;

GRANT TMBR_PRICING_SCRPT_ROLE TO PROXY_USER;

GRANT SELECT ON
APPRAISAL_DATA_SUBMISSION
TO THE.TMBR_PRICING_SCRPT;

GRANT SELECT ON
APPRAISAL_DATA_SUBMISSION_CTRL
TO THE.TMBR_PRICING_SCRPT;

GRANT SELECT ON
ORG_UNIT
TO THE.TMBR_PRICING_SCRPT;

GRANT SELECT ON
ORG_UNIT
TO THE.ADS_SUBMITTED_TIMBER_MARK;

GRANT SELECT ON
ORG_UNIT
TO THE.V_CLIENT_PUBLIC;

GRANT SELECT ON
ORG_UNIT
TO THE.RPF_LICENSEE_REP;

GRANT SELECT ON
ORG_UNIT
TO THE.ADS_BRIDGE;

GRANT SELECT ON
ORG_UNIT
TO THE.ADS_CULVERT;

GRANT SELECT ON
ORG_UNIT
TO THE.ADS_DETAILED_ENGINEERING_COST;

GRANT SELECT ON
ORG_UNIT
TO THE.ADS_TABULAR_ROAD_SECTION;

GRANT SELECT ON
ORG_UNIT
TO THE.ADS_SPECIFIED_OPERATION;









