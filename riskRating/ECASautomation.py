#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os, os.path
import win32com.client as win32
import pandas as pd
import constants
import cx_Oracle


# In[2]:


# setup ODBC connection

tns_name = constants.ORACLE_TNS_NAME
username = constants.ORACLE_USERNAME
password = constants.ORACLE_PASSWORD
connection = cx_Oracle.connect(user=username, password=password, dsn=tns_name, encoding="UTF-8")
cursor = connection.cursor()


# In[3]:


# SQL query

query = pd.read_sql_query('''
SELECT 

APPRAISAL_DATA_SUBMISSION.ECAS_ID,
APPRAISAL_DATA_SUBMISSION.UPDATE_TIMESTAMP,
APPRAISAL_DATA_SUBMISSION.CUTTING_PERMIT_ID,
APPRAISAL_DATA_SUBMISSION.FOREST_FILE_ID,
APPRAISAL_DATA_SUBMISSION.SECOND_GROWTH_IND,
APPRAISAL_DATA_SUBMISSION.NET_CRUISE_VOLUME,
APPRAISAL_DATA_SUBMISSION.SINGLE_STEM_VOLUME,
APPRAISAL_DATA_SUBMISSION.DISTRICT_RECEIVED_DATE,
APPRAISAL_DATA_SUBMISSION.TSB_NUMBER_CODE,
APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE,
APPRAISAL_DATA_SUBMISSION.APPRAISAL_EFFECTIVE_DATE,
APPRAISAL_DATA_SUBMISSION.RPF_SUBMITTED_DATE,
APPRAISAL_DATA_SUBMISSION.SENT_BY_USER_ID,
APPRAISAL_DATA_SUBMISSION.SENT_DATE,
APPRAISAL_DATA_SUBMISSION.ROAD_USE_CHARGE,
APPRAISAL_DATA_SUBMISSION.GROUND_SYSTEMS_VOLUME,
APPRAISAL_DATA_SUBMISSION.HELI_WATER_DROP_VOLUME,
APPRAISAL_DATA_SUBMISSION.CP_CRUISE_CHECKED_IND,
APPRAISAL_DATA_SUBMISSION.CLIENT_NUMBER,
APPRAISAL_DATA_SUBMISSION.RPF_USER_ID,
APPRAISAL_DATA_SUBMISSION.TRANSFER_BY_USER_ID,
APPRAISAL_DATA_SUBMISSION.TRANSFER_DATE,
APPRAISAL_DATA_SUBMISSION.CP_AVG_VOL_PER_HA,
APPRAISAL_DATA_SUBMISSION.AVERAGE_SIDE_SLOPE_PCT,
APPRAISAL_DATA_SUBMISSION.ISOLATION_TYPE_CODE,
APPRAISAL_DATA_SUBMISSION.DATA_FIELD_CHECKED_IND,
APPRAISAL_DATA_SUBMISSION.CABLE_YARDING_VOLUME,

ADS_SUBMITTED_TIMBER_MARK.TIMBER_MARK,

ORG_UNIT.ORG_UNIT_CODE,

v_client_public.client_name,

RPF_LICENSEE_REP.MEMBER_NUMBER,
RPF_LICENSEE_REP.RPF_IND,
RPF_LICENSEE_REP.RFT_IND,

nvl(roads.road_cost,0) as "Road List.Total Cost",
nvl(bridges.bridge_cost,0) as "Bridge List.Total Cost",
nvl(culverts.culvert_cost,0) as "Culvert List.Total Cost",
nvl(ndc.ndcunknown , 0) as "NDC List.",
nvl(ndc.ndctype1 , 0) as "NDC List.1",
nvl(ndc.ndctype2 , 0) as "NDC List.2",
nvl(ndc.NDCTYPE3 , 0) as "NDC List.3",
nvl(ndc.ndctype4 , 0) as "NDC List.4",
nvl(ndc.ndctype5 , 0) as "NDC List.5",
nvl(ndc.ndctype6 , 0) as "NDC List.6",
nvl(ndc.ndctype7 , 0) as "NDC List.7",
nvl(ndc.ndctype8 , 0) as "NDC List.8",
nvl(ndc.ndctype9 , 0) as "NDC List.9",
nvl(ndc.ndctype10 , 0) as "NDC List.10",
nvl(ndc.ndctype11 , 0) as "NDC List.11",
nvl(ndc.ndctype12 , 0) as "NDC List.12",
nvl(ndc.ndctype13 , 0) as "NDC List.13",
nvl(ndc.ndctype14 , 0) as "NDC List.14",
nvl(ndc.ndctype15 , 0) as "NDC List.15",
(nvl(ndc.ndcunknown,0) +nvl(ndc.ndctype1,0) +nvl(ndc.ndctype2,0) +nvl(ndc.ndctype3,0) +nvl(ndc.ndctype4,0) +nvl(ndc.ndctype5,0) +nvl(ndc.ndctype6,0) +nvl(ndc.ndctype7,0) +nvl(ndc.ndctype8,0) +nvl(ndc.ndctype9,0) +nvl(ndc.ndctype10,0) +nvl(ndc.ndctype11,0) +nvl(ndc.ndctype12,0) +nvl(ndc.ndctype13,0) +nvl(ndc.ndctype14,0) +nvl(ndc.ndctype15,0)) as "NDC List.Total Cost",
nvl(soa.ebm , 0) as "SOA List.Eco-System Based Management Operating Costs",
nvl(soa.tcm , 0) as "SOA List.Tree Crown Modification",
nvl(soa.bg , 0) as "SOA List.Barging Transportation",
nvl(soa.sl , 0) as "SOA List.Skyline Logging",
nvl(soa.iw , 0) as "SOA List.Inland Water Transportation",
nvl(soa.cs , 0) as "SOA List.Clayoquot Sound Operating Costs",
nvl(soa.hdc , 0) as "SOA List.High Development Cost",
(nvl(soa.ebm,0) + nvl(soa.tcm,0) + nvl(soa.bg,0) + nvl(soa.sl,0) + nvl(soa.iw,0) + nvl(soa.cs,0) + nvl(soa.hdc,0)) as "SOA List.SOA Total",
nvl(soa.frz, 0) as "SOA List.FRZ"


FROM 
THE.APPRAISAL_DATA_SUBMISSION
inner join THE.APPRAISAL_DATA_SUBMISSION_CTRL ON (APPRAISAL_DATA_SUBMISSION_CTRL.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID) 
left outer join THE.ORG_UNIT ON (ORG_UNIT.ORG_UNIT_NO = APPRAISAL_DATA_SUBMISSION.ADMIN_DISTRICT) 
left outer join THE.ADS_SUBMITTED_TIMBER_MARK ON (ADS_SUBMITTED_TIMBER_MARK.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID)
left outer join THE.v_client_public ON (v_client_public.client_number = APPRAISAL_DATA_SUBMISSION.client_number)
left outer join THE.RPF_LICENSEE_REP ON (RPF_LICENSEE_REP.USER_ID = APPRAISAL_DATA_SUBMISSION.RPF_USER_ID) AND (RPF_LICENSEE_REP.CLIENT_NUMBER = APPRAISAL_DATA_SUBMISSION.client_number) AND (RPF_LICENSEE_REP.CLIENT_LOCN_CODE = APPRAISAL_DATA_SUBMISSION.CLIENT_LOCN_CODE)

left outer join (
    SELECT
    ads_bridge.ecas_id,
    SUM(cost_estimate * 1000) as bridge_cost

    FROM ads_bridge
    inner join appraisal_data_submission on ads_bridge.ecas_id = appraisal_data_submission.ecas_id
    /*inner join appraisal_data_submission_ctrl on (APPRAISAL_DATA_SUBMISSION_CTRL.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID)*/
    inner join (
        SELECT 
        bc1.effective_date AS start_date,
        COALESCE(bc2.effective_date, SYSDATE + 1) AS end_date,
        bc1.bridge_type_code,
        bc1.span_length,
        bc1.crib_height,
        bc1.cost_estimate
        FROM bridge_cost bc1
        LEFT JOIN bridge_cost bc2 ON bc2.effective_date > bc1.effective_date AND bc1.bridge_type_code = bc2.bridge_type_code AND bc1.span_length = bc2.span_length AND bc1.crib_height = bc2.crib_height AND bc1.appraisal_method_code = bc2.appraisal_method_code
        LEFT JOIN bridge_cost bc3 ON bc3.effective_date > bc1.effective_date AND bc2.effective_date > bc3.effective_date AND bc3.bridge_type_code = bc2.bridge_type_code AND bc3.span_length = bc2.span_length AND bc3.crib_height = bc2.crib_height AND bc2.appraisal_method_code = bc3.appraisal_method_code
        WHERE bc1.appraisal_method_code = 'C'
        AND bc3.effective_date is null
    ) bridge_costs on appraisal_effective_date >= start_date and appraisal_effective_date < end_date and ads_bridge.bridge_type_code = bridge_costs.bridge_type_code and ads_bridge.crib_height = bridge_costs.crib_height and ads_bridge.span_length = bridge_costs.span_length
    /*WHERE
    (APPRAISAL_DATA_SUBMISSION_CTRL.APPRAISAL_METHOD_CODE = 'C') 
    AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE = 'P')*/
    GROUP BY ads_bridge.ecas_id
) bridges on bridges.ecas_id = appraisal_data_submission.ecas_id
left outer join (
    SELECT 
    ads_culvert.ecas_id,
    SUM(CASE
        WHEN ads_culvert.appraisal_culvert_type_code = 'M' THEN ads_culvert.total_culvert_length * culverts.cost_estimate
        ELSE ads_culvert.quantity_used * ads_culvert.UNIT_COST_PER_METER
    END) AS culvert_cost

    FROM ads_culvert
    inner join appraisal_data_submission on ads_culvert.ecas_id = appraisal_data_submission.ecas_id
    /*inner join appraisal_data_submission_ctrl on (APPRAISAL_DATA_SUBMISSION_CTRL.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID)*/
    left outer join (
        select 
        cc1.effective_date as START_DATE,
        COALESCE(cc2.effective_date, SYSDATE + 1) as END_DATE,
        cc1.culvert_diameter,
        cc1.cost_estimate
        from culvert_cost cc1
        left join culvert_cost cc2 on cc2.effective_date > cc1.effective_date AND cc2.culvert_diameter = cc1.culvert_diameter AND cc1.appraisal_method_code = cc2.appraisal_method_code
        LEFT JOIN culvert_cost cc3 ON cc3.effective_date > cc1.effective_date AND cc2.effective_date > cc3.effective_date AND cc3.culvert_diameter = cc2.culvert_diameter AND cc2.appraisal_method_code = cc3.appraisal_method_code
        where cc1.appraisal_method_code = 'C'
        and cc3.effective_date is null
    ) culverts on appraisal_data_submission.appraisal_effective_date >= culverts.START_DATE and appraisal_data_submission.appraisal_effective_date < culverts.END_DATE and ads_culvert.culvert_diameter = culverts.culvert_diameter
    /*WHERE
    (APPRAISAL_DATA_SUBMISSION_CTRL.APPRAISAL_METHOD_CODE = 'C') 
    AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE = 'P')*/
    GROUP BY ads_culvert.ecas_id
) culverts on appraisal_data_submission.ecas_id = culverts.ecas_id
left outer join (
    SELECT 
    ads_tabular_road_section.ecas_id,
    SUM(ads_tabular_road_section.section_length * road_costs.cost_estimate) AS road_cost
    FROM ads_tabular_road_section
    /*inner join appraisal_data_submission_ctrl on appraisal_data_submission_ctrl.ecas_id = ads_tabular_road_section.ecas_id*/
    inner join appraisal_data_submission on ads_tabular_road_section.ecas_id = appraisal_data_submission.ecas_id
    inner join (
        SELECT 
        bhrc1.effective_date as start_date,
        coalesce(bhrc2.effective_date, sysdate+1) as end_date,
        bhrc1.bank_height_category_code,
        bhrc1.rock_mass_class_code,
        bhrc1.cost_estimate
        FROM bank_height_road_cost bhrc1
        LEFT JOIN bank_height_road_cost bhrc2 ON bhrc2.effective_date > bhrc1.effective_date AND bhrc1.bank_height_category_code = bhrc2.bank_height_category_code AND bhrc1.rock_mass_class_code = bhrc2.rock_mass_class_code
        LEFT JOIN bank_height_road_cost bhrc3 ON bhrc3.effective_date > bhrc1.effective_date AND bhrc2.effective_date > bhrc3.effective_date AND bhrc3.bank_height_category_code = bhrc2.bank_height_category_code AND bhrc3.rock_mass_class_code = bhrc2.rock_mass_class_code
        WHERE bhrc3.effective_date is null
    ) road_costs on appraisal_data_submission.appraisal_effective_date >= road_costs.start_date and appraisal_data_submission.appraisal_effective_date < road_costs.end_date and ads_tabular_road_section.bank_height_category_code = road_costs.bank_height_category_code and ads_tabular_road_section.subgrade_rmc_code = road_costs.rock_mass_class_code
    /*WHERE appraisal_method_code = 'C'
    AND appraisal_category_code = 'P'*/
    GROUP BY ads_tabular_road_section.ecas_id
) roads on roads.ecas_id = appraisal_data_submission.ecas_id
left outer join (
    SELECT 
    *
    FROM (
        SELECT 
        ADEC.ECAS_ID,
        NVL(ADS_NON_TABULAR_DEV_TYPE_CODE, 0) AS ADS_NON_TABULAR_DEV_TYPE_CODE,
        SUM(TOTAL_COST) AS TOTAL_COST
        FROM ads_detailed_engineering_cost adec
        inner join appraisal_data_submission ads on ads.ecas_id = adec.ecas_id
        inner join appraisal_data_submission_ctrl adsc on adec.ecas_id = adsc.ecas_id
        group by adec.ecas_id, adec.ADS_NON_TABULAR_DEV_TYPE_CODE
    )
    PIVOT (
        SUM(TOTAL_COST) 
        FOR ADS_NON_TABULAR_DEV_TYPE_CODE IN (
            '0' AS NDCUNKNOWN, 
            '1' AS NDCTYPE1, 
            '2' AS NDCTYPE2, 
            '3' AS NDCTYPE3, 
            '4' AS NDCTYPE4, 
            '5' AS NDCTYPE5,
            '6' AS NDCTYPE6, 
            '7' AS NDCTYPE7, 
            '8' AS NDCTYPE8, 
            '9' AS NDCTYPE9, 
            '10' AS NDCTYPE10, 
            '11' AS NDCTYPE11, 
            '12' AS NDCTYPE12, 
            '13' AS NDCTYPE13, 
            '14' AS NDCTYPE14, 
            '15' AS NDCTYPE15
        )
    )
) ndc on ndc.ecas_id = appraisal_data_submission.ecas_id
left outer join (
    SELECT * FROM(
        SELECT
        ads_specified_operation.ECAS_ID,
        NVL(SPECIFIED_OPERATIONS_CODE, 0) AS SPECIFIED_OPERATIONS_CODE,
        SPECIFIED_OPERATING_RATE
        FROM ads_specified_operation
        inner join appraisal_data_submission on ads_specified_operation.ecas_id = appraisal_data_submission.ecas_id
        inner join appraisal_data_submission_ctrl adsc on (adsc.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID)
        WHERE APPRAISAL_DATA_SUBMISSION.appraisal_category_code = 'P'
            AND adsc.appraisal_method_code = 'C'
    )
    PIVOT (SUM(SPECIFIED_OPERATING_RATE) FOR SPECIFIED_OPERATIONS_CODE IN (
    'EBM' AS EBM, 
        'TCM' AS TCM, 
        'BG' AS BG, 
        'FRZ' AS FRZ, 
        'SL' AS SL, 
        'IW' AS IW, 
        'CS' AS CS, 
        'HDC' AS HDC))
) soa on appraisal_data_submission.ecas_id = soa.ecas_id

WHERE
-- Conditions
(APPRAISAL_DATA_SUBMISSION_CTRL.APPRAISAL_METHOD_CODE = 'C') 
AND (ADS_SUBMITTED_TIMBER_MARK.PRIMARY_MARK_IND = 'Y')
AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE = 'P')
AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_STATUS_CODE = 'RCD')
ORDER BY 
APPRAISAL_DATA_SUBMISSION.ECAS_ID DESC
''', connection
)


