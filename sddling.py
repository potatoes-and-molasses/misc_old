import re
import subprocess

SD_CONTROLS = 0
ACE_TYPES = 1
ACE_FLAGS = 2
SD_RIGHTS = 3
SD_USERS = 4
RIGHT_GUIDS = 5 #super very incomplete list consisting of only the extended rights guids.
LOOKUP = [{'O': 'SDDL_OWNER(Owner tag)',
'G': 'SDDL_GROUP(Group tag)',
'D': 'SDDL_DACL(DACL tag)',
'S': 'SDDL_SACL(SACL tag)',
'P': 'SDDL_PROTECTED(DACL or SACL Protected)',
'AR': 'SDDL_AUTO_INHERIT_REQ(Auto inherit request)',
'AI': 'SDDL_AUTO_INHERITED(DACL/SACL are auto inherited)',
'NO_ACCESS_CONTROL': 'SDDL_NULL_ACL(Null ACL)'},
    
    {'A': 'SDDL_ACCESS_ALLOWED(Access allowed)',
'D': 'SDDL_ACCESS_DENIED(Access denied)',
'OA': 'SDDL_OBJECT_ACCESS_ALLOWED(Object access allowed)',
'OD': 'SDDL_OBJECT_ACCESS_DENIED(Object access denied)',
'AU': 'SDDL_AUDIT(Audit)',
'AL': 'SDDL_ALARM(Alarm)',
'OU': 'SDDL_OBJECT_AUDIT(Object audit)',
'OL': 'SDDL_OBJECT_ALARM(Object alarm)',
'ML': 'SDDL_MANDATORY_LABEL(Integrity label)',
'XA': 'SDDL_CALLBACK_ACCESS_ALLOWED(callback Access allowed)',
'XD': 'SDDL_CALLBACK_ACCESS_DENIED(callback Access denied)'},
              
    {'CI': 'SDDL_CONTAINER_INHERIT(Container inherit)',
'OI': 'SDDL_OBJECT_INHERIT(Object inherit)',
'NP': 'SDDL_NO_PROPAGATE(Inherit no propagate)',
'IO': 'SDDL_INHERIT_ONLY(Inherit only)',
'ID': 'SDDL_INHERITED(Inherited)',
'SA': 'SDDL_AUDIT_SUCCESS(Audit success)',
'FA': 'SDDL_AUDIT_FAILURE(Audit failure)'},

    {'RP': 'SDDL_READ_PROPERTY',
'WP': 'SDDL_WRITE_PROPERTY',
'CC': 'SDDL_CREATE_CHILD',
'DC': 'SDDL_DELETE_CHILD',
'LC': 'SDDL_LIST_CHILDREN',
'SW': 'SDDL_SELF_WRITE',
'LO': 'SDDL_LIST_OBJECT',
'DT': 'SDDL_DELETE_TREE',
'CR': 'SDDL_CONTROL_ACCESS',
'RC': 'SDDL_READ_CONTROL',
'WD': 'SDDL_WRITE_DAC',
'WO': 'SDDL_WRITE_OWNER',
'SD': 'SDDL_STANDARD_DELETE',
'GA': 'SDDL_GENERIC_ALL',
'GR': 'SDDL_GENERIC_READ',
'GW': 'SDDL_GENERIC_WRITE',
'GX': 'SDDL_GENERIC_EXECUTE',
'FA': 'SDDL_FILE_ALL',
'FR': 'SDDL_FILE_READ',
'FW': 'SDDL_FILE_WRITE',
'FX': 'SDDL_FILE_EXECUTE',
'KA': 'SDDL_KEY_ALL',
'KR': 'SDDL_KEY_READ',
'KW': 'SDDL_KEY_WRITE',
'KX': 'SDDL_KEY_EXECUTE',
'NW': 'SDDL_NO_WRITE_UP',
'NR': 'SDDL_NO_READ_UP',
'NX': 'SDDL_NO_EXECUTE_UP'},

    {'DA': 'SDDL_DOMAIN_ADMINISTRATORS(Domain admins)',
'DG': 'SDDL_DOMAIN_GUESTS(Domain guests)',
'DU': 'SDDL_DOMAIN_USERS(Domain users)',
'ED': 'SDDL_ENTERPRISE_DOMAIN_CONTROLLERS(Enterprise domain controllers)',
'DD': 'SDDL_DOMAIN_DOMAIN_CONTROLLERS(Domain domain controllers)',
'DC': 'SDDL_DOMAIN_COMPUTERS(Domain computers)',
'BA': 'SDDL_BUILTIN_ADMINISTRATORS(Builtin (local ) administrators)',
'BG': 'SDDL_BUILTIN_GUESTS(Builtin (local ) guests)',
'BU': 'SDDL_BUILTIN_USERS(Builtin (local ) users)',
'LA': 'SDDL_LOCAL_ADMIN(Local administrator account)',
'LG': 'SDDL_LOCAL_GUEST(Local group account)',
'AO': 'SDDL_ACCOUNT_OPERATORS(Account operators)',
'BO': 'SDDL_BACKUP_OPERATORS(Backup operators)',
'PO': 'SDDL_PRINTER_OPERATORS(Printer operators)',
'SO': 'SDDL_SERVER_OPERATORS(Server operators)',
'AU': 'SDDL_AUTHENTICATED_USERS(Authenticated users)',
'PS': 'SDDL_PERSONAL_SELF(Personal self)',
'CO': 'SDDL_CREATOR_OWNER(Creator owner)',
'CG': 'SDDL_CREATOR_GROUP(Creator group)',
'SY': 'SDDL_LOCAL_SYSTEM(Local system)',
'PU': 'SDDL_POWER_USERS(Power users)',
'WD': 'SDDL_EVERYONE(Everyone ( World ))',
'RE': 'SDDL_REPLICATOR(Replicator)',
'IU': 'SDDL_INTERACTIVE(Interactive logon user)',
'NU': 'SDDL_NETWORK(Nework logon user)',
'SU': 'SDDL_SERVICE(Service logon user)',
'RC': 'SDDL_RESTRICTED_CODE(Restricted code)',
'WR': 'SDDL_WRITE_RESTRICTED_CODE(Write Restricted code)',
'AN': 'SDDL_ANONYMOUS(Anonymous Logon)',
'SA': 'SDDL_SCHEMA_ADMINISTRATORS(Schema Administrators)',
'CA': 'SDDL_CERT_SERV_ADMINISTRATORS(Certificate Server Administrators)',
'RS': 'SDDL_RAS_SERVERS(RAS servers group)',
'EA': 'SDDL_ENTERPRISE_ADMINS(Enterprise administrators)',
'PA': 'SDDL_GROUP_POLICY_ADMINS(Group Policy administrators)',
'RU': 'SDDL_ALIAS_PREW2KCOMPACC(alias to allow previous windows 2000)',
'LS': 'SDDL_LOCAL_SERVICE(Local service account (for services))',
'NS': 'SDDL_NETWORK_SERVICE(Network service account (for services))',
'RD': 'SDDL_REMOTE_DESKTOP(Remote desktop users (for terminal server))',
'NO': 'SDDL_NETWORK_CONFIGURATION_OPS(Network configuration operators ( to manage configuration of networking features))',
'MU': 'SDDL_PERFMON_USERS(Performance Monitor Users)',
'LU': 'SDDL_PERFLOG_USERS(Performance Log Users)',
'IS': 'SDDL_IIS_USERS(Anonymous Internet Users)',
'CY': 'SDDL_CRYPTO_OPERATORS(Crypto Operators)',
'OW': 'SDDL_OWNER_RIGHTS(Owner Rights SID)',
'ER': 'SDDL_EVENT_LOG_READERS(Event log readers)',
'RO': 'SDDL_ENTERPRISE_RO_DCs(Enterprise Read-only domain controllers)',
'CD': 'SDDL_CERTSVC_DCOM_ACCESS(Users who can connect to certification authorities using DCOM)',
'LW': 'SDDL_ML_LOW(Low mandatory level)',
'ME': 'SDDL_ML_MEDIUM(Medium mandatory level)',
'MP': 'SDDL_ML_MEDIUM_PLUS(Medium Plus mandatory level)',
'HI': 'SDDL_ML_HIGH(High mandatory level)',
'SI': 'SDDL_ML_SYSTEM(System mandatory level)'},

{'4332aad9-95ab-4e8e-a264-4965c3e1f964': 'ms-Exch-Store-Bypass-Access-Auditing',
'91e647de-d96f-4b70-9557-d63ff4f3ccd8': 'Private-Information',
'1131f6ae-9c07-11d1-f79f-00c04fc2dcd2': 'Read-Only-Replication-Secret-Synchronization',
'1a60ea8d-58a6-4b20-bcdc-fb71eb8a9ff8': 'Reload-SSL-Certificate',
'89e95b76-444d-4c62-991a-0facbeda640c': 'DS-Replication-Get-Changes-In-Filtered-Set',
'5805bc62-bdc9-4428-a5e2-856a0f4c185e': 'Terminal-Server-License-Server',
'811d004b-e2ed-4024-8953-0f0fb0612e47': 'ms-Exch-SMTP-Accept-XShadow',
'5bc2acab-ad7d-4878-b6cd-3122a47c6a1c': 'ms-Exch-SMTP-Send-XShadow',
'd819615a-3b9b-4738-b47e-f1bd8ee3aea4': 'RTCPropertySet',
'e2d6986b-2c7f-4cda-9851-d5b5f3fb6706': 'RTCUserSearchPropertySet',
'3e0f7e18-2c7a-4c10-ba82-4d926db99a3e': 'DS-Clone-Domain-Controller',
'd31a8757-2447-4545-8081-3bb610cacbf2': 'Validated-MS-DS-Behavior-Version',
'80863791-dbe9-4eb8-837e-7f0ab55d9ac7': 'Validated-MS-DS-Additional-DNS-Host-Name',
'a05b8cc2-17bc-4802-a710-e7c15ab866a2': 'Certificate-AutoEnrollment',
'77b5b886-944a-11d1-aebd-0000f80367c1': 'Personal-Information',
'4c164200-20c0-11d0-a768-00aa006e0529': 'User-Account-Restrictions',
'72e39547-7b18-11d1-adef-00c04fd8d5cd': 'DNS-Host-Name-Attributes',
'72e39547-7b18-11d1-adef-00c04fd8d5cd': 'Validated-DNS-Host-Name',
'1f298a89-de98-47b8-b5cd-572ad53d267e': 'Exchange-Information',
'b1b3a417-ec55-4191-b327-b72e33e38af2': 'Exchange-Personal-Information',
'a7a9ea66-e08c-4e23-8fe7-68c40e49c6c0': 'ms-Exch-Accept-Headers-Forest',
'9b51a1ef-79b7-4ae5-9ac8-d14c47daca46': 'RTCUserProvisioningPropertySet',
'c307dccd-6676-4d19-95c8-d1567fab9820': 'ms-Exch-Accept-Headers-Organization',
'04031f4f-7c36-43ea-9b49-4bd0f5f1e6af': 'ms-Exch-Accept-Headers-Routing',
'ce4c81a8-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Add-PF-To-Admin-Group',
'8e48d5a8-b09e-11d2-aa06-00c04f8eedd8': 'ms-Exch-Admin-Role-Administrator',
'8e6571e0-b09e-11d2-aa06-00c04f8eedd8': 'ms-Exch-Admin-Role-Full-Administrator',
'8ff1383c-b09e-11d2-aa06-00c04f8eedd8': 'ms-Exch-Admin-Role-Read-Only-Administrator',
'90280e52-b09e-11d2-aa06-00c04f8eedd8': 'ms-Exch-Admin-Role-Service',
'd19299b4-86c2-4c9a-8fa7-acb70c63023a': 'ms-Exch-Bypass-Anti-Spam',
'ab721a52-1e2f-11d0-9819-00aa0040529b': 'Domain-Administer-Server',
'6760cfc5-70f4-4ae8-bc39-9522d86ac69b': 'ms-Exch-Bypass-Message-Size-Limit',
'ab721a55-1e2f-11d0-9819-00aa0040529b': 'Send-To',
'cf0b3dc8-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Create-Public-Folder',
'c7407360-20bf-11d0-a768-00aa006e0529': 'Domain-Password',
'cf4b9d46-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Create-Top-Level-Public-Folder',
'59ba2f42-79a2-11d0-9020-00c04fc2d3cf': 'General-Information',
'bd919c7c-2d79-4950-bc9c-e16fd99285e8': 'ms-Exch-Download-OAB',
'5f202010-79a5-11d0-9020-00c04fc2d4cf': 'User-Logon',
'8db0795c-df3a-4aca-a97d-100162998dfa': 'ms-Exch-EPI-Impersonation',
'bc0ac240-79a9-11d0-9020-00c04fc2d4cf': 'Membership',
'bc39105d-9baa-477c-a34a-997cc25e3d60': 'ms-Exch-EPI-May-Impersonate',
'a1990816-4298-11d1-ade2-00c04fd8d5cd': 'Open-Address-Book',
'06386f89-befb-4e48-baa1-559fd9221f78': 'ms-Exch-EPI-Token-Serialization',
'e45795b2-9455-11d1-aebd-0000f80367c1': 'Email-Information',
'cf899a6a-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Mail-Enabled-Public-Folder',
'e45795b3-9455-11d1-aebd-0000f80367c1': 'Web-Information',
'd74a8769-22b9-11d3-aa62-00c04f8eedd8': 'ms-Exch-Modify-PF-ACL',
'1131f6aa-9c07-11d1-f79f-00c04fc2dcd2': 'DS-Replication-Get-Changes',
'd74a876f-22b9-11d3-aa62-00c04f8eedd8': 'ms-Exch-Modify-PF-Admin-ACL',
'1131f6ab-9c07-11d1-f79f-00c04fc2dcd2': 'DS-Replication-Synchronize',
'cffe6da4-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Modify-Public-Folder-Deleted-Item-Retention',
'1131f6ac-9c07-11d1-f79f-00c04fc2dcd2': 'DS-Replication-Manage-Topology',
'cfc7978e-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Modify-Public-Folder-Expiry',
'e12b56b6-0a95-11d1-adbb-00c04fd8d5cd': 'Change-Schema-Master',
'd03a086e-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Modify-Public-Folder-Quotas',
'd58d5f36-0a98-11d1-adbb-00c04fd8d5cd': 'Change-Rid-Master',
'd0780592-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Modify-Public-Folder-Replica-List',
'fec364e0-0a98-11d1-adbb-00c04fd8d5cd': 'Do-Garbage-Collection',
'd74a8774-22b9-11d3-aa62-00c04f8eedd8': 'ms-Exch-Open-Send-Queue',
'0bc1554e-0a99-11d1-adbb-00c04fd8d5cd': 'Recalculate-Hierarchy',
'be013017-13a1-41ad-a058-f156504cb617': 'ms-Exch-Read-Metabase-Properties',
'1abd7cf8-0a99-11d1-adbb-00c04fd8d5cd': 'Allocate-Rids',
'165ab2cc-d1b3-4717-9b90-c657e7e57f4d': 'ms-Exch-Recipient-Update-Access',
'bae50096-4752-11d1-9052-00c04fc2d4cf': 'Change-PDC',
'd0b86510-afe6-11d2-aa04-00c04f8eedd8': 'ms-Exch-Remove-PF-From-Admin-Group',
'440820ad-65b4-11d1-a3da-0000f875ae0d': 'Add-GUID',
'b3f9f977-552c-4ee6-9781-59280a81417b': 'ms-Exch-Send-Headers-Forest',
'014bf69c-7b3b-11d1-85f6-08002be74fab': 'Change-Domain-Master',
'2f7d0e23-f951-4ed0-8e71-39b6a22fa298': 'ms-Exch-Send-Headers-Organization',
'4b6e08c0-df3c-11d1-9c86-006008764d0e': 'msmq-Receive-Dead-Letter',
'eb8c07ad-b5ad-49c3-831e-bc439cca4c2a': 'ms-Exch-Send-Headers-Routing',
'4b6e08c1-df3c-11d1-9c86-006008764d0e': 'msmq-Peek-Dead-Letter',
'5c82f031-4e4c-4326-88e1-8c4f0cad9de5': 'ms-Exch-SMTP-Accept-Any-Recipient',
'4b6e08c2-df3c-11d1-9c86-006008764d0e': 'msmq-Receive-computer-Journal',
'b857b50b-94a2-4b53-93f6-41cebd2fced0': 'ms-Exch-SMTP-Accept-Any-Sender',
'4b6e08c3-df3c-11d1-9c86-006008764d0e': 'msmq-Peek-computer-Journal',
'1c75aca8-b56b-48b3-a021-858a29fa877b': 'ms-Exch-SMTP-Accept-Authentication-Flag',
'06bd3200-df3e-11d1-9c86-006008764d0e': 'msmq-Receive',
'c22841f4-96cb-498a-ac02-f9a87c74eb14': 'ms-Exch-SMTP-Accept-Authoritative-Domain-Sender',
'06bd3201-df3e-11d1-9c86-006008764d0e': 'msmq-Peek',
'e373fb21-d851-4d15-af23-982f09f2400b': 'ms-Exch-SMTP-Accept-Exch50',
'06bd3202-df3e-11d1-9c86-006008764d0e': 'msmq-Send',
'11716db4-9647-4bce-8922-1f99e526cb41': 'ms-Exch-SMTP-Send-Exch50',
'06bd3203-df3e-11d1-9c86-006008764d0e': 'msmq-Receive-journal',
'a18293f1-0685-4540-aa63-e32df421b3a2': 'ms-Exch-SMTP-Submit',
'b4e60130-df3f-11d1-9c86-006008764d0e': 'msmq-Open-Connector',
'8fc01282-006d-42b1-81e3-c0b46bed3754': 'ms-Exch-SMTP-Submit-For-MLS',
'edacfd8f-ffb3-11d1-b41d-00a0c968f939': 'Apply-Group-Policy',
'd74a8762-22b9-11d3-aa62-00c04f8eedd8': 'ms-Exch-Store-Admin',
'037088f8-0ae1-11d2-b422-00a0c968f939': 'RAS-Information',
'9fbec2a1-f761-11d9-963d-00065bbd3175': 'ms-Exch-Store-Constrained-Delegation',
'9923a32a-3607-11d2-b9be-0000f87a36b2': 'DS-Install-Replica',
'd74a8766-22b9-11d3-aa62-00c04f8eedd8': 'ms-Exch-Store-Create-Named-Properties',
'cc17b1fb-33d9-11d2-97d4-00c04fd8d5cd': 'Change-Infrastructure-Master',
'9fbec2a3-f761-11d9-963d-00065bbd3175': 'ms-Exch-Store-Read-Access',
'be2bb760-7f46-11d2-b9ad-00c04f79f805': 'Update-Schema-Cache',
'9fbec2a4-f761-11d9-963d-00065bbd3175': 'ms-Exch-Store-Read-Write-Access',
'62dd28a8-7f46-11d2-b9ad-00c04f79f805': 'Recalculate-Security-Inheritance',
'9fbec2a2-f761-11d9-963d-00065bbd3175': 'ms-Exch-Store-Transport-Access',
'69ae6200-7f46-11d2-b9ad-00c04f79f805': 'DS-Check-Stale-Phantoms',
'd74a875e-22b9-11d3-aa62-00c04f8eedd8': 'ms-Exch-Store-Visible',
'0e10c968-78fb-11d2-90d4-00c04f79dc55': 'Certificate-Enrollment',
'bf9679c0-0de6-11d0-a285-00aa003049e2': 'Self-Membership',
'ab721a53-1e2f-11d0-9819-00aa0040529b': 'User-Change-Password',
'b7b1b3dd-ab09-4242-9e30-9980e5d322f7': 'Generate-RSoP-Planning',
'00299570-246d-11d0-a768-00aa006e0529': 'User-Force-Change-Password',
'9432c620-033c-4db7-8b58-14ef6d0bf477': 'Refresh-Group-Cache',
'ab721a54-1e2f-11d0-9819-00aa0040529b': 'Send-As',
'91d67418-0135-4acc-8d79-c08e857cfbec': 'SAM-Enumerate-Entire-Domain',
'ab721a56-1e2f-11d0-9819-00aa0040529b': 'Receive-As',
'b7b1b3de-ab09-4242-9e30-9980e5d322f7': 'Generate-RSoP-Logging',
'e48d0154-bcf8-11d1-8702-00c04fb96050': 'Public-Information',
'b8119fd0-04f6-4762-ab7a-4986c76b3f9a': 'Domain-Other-Parameters',
'f3a64788-5306-11d1-a9c5-0000f80367c1': 'Validated-SPN',
'e2a36dc9-ae17-47c3-b58b-be34c55ba633': 'Create-Inbound-Forest-Trust',
'68b1d179-0d15-4d4f-ab71-46152e79a7bc': 'Allowed-To-Authenticate',
'1131f6ad-9c07-11d1-f79f-00c04fc2dcd2': 'DS-Replication-Get-Changes-All',
'ffa6f046-ca4b-4feb-b40d-04dfee722543': 'MS-TS-GatewayAccess',
'ba33815a-4f93-4c76-87f3-57574bff8109': 'Migrate-SID-History',
'7726b9d5-a4b4-4288-a6b2-dce952e80a7f': 'Run-Protect-Admin-Groups-Task',
'45ec5156-db7e-47bb-b53f-dbeb2d03c40f': 'Reanimate-Tombstones',
'7c0e2a7c-a419-48e4-a995-10180aad54dd': 'Manage-Optional-Features',
'2f16c4a5-b98e-432c-952a-cb388ba33f2e': 'DS-Execute-Intentions-Script',
'f98340fb-7c5b-4cdb-a00b-2ebdfa115a96': 'DS-Replication-Monitor-Topology',
'280f369c-67c7-438e-ae98-1d46f3c6f541': 'Update-Password-Not-Required-Bit',
'ccc2dc7d-a6ad-4a7a-8846-c04e3cc53501': 'Unexpire-Password',
'05c74c5e-4deb-43b4-bd9f-86664c2a7fd5': 'Enable-Per-User-Reversibly-Encrypted-Password',
'4ecc03fe-ffc0-4947-b630-eb672a8a9dbc': 'DS-Query-Self-Quota',
'4125c71f-7fac-4ff0-bcb7-f09a41325286': 'DS-Set-Owner',
'88a9933e-e5c8-4f2a-9dd7-2527416b8092': 'DS-Bypass-Quota',
'084c93a2-620d-4879-a836-f0ae47de0e89': 'DS-Read-Partition-Secrets'}]
def lookup(const,table):
    
    
    if const in LOOKUP[table]:
        return LOOKUP[table][const]
    else:
        return const

