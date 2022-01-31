import js_properties
import js_globals
import subprocess
import os

bat_run_dir = '/cdrive/f_drive'


def get_file_from_remote(remote_file, local_file):
    cmd = 'ssh -p 22 -o StrictHostKeyChecking=no -o ControlPersist=60s -o ServerAliveInterval=30 -i ' \
          + js_globals.keys_dir + '/' + js_properties.key_file + ' -o PasswordAuthentication=no vxuser@' \
          + js_properties.controller_ip + ' dd if=' + remote_file + ' | dd of=' + local_file

    print(cmd)
    run_ssh = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    run_ssh.communicate()


def put_file_on_remote(remote_file, local_file):
    if os.path.exists(local_file) is False:
        print("Cannot copy file " + local_file + ", it does not exist")
        return False
    else:
        cmd = 'dd if=' + local_file + ' | ssh -p 22 -o StrictHostKeyChecking=no -o ControlPersist=60s -o ' \
                                      'ServerAliveInterval=30 -i ' + js_globals.keys_dir + '/' + js_properties.key_file + \
              ' -o PasswordAuthentication=no vxuser@' + js_properties.controller_ip + \
              ' dd of=' + remote_file
        print(cmd)
        run_ssh = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        run_ssh.communicate()


def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print('File ' + filename + ' removed!')


def delete_file_from_remote(filename):
    props = {
        'key_file': js_globals.keys_dir + '/' + js_properties.key_file,
        'user': 'vxuser',
        'ip': js_properties.controller_ip,
        'file': filename
    }
    cmd = 'ssh -p 22 -o StrictHostKeyChecking=no -o ControlPersist=60s -o ServerAliveInterval=30 -i {key_file} -o ' \
          'PasswordAuthentication=no {user}@{ip} rm {file}'.format(**props)
    print(cmd)
    try:
        run_ssh = subprocess.check_output([cmd], shell=True)
    except subprocess.CalledProcessError as e:
        run_ssh = e.output
    print('output of %s' % run_ssh)


def search_file_for_text(filename, text):
    f = open(filename,  'r', encoding='ISO-8859-1')
    for x in f:
        if x.__contains__(text):
            return True
        # print(x)
    return False


def get_file_contents(filename):
    file = open(filename, 'r')
    whole_file = file.read()
    file.close()
    return whole_file


def update_file_with_text(filename, text):
    delete_file(filename)
    with open(filename, "w") as f:
        f.write(text)
    f.close()


def create_bat(bat_command, bat_name, output_string='>'):
    # create bat file
    props = {
        'key_file': js_globals.keys_dir + '/' + js_properties.key_file,
        'user': 'vxuser',
        'ip': js_properties.controller_ip,
        'bat_command': bat_command,
        'bat_name': bat_name,
        'output_string': output_string
    }
    cmd = 'ssh -p 22 -o StrictHostKeyChecking=no -o ControlPersist=60s -o ServerAliveInterval=30 -i {key_file} -o ' \
          'PasswordAuthentication=no {user}@{ip} "echo {bat_command} {output_string} {bat_name}"'.format(**props)
    print(cmd)
    try:
        run_ssh = subprocess.check_output([cmd], shell=True)
    except subprocess.CalledProcessError as e:
        run_ssh = e.output
    print('output of %s' % run_ssh)
    # make bat file executable
    cmd = 'ssh -p 22 -o StrictHostKeyChecking=no -o ControlPersist=60s -o ServerAliveInterval=30 -i {key_file} -o ' \
          'PasswordAuthentication=no {user}@{ip} chmod +x {bat_name}'.format(**props)
    print(cmd)
    try:
        run_ssh = subprocess.check_output([cmd], shell=True)
    except subprocess.CalledProcessError as e:
        run_ssh = e.output
    print('chmod output of %s' % run_ssh)


def execute_bat(bat_name):
    passed = True
    props = {
        'key_file': js_globals.keys_dir + '/' + js_properties.key_file,
        'user': 'vxuser',
        'ip': js_properties.controller_ip,
        'bat_name': bat_name,
    }
    cmd = 'ssh -p 22 -o StrictHostKeyChecking=no -o ControlPersist=60s -o ServerAliveInterval=30 -i {key_file} -o ' \
          'PasswordAuthentication=no {user}@{ip} {bat_name}'.format(**props)
    print(cmd)
    try:
        run_ssh = subprocess.check_output([cmd], shell=True)
        print('Batch file ran successfully')
    except subprocess.CalledProcessError as e:
        print('Exception caught')
        run_ssh = e.output
        passed = False
    print('bat execute output of %s' % run_ssh)
    print('Returning %s' % str(passed))
    return passed


def copy_tlog_to_f(last_letter):
    bat_file = '%s/%s' % (bat_run_dir, 'copytlog.bat')
    tlog_file = "c:/adx_idt4/eamtran" + last_letter + '.dat'
    if last_letter == 'suspend':
        tlog_file = "c:/adx_idt4/eamsrtrx.dat"
    create_bat('copy "' + tlog_file + ' f:/tlog.dat"', bat_file)
    execute_bat(bat_file)


def copy_receipts_to_controller(receipt_num):
    bat_file = '%s/%s' % (bat_run_dir, 'getReceipts.bat')
    props = {
        'receipts_dir': 'f:/adxetc/ext/xpd/config/print_templates/virtual/',
        'sit_auth': js_properties.adxsitql_auth,
        'store_number': js_properties.store_number,
        'terminal': js_properties.terminal,
    }
    bat_base = 'adxsitql -get -auth:{sit_auth} t{store_number}{terminal} {receipts_dir}'.format(**props)
    for i in range(1, receipt_num + 1):
        bat_command = bat_base + 'Receipt-' + str(i) + '.html'
        create_bat(bat_command, bat_file, '>>')
    bat_command = 'adxsitql -get -auth:{sit_auth} t{store_number}{terminal} {receipts_dir}/barcode.png'.format(**props)
    create_bat(bat_command, bat_file, '>>')
    execute_bat(bat_file)


def delete_receipts_from_terminal():
    bat_file = '%s/%s' % (bat_run_dir, 'delReceipts.bat')
    props = {
        'receipts_dir': 'f:/adxetc/ext/xpd/config/print_templates/virtual/',
        'sit_auth': js_properties.adxsitql_auth,
        'store_number': js_properties.store_number,
        'terminal': js_properties.terminal,
    }
    bat_command = 'adxsitql -del -auth:{sit_auth} t{store_number}{terminal} {receipts_dir}*.html'.format(**props)
    create_bat(bat_command, bat_file)
    execute_bat(bat_file)
    delete_file_from_remote(bat_file)


def count_receipts_on_terminal():
    num_receipts = 0
    bat_file = '%s/%s' % (bat_run_dir, 'countReceipts.bat')
    props = {
        'receipts_dir': 'f:/adxetc/ext/xpd/config/print_templates/virtual/',
        'sit_auth': js_properties.adxsitql_auth,
        'store_number': js_properties.store_number,
        'terminal': js_properties.terminal,
    }
    bat_base = 'adxsitql -get -auth:{sit_auth} t{store_number}{terminal} {receipts_dir}'.format(**props)
    for i in range(1, 5):
        print('Trying to get receipt %s' % i)
        bat_command = bat_base + 'Receipt-' + str(i) + '.html'
        create_bat(bat_command, bat_file, '>')
        if not execute_bat(bat_file):
            num_receipts = i - 1
            break
    return num_receipts
