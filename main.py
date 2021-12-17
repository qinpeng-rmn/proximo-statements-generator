# Qin Peng, Dec 16 2021

# command line arguments
import sys

def create_accountID_to_shortcode_dict(file_path):
    """
    :param file_path:
        path to a tsv file with 2 columns, the first column is accountID, the second column is shortcode
    :return:
        a dictionary with key accountID, and value shortcode
    """
    accountID_to_shortcode = dict()
    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i in range(1, len(lines)):
        line = lines[i].rstrip()
        accountID_to_shortcode[line.split('\t')[0].strip()] = line.split('\t')[1].strip()
    return accountID_to_shortcode

def parse_diff(file_path, accountID_to_shortcode = None):
    """
    :param file_path:
        path to a .diff file
    :param accountID_to_shortcode
        a dictionary, key: accountID, value: shortcode
    :return:
        a dictionary, 
        keys are '+' and '-',
        values are a dictionary, with keys: user_name, values: list of list [[shortcode, policy_name]]
    """

    if accountID_to_shortcode == None:
        accountID_to_shortcode = {'631714410516': 'AGN', '842029485983': 'AGN-DEV', '499859952161': 'AMN', '290264464043': 'AR1?', '866571017402': 'AR2', '810541000179': 'ARA', '496476816822': 'ARA-DEV', '198957617428': 'ARR', '140230471469': 'ARS', '395672959192': 'ARS-DEV', '555180734798': 'ARX', '019297128470': 'ARX-DEV', '003512116871': 'ARY', '401842988166': 'ARY-DEV', '812149967671': 'AUD', '317756950691': 'BAK', '772253218339': 'BAK-DEV', '119809719251': 'BLT', '402639244087': 'BLT-DEV', '289131770848': 'BRA', '476611035200': 'BRA-DEV', '935821084003': 'BTH', '386719845984': 'BTH-DEV', '750876715910': 'CRP', '561581261911': 'CRS', '969770262377': 'DNS', '472300084261': 'DNS-DEV', '357649774407': 'DPS', '908074885047': 'DPS-DEV', '475562822831': 'DRG', '041036996115': 'DRG-DEV', '371816244921': 'DRN', '721133074041': 'DRN-DEV', '806665022227': 'DSG', '454041447388': 'EDD', '485454313235': 'EDD-DEV', '506764723658': 'EDM', '259093127537': 'EDM-DEV', '249030517958': 'ENG', '904773826334': 'GHI', '481835377713': 'GHI-DEV', '142129117135': 'GLB', '741872977264': 'GLB-DEV', '475716509885': 'GLB-DR', '578156875699': 'HBZ', '847626187189': 'HMS', '200823618722': 'HMS-DEV', '490563644898': 'HTE', '382890409895': 'HTE-DEV', '212908038949': 'INT', '657670068889': 'ITM', '337090458047': 'ITM-DEV', '144028019382': 'IWG', '706505439282': 'IWG-DEV', '961982260910': 'JLN', '532117024550': 'JLN-DEV', '780023630740': 'LHF', '445612108876': 'LHF-DEV', '629542430246': 'LRS', '072193897462': 'LRS-DEV', '784555638741': 'LST', '366654054741': 'LST-DEV', '995505153132': 'LYN', '051625422615': 'LYS', '436504045080': 'MGL', '555519592862': 'MGL-DEV', '154023172102': 'MGT', '503713231026': 'MLS', '697575839920': 'MLS-DEV', '459857334855': 'MMT', '787427185972': 'MMT-DEV', '666444612450': 'MON', '962338301662': 'MON-DEV', '481737186100': 'MRG', '623240943232': 'MRG-DEV', '629311375156': 'MRT', '276154851597': 'MRT-DEV', '653464136140': 'NBV', '954821168462': 'NBV-DEV', '867237858700': 'NET', '730917175195': 'NOQ', '444352623780': 'NOQ-DEV', '918550568931': 'NYM', '175123015489': 'OBN', '934577454729': 'OBN-DEV', '415375086818': 'OBR', '213784957902': 'OBR-DEV', '715327144721': 'ORG', '112288256163': 'ORG-DEV', '308388906789': 'PLY', '871166422776': 'PRD', '395217052961': 'QTN', '210616021129': 'RBT', '019258521193': 'RBT-DEV', '881656589561': 'RC1', '796207007328': 'RC2', '296789222591': 'RCK', '755063927666': 'RCK-DEV', '122157916401': 'RHL', '258587091788': 'RHL-DEV', '727472207329': 'RNL', '840551294022': 'RPT', '583712744397': 'SAU', '788305809948': 'SHR', '097999863757': 'SHR-DEV', '659610907158': 'SSA', '455570743117': 'STG', '114420962703': 'STK', '405441783360': 'STK-DEV', '842007522200': 'SVR', '359856303733': 'SVR-DEV', '278890653358': 'TST', '905117706048': 'TYN', '848646370698': 'TYN-DEV', '831150022978': 'URX', '031826323264': 'URX-DEV', '288313784527': 'USR', '148176209732': 'USR-DEV', '014928871567': 'VAL', '910316543662': 'VAR', '461159204115': 'VAR-DEV', '801443527760': 'VHG', '617236244619': 'VRC', '591856689459': 'VSR', '176845980324': 'YTW', '459514715664': 'YTW-DEV', '412205967970': 'ZMG', '489682343983': 'ZMG-DEV', '059758761858': 'ZMGC', '404286454561': 'MASH', '525989141826': 'ZD'}

    lines = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    user_to_shortcode_policy = {'+': {}, '-': {}}
    shortcode = ""
    policy_name = ""
    user_names_plus = []
    user_names_minus = []
    for line in lines:
        line = line.rstrip()
        if line.startswith("diff --git"):
            if (len(user_names_plus) != 0):
                for user_name in user_names_plus:
                    if user_name in user_to_shortcode_policy:
                        user_to_shortcode_policy['+'][user_name].append([shortcode, policy_name])
                    else:
                        user_to_shortcode_policy['+'][user_name] = [[shortcode, policy_name]]
            if (len(user_names_minus) != 0):
                for user_name in user_names_minus:
                    if user_name in user_to_shortcode_policy:
                        user_to_shortcode_policy['-'][user_name].append([shortcode, policy_name])
                    else:
                        user_to_shortcode_policy['-'][user_name] = [[shortcode, policy_name]]
            shortcode = ""
            policy_name = ""
            user_names_plus = []
            user_names_minus = []

            # check the file names are the same
            args = line.split(' ')
            a = args[2][1:]
            b = args[3][1:]
            if (a == b):
                #print(a)
                if (a.startswith('/legacy')):
                    # list_a[2] will be the accountID
                    # get the shortcode from dict
                    accountID = a.split('/')[2].strip()
                    shortcode = accountID_to_shortcode[accountID]
                    policy_name = "\"" + a.split('/')[-1].rstrip('.yml').strip() + "\""
        elif line.startswith("+  -"):
            user_names_plus.append(line[4:].strip())
        elif line.startswith("-  -"):
            user_names_minus.append(line[4:].strip())

        # most likely it is in /privileges
        elif line[0] == '+' and line[1] != ' ' and line[1] != '+' and len(line.split(' ')) == 3:
            user_name = line[1:].split(' ')[0].strip()
            accountID = line[1:].split(' ')[1].strip()
            shortcode = accountID_to_shortcode[accountID]
            policy_name = "\"" + line[1:].split(' ')[2].strip() + "\""
            if user_name in user_to_shortcode_policy['+']:
                user_to_shortcode_policy['+'][user_name].append([shortcode, policy_name])
            else:
                user_to_shortcode_policy['+'][user_name] = [[shortcode, policy_name]]

        elif line[0] == '-' and line[1] != ' ' and line[1] != '-' and len(line.split(' ')) == 3:
            user_name = line[1:].split(' ')[0].strip()
            accountID = line[1:].split(' ')[1].strip()
            shortcode = accountID_to_shortcode[accountID]
            policy_name = "\"" + line[1:].split(' ')[2].strip() + "\""
            if user_name in user_to_shortcode_policy['-']:
                user_to_shortcode_policy['-'][user_name].append([shortcode, policy_name])
            else:
                user_to_shortcode_policy['-'][user_name] = [[shortcode, policy_name]]
    return user_to_shortcode_policy
    
