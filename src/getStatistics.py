import pandas as pd, orderedset, datetime, cliffsDelta
from collections import Counter
from prettytable import PrettyTable
from scipy.stats import mannwhitneyu



class Gist:
    def __init__(self, name, author, repo, gists, followers, following):
        self.name = name
        self.author = author
        self.repo = repo
        self.gists = gists
        self.followers = followers
        self.following = following
        self.experience = 0
        self.smells = []
        self.sloc = 0
        self.withAtleastOneSmell = False
        self.reputation = 0

gistData = pd.read_csv('author2.csv', header=None)
smellData = pd.read_csv('smells.csv', header=None)

gists = []

for index in range(0, len(gistData)):
    gist = Gist(gistData.iloc[index, 1], gistData.iloc[index, 2], gistData.iloc[index, 3], gistData.iloc[index, 4], gistData.iloc[index, 5], gistData.iloc[index, 6])
    authorCreationTime = datetime.datetime.strptime(gistData.iloc[index, 7], '%Y-%m-%d')
    gist.experience = (datetime.datetime.now() - authorCreationTime).days
    gist.reputation = gist.followers/gist.experience
    gists.append(gist)

print(f'total gists: {len(gists)}')
foundSmells = []
files = []
for index in range(0, len(smellData)):
    foundSmells.append(smellData.iloc[index, 1])
    files.append(smellData.iloc[index, 0])

smellSet = orderedset.OrderedSet(foundSmells)
fileSet = orderedset.OrderedSet(files)
print(f'smells: {smellSet}')

for index in range(0, len(smellData)):
    fileName = smellData.iloc[index, 0]
    smellName = smellData.iloc[index, 1]
    try:
        gist = next(x for x in gists if x.name == fileName)
    except:
        continue
    gist.smells.append(smellName)

GISTWITHATLEASTONESMELL = len([x for x in gists if len(x.smells) > 0])
print(f'gists with at least one smells: {GISTWITHATLEASTONESMELL}')

SH_IN = 0
AS_US = 0
EM_PA = 0
EX_US = 0
DE_TR = 0
HA_IN = 0
HA_SE = 0
HA_SQ = 0
HA_TE = 0
NO_IN = 0
NO_CE = 0
BA_PE = 0
IG_EX = 0
US_HT = 0
US_RE = 0
CO_IN = 0
YA_LO = 0

SH_IN_AL = 0
AS_US_AL = 0
EM_PA_AL = 0
EX_US_AL = 0
DE_TR_AL = 0
HA_IN_AL = 0
HA_SE_AL = 0
HA_SQ_AL = 0
HA_TE_AL = 0
NO_IN_AL = 0
NO_CE_AL = 0
BA_PE_AL = 0
IG_EX_AL = 0
US_HT_AL = 0
US_RE_AL = 0
CO_IN_AL = 0
YA_LO_AL = 0
TOTAL_SMELLS = 0


for item in gists:
    count = Counter(item.smells)
    TOTAL_SMELLS += len(item.smells)

    if len(item.smells) > 0: item.withAtleastOneSmell = True

    if count['shell_injection']: SH_IN += count['shell_injection']
    if count['shell_injection'] > 0: SH_IN_AL += 1

    if count['assert_used']: AS_US += count['assert_used']
    if count['assert_used'] > 0: AS_US_AL += 1

    if count['empty_password']: EM_PA += count['empty_password']
    if count['empty_password'] > 0: EM_PA_AL += 1

    if count['exec_used']: EX_US += count['exec_used']
    if count['exec_used'] > 0: EX_US_AL += 1

    if count['debug_true']: DE_TR += count['debug_true']
    if count['debug_true'] > 0: DE_TR_AL += 1

    if count['hardcoded_interface']: HA_IN += count['hardcoded_interface']
    if count['hardcoded_interface'] > 0: HA_IN_AL += 1

    if count['hardcoded_secret']: HA_SE += count['hardcoded_secret']
    if count['hardcoded_secret'] > 0: HA_SE_AL += 1

    if count['hardcoded_sql']: HA_SQ += count['hardcoded_sql']
    if count['hardcoded_sql'] > 0: HA_SQ_AL += 1

    if count['hardcoded_tmp']: HA_TE += count['hardcoded_tmp']
    if count['hardcoded_tmp'] > 0: HA_TE_AL += 1

    if count['no_integrity_check']: NO_IN += count['no_integrity_check']
    if count['no_integrity_check'] > 0: NO_IN_AL += 1

    if count['no_cert_validation']: NO_CE += count['no_cert_validation']
    if count['no_cert_validation'] > 0: NO_CE_AL += 1

    if count['bad_file_permissions']: BA_PE += count['bad_file_permissions']
    if count['bad_file_permissions'] > 0: BA_PE_AL += 1

    if count['ignore_except_block']: IG_EX += count['ignore_except_block']
    if count['ignore_except_block'] > 0: IG_EX_AL += 1

    if count['use_of_http']: US_HT += count['use_of_http']
    if count['use_of_http'] > 0: US_HT_AL += 1

    if count['use_of_regex']: US_RE += count['use_of_regex']
    if count['use_of_regex'] > 0: US_RE_AL += 1

    if count['command_injection']: CO_IN += count['command_injection']
    if count['command_injection'] > 0: CO_IN_AL += 1

    if count['yaml_load']: YA_LO += count['yaml_load']
    if count['yaml_load'] > 0: YA_LO_AL += 1

    sloc = 0
    src = open(f'/home/brokenquark/Workspace/ICSME19/gist-src/{item.name}', 'r')
    for line in src:
        if len(line.strip()) > 0:
            sloc += 1

    item.sloc = sloc

totalSloc = sum(x.sloc for x in gists)
totalFiles = len(gists)


print('=== GITHUB GIST DATA ===')
pt = PrettyTable()

pt.field_names = ['smell', 'occurence', 'density', 'proportion']
pt.add_row(['shell_injection', f'{SH_IN}', f'{SH_IN/(totalSloc/1000):.2f}', f'{100*SH_IN_AL/totalFiles:.2f}'])
pt.add_row(['assert_used', f'{AS_US}', f'{AS_US/(totalSloc/1000):.2f}', f'{100*AS_US_AL/totalFiles:.2f}'])
pt.add_row(['empty_password', f'{EM_PA}', f'{EM_PA/(totalSloc/1000):.2f}', f'{100*EM_PA_AL/totalFiles:.2f}'])
pt.add_row(['exec_used', f'{EX_US}', f'{EX_US/(totalSloc/1000):.2f}', f'{100*EX_US_AL/totalFiles:.2f}'])
pt.add_row(['debug_true', f'{DE_TR}', f'{DE_TR/(totalSloc/1000):.2f}', f'{100*DE_TR_AL/totalFiles:.2f}'])
pt.add_row(['hardcoded_interface', f'{HA_IN}', f'{HA_IN/(totalSloc/1000):.2f}', f'{100*HA_IN_AL/totalFiles:.2f}'])
pt.add_row(['hardcoded_secret', f'{HA_SE}', f'{HA_SE/(totalSloc/1000):.2f}', f'{100*HA_SE_AL/totalFiles:.2f}'])
pt.add_row(['hardcoded_sql', f'{HA_SQ}', f'{HA_SQ/(totalSloc/1000):.2f}', f'{100*HA_SQ_AL/totalFiles:.2f}'])
pt.add_row(['hardcoded_tmp', f'{HA_TE}', f'{HA_TE/(totalSloc/1000):.2f}', f'{100*HA_TE_AL/totalFiles:.2f}'])
pt.add_row(['no_integrity_check', f'{NO_IN}', f'{NO_IN/(totalSloc/1000):.2f}', f'{100*NO_IN_AL/totalFiles:.2f}'])
pt.add_row(['no_cert_validation', f'{NO_CE}', f'{NO_CE/(totalSloc/1000):.2f}', f'{100*NO_CE_AL/totalFiles:.2f}'])
pt.add_row(['bad_file_permissions', f'{BA_PE}', f'{BA_PE/(totalSloc/1000):.2f}', f'{100*BA_PE_AL/totalFiles:.2f}'])
pt.add_row(['ignore_except_block', f'{IG_EX}', f'{IG_EX/(totalSloc/1000):.2f}', f'{100*IG_EX_AL/totalFiles:.2f}'])
pt.add_row(['use_of_http', f'{US_HT}', f'{US_HT/(totalSloc/1000):.2f}', f'{100*US_HT_AL/totalFiles:.2f}'])
pt.add_row(['TOTAL', f'{TOTAL_SMELLS}', f'{TOTAL_SMELLS/(totalSloc/1000):.2f}', f'{100*GISTWITHATLEASTONESMELL/totalFiles:.2f}'])

print(pt)


authorsOfSmellyGists = [x.reputation for x in gists if x.withAtleastOneSmell == True]
authorsOfCleanGists = [x.reputation for x in gists if x.withAtleastOneSmell == False]

stat, p = mannwhitneyu(authorsOfSmellyGists, authorsOfCleanGists)

alpha = 0.05
if p > alpha:
    print('Two sets of authors are same')
else:
    print('Authors with at least one smell in gists are different than authors with no smell in gists')

print('however, this difference is, ', end='')
print(cliffsDelta.cliffsDelta(authorsOfCleanGists, authorsOfSmellyGists))

print('=== GITHUB GIST MANUAL INSPECTION ===')
pt2 = PrettyTable()

pt2.field_names = ['smell', 'occurence', 'precision', 'recall']
pt2.add_row(['shell_injection', '86', '1.00', '1.00'])
pt2.add_row(['assert_used', '79', '1.00', '1.00'])
pt2.add_row(['empty_password', '2', '1.00', '1.00'])
pt2.add_row(['exec_used', '4', '1.00', '1.00'])
pt2.add_row(['debug_true',  '2', '1.00', '1.00'])
pt2.add_row(['hardcoded_interface',  '3', '1.00', '1.00'])
pt2.add_row(['hardcoded_secret',  '31', '0.94', '0.91'])
pt2.add_row(['hardcoded_sql',  '3', '1.00', '1.00'])
pt2.add_row(['hardcoded_tmp',  '3', '1.00', '1.00'])
pt2.add_row(['no_integrity_check',  '7', '0.43', '0.75'])
pt2.add_row(['no_cert_validation',  '1', '1.00', '1.00'])
pt2.add_row(['bad_file_permissions',  '1', '1.00', '1.00'])
pt2.add_row(['ignore_except_block',  '13', '1.00', '1.00'])
pt2.add_row(['use_of_http',  '71', '1.00', '1.00'])
pt2.add_row(['TOTAL', '306', '0.98', '0.99'])

print(pt2)

frequencies = []

# for item in gists:
#     frequencies.append(len(item.smells))
#
# for item in frequencies:
#     print(item)