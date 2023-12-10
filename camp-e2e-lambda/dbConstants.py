from enum import Enum

TABLE_NAME = 'Camp-E2E-table'

#########  Db attributes  #########
PARTITION_KEY = 'testConfigId'
SORT_KEY = 'payloadIdOrStatus'

# TestConfig Schema
COL_NAME = 'testName'
COL_DESCRIPTION = 'description'
COL_PRODID_MAPPING = 'productIdMapping'
COL_BRANDID_MAPPING = 'brandIdMapping'
COL_CREDITPOLICYID = 'creditPolicyId'
COL_MENSAFILENAME = 'mensaFileName' 
COL_CSV_DATA = 'csvData'

# TestResult Schema
COL_OTHERS = 'resultFields'
COL_RESULT = 'result'
COL_PAYLOAD = 'payload'
COL_APPLICATION_ID = 'applicationId'

# COMMON
COL_DATE_CREATED = 'dateCreated'
COL_LAST_UPDATED = 'lastUpdated'


# sort key
CONFIG_SORT_VALUE = 'config'

# enumerators
class TESTCONFIGSTATUS(Enum):
    ACTIVE = 'Active'
    ARCHIVED = 'Archived'

class TESTRESULTYPE(Enum):
    APPROVED = 'Approved'
    IN_PROGRESS = 'In-progress'
    DECLINED = 'Declined'