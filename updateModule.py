# command: pyinstaller -F [filename].py

import subprocess, sys, glob, os, re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def printAction(action):
    showColorText(bcolors.OKGREEN, '\n#########################')
    showColorText(bcolors.OKGREEN, '#  ' + action)
    showColorText(bcolors.OKGREEN, '#########################\n')

def showColorText(color, text):
     print(color + text + bcolors.ENDC)

def set_pwd(path):
    printAction('set pwd')
    ### set pwd
    if getattr(sys, 'frozen', False):
        cwd = os.path.dirname(sys.executable)
    elif __file__:
        cwd = os.path.dirname(__file__)
    # cwd = os.path.dirname(os.path.abspath(__file__))

    # path = input('project path(tap enter to skip): ')
    path = path.replace(' ', '')
    
    if len(path) > 0:
        if os.path.isdir(path):
            cwd = path
        else:
            showColorText(bcolors.FAIL, '\nNo such file or directory:' + path + '\n')
            exit()

    os.chdir(cwd)
    # cwd = os.getcwd()
    print('pwd: %s' % cwd)

def find_podspec_file():
    printAction('get podspec filename')
    count = 0
    for filename in glob.glob('*.podspec'):
        count += 1
        
    if count == 1:
        lines = list(open(filename, 'r'))
        for line in lines:
            if 's.version' in line:
                break

        m = re.search('\'(.+?)\'', line)
        if m:
            version = m.group(1)
        else:
            showColorText(bcolors.FAIL, 'version not found')
            exit()
        
        return filename, version
    else:
        showColorText(bcolors.FAIL, 'please check .podspec !!!\n')
        exit()

def setupSSH(ssh_path):
    printAction('add SSH')
    # ssh_path = input('enter your SSH path: ')
    ssh_path = ssh_path.replace(' ', '')
    # print(ssh_path)
    # print(os.path.isfile(ssh_path))
    if os.path.isfile(ssh_path):
        subprocess.call('ssh-add %s' % ssh_path, shell=True)
    else:
        showColorText(bcolors.FAIL, 'can not find file: %s' % ssh_path)
        exit()

def get_last_git_command():
    return subprocess.check_output(['git', 'log', '-1', '--pretty=%B'], shell=False).decode()

def add_tag_do_push(version):
    command = get_last_git_command()
    #command 自己會換行
    printAction('add tag \nversion: %s \ncommand: %s' % (version, command)) 
    
    retcode = subprocess.call(['git', 'tag', '-a', version, '-m', command])
    if retcode != 0:
        c = input('\nContinue: Push tag to remote? (Y/N) ')
        
        if c.upper() == 'N':
            showColorText(bcolors.FAIL, 'exit')
            sys.exit(retcode)
        else:
            print('SKIP: add tag to local')

    printAction('Push tag to remote') 
    retcode = subprocess.call(['git', 'push', 'origin', version])
    if retcode != 0:
        sys.exit(retcode)
            
    
def main(path, ssh_path):
    ### clear terminal
    # subprocess.call('reset', shell=True)

    ### set pwd
    set_pwd(path=path)

    setupSSH(ssh_path=ssh_path)

    ### find .podspec
    filename, version = find_podspec_file()

    add_tag_do_push(version)

    printAction('clear pod cache')
    subprocess.call(['pod','cache','clean', '--all'])

    printAction('run pod repo push --allow-warnings')
    subprocess.call(['pod','repo','push','--allow-warnings','104cac-specs',filename,'--verbose'])

    printAction('Done!!!')

if __name__ == "__main__":
    main()