class sddl:

    def __init__(self,sdstring):
        first_ace = sdstring.find('(')
        self.header = sdstring[:first_ace]
        self.aces = set(sdstring[first_ace+1:-1].split(')('))
    
        
    def diff(self,other):
        diff = 0
        if self.header!=other.header:
            print 'header_diff: {} <=> {}'.format(self.header, other.header)
            diff = 1
        if self.aces != other.aces:
            a = self.aces-other.aces
            b = other.aces-self.aces
            print 'ace diffs:'
            if a:
                print '--only in self--\n{}'.format('\n'.join(a))
            if b:
                print '--only in other--\n{}\n'.format('\n'.join(b))
            diff = 1
        if not diff:
            print 'identical sddls'



def header2string(headerstring):
    sacl_exists = 0
    if 'S:' in headerstring:
        sacl_exists = 1
        q=re.match('O:(.*)G:(.*)D:(.*)S:(.*)',headerstring).groups()
    else:
        q=re.match('O:(.*)G:(.*)D:(.*)',headerstring).groups()
    print 'Owner: {}'.format(lookup(q[0],SD_USERS))
    print 'Group: {}'.format(lookup(q[1],SD_USERS))
    print 'DACL: ',
    if q[2] == 'NO_ACCESS_CONTROL' or q[2]=='':
        print 'Null'
    elif q[2]=='P':
        print lookup(q[2],SD_CONTROLS)
    elif 'P' in q[2]:
        print '{} - {}'.format(lookup(q[2][0],SD_CONTROLS),lookup(q[2][1:],SD_CONTROLS))
    else:
        print lookup(q[2],SD_CONTROLS)
    if sacl_exists:
        print 'SACLS: '
        if q[3] == 'NO_ACCESS_CONTROL' or q[3]=='':
            print 'Null'
        elif q[3]=='P':
            print lookup(q[3],SD_CONTROLS)
        elif 'P' in q[3]:
            print '{} - {}'.format(lookup(q[3][0],SD_CONTROLS),lookup(q[3][1:],SD_CONTROLS))
        else:
            print lookup(q[3],SD_CONTROLS)
        