# In[4]:


rootPath = constants.DATA_PATH
filePath = os.path.join(rootPath, 'received.csv')
new_received = pd.DataFrame(query)
new_received.to_csv(filePath, mode='a', index=False, header=False)


# In[5]:


df = pd.read_csv(filePath)
df = df.sort_values(['ECAS_ID', 'UPDATE_TIMESTAMP']).drop_duplicates(subset=['ECAS_ID'], keep='first')
df.to_csv(filePath, index=False)


# In[6]:


query = pd.read_sql_query('''

SELECT 

APPRAISAL_DATA_SUBMISSION.ECAS_ID,
APPRAISAL_DATA_SUBMISSION.UPDATE_TIMESTAMP,
APPRAISAL_DATA_SUBMISSION.CUTTING_PERMIT_ID,
APPRAISAL_DATA_SUBMISSION.FOREST_FILE_ID,
APPRAISAL_DATA_SUBMISSION.SECOND_GROWTH_IND,
APPRAISAL_DATA_SUBMISSION.NET_CRUISE_VOLUME,
APPRAISAL_DATA_SUBMISSION.SINGLE_STEM_VOLUME,
APPRAISAL_DATA_SUBMISSION.DISTRICT_RECEIVED_DATE,
APPRAISAL_DATA_SUBMISSION.TSB_NUMBER_CODE,
APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE,
APPRAISAL_DATA_SUBMISSION.APPRAISAL_EFFECTIVE_DATE,
APPRAISAL_DATA_SUBMISSION.DATA_OFFICE_CHECKED_IND,
APPRAISAL_DATA_SUBMISSION.DATA_FIELD_CHECKED_IND,
APPRAISAL_DATA_SUBMISSION.NUMBER_OF_ISSUES,
APPRAISAL_DATA_SUBMISSION.RPF_SUBMITTED_DATE,
APPRAISAL_DATA_SUBMISSION.SENT_BY_USER_ID,
APPRAISAL_DATA_SUBMISSION.SENT_DATE,
APPRAISAL_DATA_SUBMISSION.ROAD_USE_CHARGE,
APPRAISAL_DATA_SUBMISSION.GROUND_SYSTEMS_VOLUME,
APPRAISAL_DATA_SUBMISSION.HELI_WATER_DROP_VOLUME,
APPRAISAL_DATA_SUBMISSION.CP_CRUISE_CHECKED_IND,
APPRAISAL_DATA_SUBMISSION.CLIENT_NUMBER,
APPRAISAL_DATA_SUBMISSION.RPF_USER_ID,
APPRAISAL_DATA_SUBMISSION.TRANSFER_BY_USER_ID,
APPRAISAL_DATA_SUBMISSION.TRANSFER_DATE,
APPRAISAL_DATA_SUBMISSION.CP_AVG_VOL_PER_HA,
APPRAISAL_DATA_SUBMISSION.AVERAGE_SIDE_SLOPE_PCT,
APPRAISAL_DATA_SUBMISSION.ISOLATION_TYPE_CODE,
APPRAISAL_DATA_SUBMISSION.DATA_FIELD_CHECKED_IND,
APPRAISAL_DATA_SUBMISSION.ROAD_USE_CHARGE,
APPRAISAL_DATA_SUBMISSION.CABLE_YARDING_VOLUME,

ADS_SUBMITTED_TIMBER_MARK.TIMBER_MARK,

ORG_UNIT.ORG_UNIT_CODE,

v_client_public.client_name,

RPF_LICENSEE_REP.MEMBER_NUMBER,
RPF_LICENSEE_REP.RPF_IND,
RPF_LICENSEE_REP.RFT_IND,

APPRAISED_STUMPAGE_RATE.STUMPAGE_RATE_EFFECTIVE_DATE,
SRS1.SUBTOTAL_VALUE AS INDICATED_RATE,
SRS2.SUBTOTAL_VALUE AS FEWB,
SRS3.SUBTOTAL_VALUE AS TOA,
APP_STMPG_RATE.TOT_STUMPAGE_RATE,

nvl(roads.road_cost,0) as "Road List.Total Cost",
nvl(bridges.bridge_cost,0) as "Bridge List.Total Cost",
nvl(culverts.culvert_cost,0) as "Culvert List.Total Cost",
nvl(ndc.ndcunknown , 0) as "NDC List.",
nvl(ndc.ndctype1 , 0) as "NDC List.1",
nvl(ndc.ndctype2 , 0) as "NDC List.2",
nvl(ndc.NDCTYPE3 , 0) as "NDC List.3",
nvl(ndc.ndctype4 , 0) as "NDC List.4",
nvl(ndc.ndctype5 , 0) as "NDC List.5",
nvl(ndc.ndctype6 , 0) as "NDC List.6",
nvl(ndc.ndctype7 , 0) as "NDC List.7",
nvl(ndc.ndctype8 , 0) as "NDC List.8",
nvl(ndc.ndctype9 , 0) as "NDC List.9",
nvl(ndc.ndctype10 , 0) as "NDC List.10",
nvl(ndc.ndctype11 , 0) as "NDC List.11",
nvl(ndc.ndctype12 , 0) as "NDC List.12",
nvl(ndc.ndctype13 , 0) as "NDC List.13",
nvl(ndc.ndctype14 , 0) as "NDC List.14",
nvl(ndc.ndctype15 , 0) as "NDC List.15",
(nvl(ndc.ndcunknown,0) +nvl(ndc.ndctype1,0) +nvl(ndc.ndctype2,0) +nvl(ndc.ndctype3,0) +nvl(ndc.ndctype4,0) +nvl(ndc.ndctype5,0) +nvl(ndc.ndctype6,0) +nvl(ndc.ndctype7,0) +nvl(ndc.ndctype8,0) +nvl(ndc.ndctype9,0) +nvl(ndc.ndctype10,0) +nvl(ndc.ndctype11,0) +nvl(ndc.ndctype12,0) +nvl(ndc.ndctype13,0) +nvl(ndc.ndctype14,0) +nvl(ndc.ndctype15,0)) as "NDC List.Total Cost",
nvl(soa.ebm , 0) as "SOA List.Eco-System Based Management Operating Costs",
nvl(soa.tcm , 0) as "SOA List.Tree Crown Modification",
nvl(soa.bg , 0) as "SOA List.Barging Transportation",
nvl(soa.sl , 0) as "SOA List.Skyline Logging",
nvl(soa.iw , 0) as "SOA List.Inland Water Transportation",
nvl(soa.cs , 0) as "SOA List.Clayoquot Sound Operating Costs",
nvl(soa.hdc , 0) as "SOA List.High Development Cost",
(nvl(soa.ebm,0) + nvl(soa.tcm,0) + nvl(soa.bg,0) + nvl(soa.sl,0) + nvl(soa.iw,0) + nvl(soa.cs,0) + nvl(soa.hdc,0)) as "SOA List.SOA Total",
nvl(soa.frz, 0) as "SOA List.FRZ"

FROM
THE.APPRAISAL_DATA_SUBMISSION
INNER JOIN THE.APPRAISAL_DATA_SUBMISSION_CTRL ON APPRAISAL_DATA_SUBMISSION_CTRL.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID
LEFT OUTER JOIN THE.ORG_UNIT ON ORG_UNIT.ORG_UNIT_NO = APPRAISAL_DATA_SUBMISSION.ADMIN_DISTRICT
LEFT OUTER JOIN THE.ADS_SUBMITTED_TIMBER_MARK ON ADS_SUBMITTED_TIMBER_MARK.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID
LEFT OUTER JOIN THE.v_client_public ON v_client_public.client_number = APPRAISAL_DATA_SUBMISSION.client_number
LEFT OUTER JOIN THE.RPF_LICENSEE_REP ON RPF_LICENSEE_REP.USER_ID = APPRAISAL_DATA_SUBMISSION.RPF_USER_ID AND RPF_LICENSEE_REP.CLIENT_NUMBER = APPRAISAL_DATA_SUBMISSION.client_number AND RPF_LICENSEE_REP.CLIENT_LOCN_CODE = APPRAISAL_DATA_SUBMISSION.CLIENT_LOCN_CODE
INNER JOIN THE.APPRAISED_WORKSHEET ON APPRAISED_WORKSHEET.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID
INNER JOIN THE.APPRAISED_STUMPAGE_RATE ON APPRAISED_STUMPAGE_RATE.APPRAISED_WORKSHEET_ID = APPRAISED_WORKSHEET.APPRAISED_WORKSHEET_ID
LEFT OUTER JOIN STUMPAGE_RATE_SUBTOTAL SRS1 ON SRS1.APPRAISED_STUMPAGE_RATE_ID = APPRAISED_STUMPAGE_RATE.APPRAISED_STUMPAGE_RATE_ID
LEFT OUTER JOIN STUMPAGE_RATE_SUBTOTAL SRS2 ON SRS2.APPRAISED_STUMPAGE_RATE_ID = APPRAISED_STUMPAGE_RATE.APPRAISED_STUMPAGE_RATE_ID
LEFT OUTER JOIN STUMPAGE_RATE_SUBTOTAL SRS3 ON SRS3.APPRAISED_STUMPAGE_RATE_ID = APPRAISED_STUMPAGE_RATE.APPRAISED_STUMPAGE_RATE_ID
LEFT OUTER JOIN APP_STMPG_RATE ON APP_STMPG_RATE.TIMBER_MARK = ADS_SUBMITTED_TIMBER_MARK.TIMBER_MARK 
INNER JOIN (
      SELECT AW.ECAS_ID, MIN(ASR.STUMPAGE_RATE_EFFECTIVE_DATE) AS MIN_APPRAISAL_DATE
      FROM APPRAISED_WORKSHEET AW 
      INNER JOIN APPRAISED_STUMPAGE_RATE ASR ON AW.APPRAISED_WORKSHEET_ID = ASR.APPRAISED_WORKSHEET_ID
      GROUP BY AW.ECAS_ID
  ) MIN_DATE ON MIN_DATE.ECAS_ID = APPRAISED_WORKSHEET.ECAS_ID AND MIN_DATE.MIN_APPRAISAL_DATE = APPRAISED_STUMPAGE_RATE.STUMPAGE_RATE_EFFECTIVE_DATE AND APP_STMPG_RATE.STMPG_RTE_EFCTV_DT = MIN_DATE.MIN_APPRAISAL_DATE

left outer join (
    SELECT
    ads_bridge.ecas_id,
    SUM(cost_estimate * 1000) as bridge_cost

    FROM ads_bridge
    inner join appraisal_data_submission on ads_bridge.ecas_id = appraisal_data_submission.ecas_id
    /*inner join appraisal_data_submission_ctrl on (APPRAISAL_DATA_SUBMISSION_CTRL.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID)*/
    inner join (
        SELECT 
        bc1.effective_date AS start_date,
        COALESCE(bc2.effective_date, SYSDATE + 1) AS end_date,
        bc1.bridge_type_code,
        bc1.span_length,
        bc1.crib_height,
        bc1.cost_estimate
        FROM bridge_cost bc1
        LEFT JOIN bridge_cost bc2 ON bc2.effective_date > bc1.effective_date AND bc1.bridge_type_code = bc2.bridge_type_code AND bc1.span_length = bc2.span_length AND bc1.crib_height = bc2.crib_height AND bc1.appraisal_method_code = bc2.appraisal_method_code
        LEFT JOIN bridge_cost bc3 ON bc3.effective_date > bc1.effective_date AND bc2.effective_date > bc3.effective_date AND bc3.bridge_type_code = bc2.bridge_type_code AND bc3.span_length = bc2.span_length AND bc3.crib_height = bc2.crib_height AND bc2.appraisal_method_code = bc3.appraisal_method_code
        WHERE bc1.appraisal_method_code = 'C'
        AND bc3.effective_date is null
    ) bridge_costs on appraisal_effective_date >= start_date and appraisal_effective_date < end_date and ads_bridge.bridge_type_code = bridge_costs.bridge_type_code and ads_bridge.crib_height = bridge_costs.crib_height and ads_bridge.span_length = bridge_costs.span_length
    /*WHERE
    (APPRAISAL_DATA_SUBMISSION_CTRL.APPRAISAL_METHOD_CODE = 'C') 
    AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE = 'P')*/
    GROUP BY ads_bridge.ecas_id
) bridges on bridges.ecas_id = appraisal_data_submission.ecas_id
left outer join (
    SELECT 
    ads_culvert.ecas_id,
    SUM(CASE
        WHEN ads_culvert.appraisal_culvert_type_code = 'M' THEN ads_culvert.total_culvert_length * culverts.cost_estimate
        ELSE ads_culvert.quantity_used * ads_culvert.UNIT_COST_PER_METER
    END) AS culvert_cost

    FROM ads_culvert
    inner join appraisal_data_submission on ads_culvert.ecas_id = appraisal_data_submission.ecas_id
    /*inner join appraisal_data_submission_ctrl on (APPRAISAL_DATA_SUBMISSION_CTRL.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID)*/
    left outer join (
        select 
        cc1.effective_date as START_DATE,
        COALESCE(cc2.effective_date, SYSDATE + 1) as END_DATE,
        cc1.culvert_diameter,
        cc1.cost_estimate
        from culvert_cost cc1
        left join culvert_cost cc2 on cc2.effective_date > cc1.effective_date AND cc2.culvert_diameter = cc1.culvert_diameter AND cc1.appraisal_method_code = cc2.appraisal_method_code
        LEFT JOIN culvert_cost cc3 ON cc3.effective_date > cc1.effective_date AND cc2.effective_date > cc3.effective_date AND cc3.culvert_diameter = cc2.culvert_diameter AND cc2.appraisal_method_code = cc3.appraisal_method_code
        where cc1.appraisal_method_code = 'C'
        and cc3.effective_date is null
    ) culverts on appraisal_data_submission.appraisal_effective_date >= culverts.START_DATE and appraisal_data_submission.appraisal_effective_date < culverts.END_DATE and ads_culvert.culvert_diameter = culverts.culvert_diameter
    /*WHERE
    (APPRAISAL_DATA_SUBMISSION_CTRL.APPRAISAL_METHOD_CODE = 'C') 
    AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE = 'P')*/
    GROUP BY ads_culvert.ecas_id
) culverts on appraisal_data_submission.ecas_id = culverts.ecas_id
left outer join (
    SELECT 
    ads_tabular_road_section.ecas_id,
    SUM(ads_tabular_road_section.section_length * road_costs.cost_estimate) AS road_cost
    FROM ads_tabular_road_section
    /*inner join appraisal_data_submission_ctrl on appraisal_data_submission_ctrl.ecas_id = ads_tabular_road_section.ecas_id*/
    inner join appraisal_data_submission on ads_tabular_road_section.ecas_id = appraisal_data_submission.ecas_id
    inner join (
        SELECT 
        bhrc1.effective_date as start_date,
        coalesce(bhrc2.effective_date, sysdate+1) as end_date,
        bhrc1.bank_height_category_code,
        bhrc1.rock_mass_class_code,
        bhrc1.cost_estimate
        FROM bank_height_road_cost bhrc1
        LEFT JOIN bank_height_road_cost bhrc2 ON bhrc2.effective_date > bhrc1.effective_date AND bhrc1.bank_height_category_code = bhrc2.bank_height_category_code AND bhrc1.rock_mass_class_code = bhrc2.rock_mass_class_code
        LEFT JOIN bank_height_road_cost bhrc3 ON bhrc3.effective_date > bhrc1.effective_date AND bhrc2.effective_date > bhrc3.effective_date AND bhrc3.bank_height_category_code = bhrc2.bank_height_category_code AND bhrc3.rock_mass_class_code = bhrc2.rock_mass_class_code
        WHERE bhrc3.effective_date is null
    ) road_costs on appraisal_data_submission.appraisal_effective_date >= road_costs.start_date and appraisal_data_submission.appraisal_effective_date < road_costs.end_date and ads_tabular_road_section.bank_height_category_code = road_costs.bank_height_category_code and ads_tabular_road_section.subgrade_rmc_code = road_costs.rock_mass_class_code
    /*WHERE appraisal_method_code = 'C'
    AND appraisal_category_code = 'P'*/
    GROUP BY ads_tabular_road_section.ecas_id
) roads on roads.ecas_id = appraisal_data_submission.ecas_id
left outer join (
    SELECT 
    *
    FROM (
        SELECT 
        ADEC.ECAS_ID,
        NVL(ADS_NON_TABULAR_DEV_TYPE_CODE, 0) AS ADS_NON_TABULAR_DEV_TYPE_CODE,
        SUM(TOTAL_COST) AS TOTAL_COST
        FROM ads_detailed_engineering_cost adec
        inner join appraisal_data_submission ads on ads.ecas_id = adec.ecas_id
        inner join appraisal_data_submission_ctrl adsc on adec.ecas_id = adsc.ecas_id
        group by adec.ecas_id, adec.ADS_NON_TABULAR_DEV_TYPE_CODE
    )
    PIVOT (
        SUM(TOTAL_COST) 
        FOR ADS_NON_TABULAR_DEV_TYPE_CODE IN (
            '0' AS NDCUNKNOWN, 
            '1' AS NDCTYPE1, 
            '2' AS NDCTYPE2, 
            '3' AS NDCTYPE3, 
            '4' AS NDCTYPE4, 
            '5' AS NDCTYPE5,
            '6' AS NDCTYPE6, 
            '7' AS NDCTYPE7, 
            '8' AS NDCTYPE8, 
            '9' AS NDCTYPE9, 
            '10' AS NDCTYPE10, 
            '11' AS NDCTYPE11, 
            '12' AS NDCTYPE12, 
            '13' AS NDCTYPE13, 
            '14' AS NDCTYPE14, 
            '15' AS NDCTYPE15
        )
    )
) ndc on ndc.ecas_id = appraisal_data_submission.ecas_id
left outer join (
    SELECT * FROM(
        SELECT
        ads_specified_operation.ECAS_ID,
        NVL(SPECIFIED_OPERATIONS_CODE, 0) AS SPECIFIED_OPERATIONS_CODE,
        SPECIFIED_OPERATING_RATE
        FROM ads_specified_operation
        inner join appraisal_data_submission on ads_specified_operation.ecas_id = appraisal_data_submission.ecas_id
        inner join appraisal_data_submission_ctrl adsc on (adsc.ECAS_ID = APPRAISAL_DATA_SUBMISSION.ECAS_ID)
        WHERE APPRAISAL_DATA_SUBMISSION.appraisal_category_code = 'P'
            AND adsc.appraisal_method_code = 'C'
    )
    PIVOT (SUM(SPECIFIED_OPERATING_RATE) FOR SPECIFIED_OPERATIONS_CODE IN (
        '0' AS SOAUNKNOWN, 
        'EBM' AS EBM, 
        'TCM' AS TCM, 
        'BG' AS BG, 
        'FRZ' AS FRZ, 
        'SL' AS SL, 
        'IW' AS IW, 
        'CS' AS CS, 
        'HDC' AS HDC))
) soa on appraisal_data_submission.ecas_id = soa.ecas_id

WHERE
-- Conditions
(APPRAISAL_DATA_SUBMISSION_CTRL.APPRAISAL_METHOD_CODE = 'C') 
AND (ADS_SUBMITTED_TIMBER_MARK.PRIMARY_MARK_IND = 'Y')
AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_CATEGORY_CODE = 'P')
AND (APPRAISAL_DATA_SUBMISSION.APPRAISAL_STATUS_CODE = 'CON')
AND SRS1.STUMPAGE_RTE_SUBTOTAL_TYP_CODE = 'INDR'
AND SRS2.STUMPAGE_RTE_SUBTOTAL_TYP_CODE = 'FEWB'
AND SRS3.STUMPAGE_RTE_SUBTOTAL_TYP_CODE = 'TTOA'
ORDER BY 
APPRAISAL_DATA_SUBMISSION.ECAS_ID DESC

''', connection)


