import sys, os, subprocess

#Get virtualenv if not already present
try:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'virtualenv'])
except subprocess.CalledProcessError:
    try:
        subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'virtualenv'])
    except subprocess.CalledProcessError:
        print('pip not found')
        sys.exit()


import virtualenv.run as vrun

#Get path of repository (where this script is located)
repo_path = os.path.dirname(os.path.abspath(__file__))

#Get the path to where the env should be (or will be)
env_path = os.path.join(repo_path, 'ReactComboEnv')

#Create env if it doesn't exist
if not os.path.exists(env_path):
    vrun.cli_run(['ReactComboEnv'])

#Activate the env
activate_this = os.path.join(env_path, 'bin', 'activate_this.py')
code = compile(open(activate_this).read(), activate_this, 'exec')
exec(code, dict(__file__=activate_this))

#subprocess.run([sys.executable, '-m', 'pip', 'install', 'trueskill'])
import pip
#pip.main(['install', '--prefix', 'env_path', 'trueskill'])
subprocess.check_call([sys.executable, '-m', 'pip', 'install',  \
    '--no-warn-script-location', '--ignore-installed', '--prefix', \
    'ReactComboEnv', '-r', 'requirements.txt'])

print('\n\nDone!')