def lookupsid(sid):
    return subprocess.check_output('powershell -c "([ADSI]\'LDAP://<SID={}>\').distinguishedname"'.format(sid),creationflags=0x08000000)
    
def ace2engrish(acestring):
    resource_attr = 0
    parts = acestring.split(';')
    if len(parts)==7:
        resource_attr = 1
        (ace_types,ace_flags,rights,object_guid,inherit_object_guid,account_sid,resource_attribute) = parts
    else:
        (ace_types,ace_flags,rights,object_guid,inherit_object_guid,account_sid) = parts
    print 'ace_type:\n{}'.format(lookup(ace_types,ACE_TYPES))
    print 'ace_flags:\n{}'.format('\n'.join([lookup(ace_flags[i:i+2],ACE_FLAGS) for i in range(0,len(ace_flags),2)]))
    print 'rights:\n{}'.format('\n'.join([lookup(rights[i:i+2],SD_RIGHTS) for i in range(0,len(rights),2)]))
    
    if object_guid :
        tmp = lookup(object_guid,RIGHT_GUIDS)
        if tmp!=object_guid:
            print 'object guid: {} => {}'.format(object_guid,tmp)
        else:
            print 'object guid: {}(google it^^)'.format(tmp)
    if inherit_object_guid:
        tmp = lookup(inherit_object_guid,RIGHT_GUIDS)
        if tmp!=inherit_object_guid:
            print 'object guid: {} => {}'.format(inherit_object_guid,tmp)
        else:
            print 'object guid: {}(google it^^)'.format(tmp)
    print 'account sid: {}'.format(lookup(account_sid,SD_USERS))

#lol bad
    print 'lousy implementation ahead, searching for sid in domain:'
    print lookupsid(lookup(account_sid,SD_USERS))
        
    if resource_attr:
        print 'resource attr: {}'.format(resource_attribute)
            
            
            
            
            
            