# In[7]:


confirmed = pd.DataFrame(query)
filePath = os.path.join(rootPath, 'confirmed.csv')
confirmed.to_csv(filePath,index=False, header=True)


# In[8]:


query = pd.read_sql_query('''

SELECT
ADS.ECAS_ID,
ASTM.TIMBER_MARK,
APPRAISAL_STATUS_CODE,
ORG_UNIT_CODE,
DATA_OFFICE_CHECKED_IND,
DATA_FIELD_CHECKED_IND,
TOA_ELIGIBLE_IND
FROM 
APPRAISAL_DATA_SUBMISSION ADS
LEFT JOIN APPRAISAL_DATA_SUBMISSION_CTRL ADSC ON ADS.ECAS_ID = ADSC.ECAS_ID
LEFT JOIN ORG_UNIT ON ORG_UNIT.ORG_UNIT_NO = ADS.ADMIN_DISTRICT
LEFT JOIN ADS_SUBMITTED_TIMBER_MARK ASTM ON ASTM.ECAS_ID = ADS.ECAS_ID
WHERE
APPRAISAL_METHOD_CODE = 'C'
AND APPRAISAL_CATEGORY_CODE = 'P'

''', connection)


# In[9]:


running_total = pd.DataFrame(query)
filePath = os.path.join(rootPath, 'runningTotal.csv')
running_total.to_csv(filePath,index=False, header=True)


# In[ ]:




