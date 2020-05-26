import ast, socket, re, sys, argparse, os, subprocess
from pprint import pprint
from urllib.parse import urlparse

class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.imports = []
        self.vars = []
        self.strings = []
        self.subscripts = []
        self.calls = []
        self.attrs = []
        self.assign = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        self.vars.append(node)
        self.generic_visit(node)

    def visit_Str(self, node):
        self.strings.append(node)
        self.generic_visit(node)

    def visit_Subscript(self, node):
        self.subscripts.append(node)
        self.generic_visit(node)

    def visit_Call(self, node):
        self.calls.append(node)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.attrs.append(node)
        self.generic_visit(node)

    def visit_Assign(self, node):
        self.assign.append(node)
        self.generic_visit(node)

def detectSmell(input):
    dump = open('smell-updated0000.csv', 'a')
    try:
        with open(f'/home/brokenquark/Workspace/ICSME19/gist-src/{input}', "r") as source:
            tree = ast.parse(source.read())
    except:
        print(f'failure parsing {input}')
        subprocess.call(f'rm /home/brokenquark/Workspace/ICSME19/gist-src/{input}', shell=True)
        return 1

    analyzer = Analyzer()
    analyzer.visit(tree)

    hardcodedSecretWords = ['key','id', 'cert', 'root','passno','pass-no', 'pass_no', 'auth_token', 'authetication_token','auth-token', 'authentication-token', 'user', 'uname', 'username', 'user-name', 'user_name', 'owner-name', 'owner_name', 'owner', 'admin', 'login', 'pass', 'pwd', 'password', 'passwd', 'secret', 'uuid', 'crypt', 'certificate', 'userid', 'loginid', 'token', 'ssh_key', 'md5', 'rsa', 'ssl_content', 'ca_content', 'ssl-content', 'ca-content', 'ssh_key_content', 'ssh-key-content', 'ssh_key_public', 'ssh-key-public', 'ssh_key_private', 'ssh-key-private', 'ssh_key_public_content', 'ssh_key_private_content', 'ssh-key-public-content', 'ssh-key-private-content']
    hardcodedPasswords = ['pass', 'pwd', 'password', 'passwd', 'passno', 'pass-no', 'pass_no']

    hardcoded_pass_found = 0

    for var in analyzer.assign:
        for item in hardcodedPasswords:
            if isinstance(var.targets[0], ast.Name) and isinstance(var.value, ast.Str):
                if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()),
                            str(var.targets[0].id).lower().strip()):
                    if len(var.value.s) > 0:
                        hardcoded_pass_found += 1
                        print(input)
            if isinstance(var.targets[0], ast.Attribute) and isinstance(var.value, ast.Str):
                if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()),
                            str(var.targets[0].attr).lower().strip()):
                    if len(var.value.s) > 0:
                        hardcoded_pass_found += 1
                        print(input)
            if isinstance(var.targets[0], ast.Subscript) and isinstance(var.value, ast.Str):
                if isinstance(var.targets[0].slice.value, ast.Str):
                    if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()),
                            str(var.targets[0].slice.value.s).lower().strip()):
                        if len(var.value.s) > 0:
                            hardcoded_pass_found += 1
                            print(input)


    for var in analyzer.assign:
        for item in hardcodedSecretWords:
            if isinstance(var.targets[0], ast.Name) and isinstance(var.value, ast.Str):
                if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()),
                            str(var.targets[0].id).lower().strip()):
                    if len(var.value.s) > 0: dump.write(f'{input}, hardcoded secret, {var.lineno}\n')
            if isinstance(var.targets[0], ast.Attribute) and isinstance(var.value, ast.Str):
                if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()),
                            str(var.targets[0].attr).lower().strip()):
                    if len(var.value.s) > 0: dump.write(f'{input}, hardcoded secret, {var.lineno}\n')
            if isinstance(var.targets[0], ast.Subscript) and isinstance(var.value, ast.Str):
                if isinstance(var.targets[0].slice.value, ast.Str):
                    if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()),
                            str(var.targets[0].slice.value.s).lower().strip()):
                        if len(var.value.s) > 0: dump.write(f'{input}, hardcoded secret, {var.lineno}\n')

    for var in analyzer.assign:
        for item in hardcodedPasswords:
            if isinstance(var.targets[0], ast.Name) and isinstance(var.value, ast.Str):
                if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()), str(var.targets[0].id).lower().strip()):
                    if var.value.s == '': dump.write(f'{input}, empty password, {var.lineno}\n')
            if isinstance(var.targets[0], ast.Attribute) and isinstance(var.value, ast.Str):
                if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()), str(var.targets[0].attr).lower().strip()):
                    if var.value.s == '': dump.write(f'{input}, empty password, {var.lineno}\n')
            if isinstance(var.targets[0], ast.Subscript) and isinstance(var.value, ast.Str):
                if isinstance(var.targets[0].slice.value, ast.Str):
                    if re.match(r'[_A-Za-z0-9-]*{text}\b'.format(text=str(item).lower()), str(var.targets[0].slice.value.s).lower().strip()):
                        if var.value.s == '': dump.write(f'{input}, empty password, {var.lineno}\n')

    for var in analyzer.vars:
        if var.id == 'DEBUG' or var.id == 'DEBUG_PROPAGATE_EXCEPTIONS':
            if any(x.lineno == var.lineno and x.s == 'True' for x in analyzer.strings):
                dump.write(f'{input}, DEBUG True in deployment, {var.lineno}\n')

    for value in analyzer.strings:
        download = ['iso', 'tar', 'tar.gz', 'tar.bzip2', 'zip', 'rar', 'gzip', 'gzip2', 'deb', 'rpm', 'sh', 'run', 'bin', 'exe', 'zip', 'rar', '7zip', 'msi', 'bat']
        try:
            parsedUrl = urlparse(str(value.s))
        except:
            parsedUrl = ''
        if len(parsedUrl) > 1:
            if re.match(
                    r'^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([_\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$',
                    str(value.s)):
                if ('http' in str(value.s).strip().lower() or 'www' in str(
                        value.s).strip().lower()) and 'https' not in str(value.s).strip().lower():
                    dump.write(f'{input}, use of http without tls, {value.lineno}\n')
                for item in download:
                    if re.match(r'(http|https|www)[_\-a-zA-Z0-9:\/.]*{text}$'.format(text=item), str(value.s)):
                        if 'hashlib' not in analyzer.imports and 'pygpgme' not in analyzer.imports:
                            dump.write(f'{input}, no integrity check\n')
            elif parsedUrl.scheme == 'http' or parsedUrl.scheme == 'https':
                if parsedUrl.scheme == 'http':
                    dump.write(f'{input}, use of http without tls, {value.lineno}\n')
                for item in download:
                    if re.match(r'(http|https|www)[_\-a-zA-Z0-9:\/.]*{text}$'.format(text=item), str(value.s)):
                        if 'hashlib' not in analyzer.imports and 'pygpgme' not in analyzer.imports:
                            dump.write(f'{input}, no integrity check, {value.lineno}\n')

    for item in analyzer.subscripts:
        if isinstance(item.value, ast.Attribute):
            if item.value.attr == 'argv':
                dump.write(f'{input}, use of shell arguments, {item.lineno}\n')

    for item in analyzer.calls:
        if isinstance(item.func, ast.Attribute):
            if item.func.attr == 'ArgumentParser' and item.func.value.id == 'argparse':
                dump.write(f'{input}, use of shell arguments, {item.lineno}\n')

    for item in analyzer.calls:
        if isinstance(item.func, ast.Attribute):
            if (item.func.attr == 'match' or item.func.attr == 'search' or item.func.attr == 'compile'):
                if isinstance(item.func.value, ast.Name):
                    if item.func.value.id == 're':
                        dump.write(f'{input}, use of regex, {item.lineno}\n')

    return hardcoded_pass_found
count = 0
for dirName, subdirList, fileList in os.walk('/home/brokenquark/Workspace/ICSME19/gist-src'):
    for fileName in fileList:
        count = count + detectSmell(fileName)

print(count)