def generated_statements(user_to_shortcode_policy , statement, flag = None, print_out = True):
    """
    :param user_to_shortcode_policy: return value of parse_diff() function
    :param statement: a valid proximo statement
    :param flag:
        '+' or '-' or None, when flag = None, will apply to both '+' and '-'
        '+' means user added to .diff
        '-' means user removed from .diff
    :return:
    """
    proximo_statements = {"create-user", "setup-mfa", "remove-mfa", "reset-password", "remove-credentials", "create-role", "delete-role",
         "delete-instance-roles", "dump", "list-attachments", "attach-policy", "detach-policy", "clone-role", "apply",
         "terminate"}

    flags = {'+', '-', '+-'}
    if statement not in proximo_statements:
        print("Please give a valid proximo statement")
        print(proximo_statements)
        return None

    if flag == None:
        flag = '+-'
    if flag not in flags:
        print("Please give a valid flag, flag can only be '+', '-', or no flags, means both '+' and '-'")

    # just a visual reminder
    if len(user_to_shortcode_policy['+']) > 0:
        print("has plus + in .diff")
    if len(user_to_shortcode_policy['-']) > 0:
        print("has minus - in .diff")

    if statement == "create-role":
        if flag == '-':
            print("Can't create roles when flag is '-")
            return None
        role_to_shortcode = {}
        generated_statements = []
        for role_name in user_to_shortcode_policy['+'].keys():
            for item in user_to_shortcode_policy['+'][role_name]:
                if role_name not in role_to_shortcode.keys():
                    role_to_shortcode[role_name] = {item[0]}
                else:
                    role_to_shortcode[role_name].add(item[0])
        for role_name in role_to_shortcode.keys():
            string_shortcodes = ""
            for i in role_to_shortcode[role_name]:
                string_shortcodes += i + " "
            generated_statements.append("aws-assume usr proximo create-role --account " + string_shortcodes + " --role-name " + role_name)

        if print_out == True:
            for stmt in generated_statements:
                print(stmt)
        return generated_statements

    limited_proximo_statements = {"attach-policy", "detach-policy", "apply"}
    if statement in limited_proximo_statements:
        generated_statements = []
        selected_user_to_shortcode_policy = {}
        if flag == '+' or flag == '+-':
            selected_user_to_shortcode_policy.update(user_to_shortcode_policy['+'])
        if flag == '-' or flag == '+-':
            selected_user_to_shortcode_policy.update(user_to_shortcode_policy['-'])

        for role_name in selected_user_to_shortcode_policy.keys():
            for item in selected_user_to_shortcode_policy[role_name]:
                generated_statements.append("aws-assume usr proximo " + statement + " --account " + item[0] + " --policy-name " + item[1] + " --role-name " + role_name)

        if print_out == True:
            for stmt in generated_statements:
                print(stmt)
        return generated_statements


if __name__ == '__main__':
    #lines = read_file("./files/895.diff")
    #accountID_to_shortcode = create_accountID_to_shortcode_dict('./files/accountID_shortcode.txt')
    user_to_shortcode_policy = parse_diff("./files/895.diff")
    #user_to_shortcode_policy = parse_diff("./files/897.diff")
    #print(user_to_shortcode_policy)
    generated_statements(user_to_shortcode_policy, "create-role")
    print("--------------------------------\n")
    generated_statements(user_to_shortcode_policy, "apply")

