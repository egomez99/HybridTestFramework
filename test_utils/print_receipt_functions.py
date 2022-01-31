from os.path import join, dirname, realpath, exists
from os import mkdir
import js_properties
import file_helper
import js_globals
import base64
import imgkit
from shutil import copyfile
from re import compile


def take_screenshot(receipt_file_name):
    receipt_file = file_helper.get_file_contents(receipt_file_name)
    if receipt_file.__contains__('class="barcode"'):
        get_image_from_terminal('/cdrive/f_drive/adxetc/ext/xpd/config/print_templates/virtual/barcode.png')
        file_helper.get_file_from_remote('/cdrive/f_drive/adxetc/home/vxuser/barcode.png', 'barcode.png')
    receipt_file = receipt_file.replace(js_globals.test_object['receipt_url'],
                                        realpath(js_globals.test_object['image_location']))
    file_helper.update_file_with_text(receipt_file_name, receipt_file)
    imgkit.from_file(realpath(receipt_file_name), 'current_receipt.jpg')
    file_helper.delete_file('barcode.png')
    file_helper.delete_file('image.bmp')


def verify_screenshot():
    image_dir = join(js_globals.home_dir, 'resources/html_images')
    if not exists(image_dir):
        mkdir(image_dir)
    master_image = join(image_dir, js_globals.test_object['scenario_name'] + '.jpg')
    print('master image location is: ' + master_image)
    if exists(master_image):
        with open('current_receipt.jpg', "rb") as f:
            current_encoded_image = base64.b64encode(f.read()).decode('ASCII')
        with open(master_image, "rb") as f:
            previous_encoded_image = base64.b64encode(f.read()).decode('ASCII')
        copyfile('current_receipt.jpg', master_image + '.current')
        assert current_encoded_image == previous_encoded_image, 'Image generated from html receipt does not match ' \
                                                                'expected. Compare "' + master_image + '" to "' + \
                                                                master_image + '.current" to see the difference.'
        file_helper.delete_file(master_image + '.current')
    else:
        # no file exists yet to compare the generated html to, so we'll make this one the baseline
        print('No receipt image exists, so saving current as the master copy - no verification occurring')
        copyfile('current_receipt.jpg', master_image)
    file_helper.delete_file('current_receipt.jpg')


def verify_template_data():
    # print('data object is:')
    # print(js_globals.template_object['data'])
    number_format = 'computer'
    receipt_string = file_helper.get_file_contents('Receipt-1.html')
    receipt_iterator = iter(receipt_string.splitlines())
    template_iterator = iter(js_globals.template_object['data'].splitlines())
    active_iterator = template_iterator
    backup_iterator = template_iterator
    receipt_line = ''
    # fast forward to first div
    for line in receipt_iterator:
        if 'div' in line:
            receipt_line = line
            break
    print('first div is ' + receipt_line)
    receipt_div_line = retrieve_div_line(receipt_line)
    assert receipt_div_line[
               'name'] == 'receipt', 'Expected div id of receipt to be the first element in receipt, but it was not'
    receipt_line = next(receipt_iterator)
    template_line = ''
    active_list = False
    list_def = {'list_iterations': 0, 'new_name': ''}
    list_contents = []
    for line in template_iterator:
        if 'div' in line:
            template_line = line
            break
    while True:
        skip = False
        try:
            template_div_line = retrieve_div_line(template_line)
            print('template line is ' + template_line)
            receipt_div_line = retrieve_div_line(receipt_line)
            print('receipt_line is ' + receipt_line)
            if template_div_line is not {}:
                print('line type is ' + template_div_line['type'])
                if template_div_line['type'] is 'list':
                    skip = True
                    active_list = True
                    list_def = template_div_line
                    list_contents = create_sub_list(template_div_line['type'], 'end_list', template_iterator)
                    active_iterator = iter(list_contents)
                elif template_div_line['type'] is 'end_list':
                    skip = True
                    list_def['list_iterations'] = list_def['list_iterations'] + 1
                    if len(js_globals.test_object[list_def['name']]) > list_def['list_iterations']:
                        # we have more objects, need to cycle through the list again
                        print('setting iterator to beginning of list')
                        active_iterator = iter(list_contents)
                    else:
                        active_list = False
                        list_def = {'list_iterations': 0, 'new_name': ''}
                        list_contents = []
                        active_iterator = template_iterator
                        print('end of list, restoring template iterator')
                if template_div_line['type'] is 'setting':
                    skip = True
                    if template_div_line['name'] == 'number_format':
                        number_format = template_div_line['value']
                if template_div_line['type'] == 'if':
                    active_if = True
                    skip = True
                    if_contents = create_sub_list(template_div_line['type'], 'end_if', active_iterator)
                    if_line = template_div_line['value']
                    variable_before_dot = template_div_line['value'].split('.')[0]
                    # evaluate if to see if we need to process it
                    if template_div_line['value'].__contains__('.'):
                        print('variable before dot is ' + variable_before_dot + ' and list new name is ' + list_def[
                            'new_name'])
                        variable_after_dot = template_div_line['value'].split('.')[1].split('=')[0].strip()
                        if variable_before_dot == list_def['new_name']:
                            # translating the freemarker if statement to a python evaluatable statement
                            if_line = if_line.replace(variable_before_dot, list_def['name'])
                            variable_before_dot = list_def['name']
                            if_line = if_line.replace('.', '[' + str(list_def['list_iterations']) + ']')
                        if_line = if_line.replace(variable_after_dot, "['" + variable_after_dot + "']")
                    if_line = if_line.replace(variable_before_dot,
                                              "js_globals.test_object['" + list_def['name'] + "']")
                    if_line = if_line[:-1]
                    print('evaluating ' + if_line)
                    print('line evaluates to %s' % eval(if_line))
                    if eval(if_line):
                        backup_iterator = active_iterator
                        active_iterator = iter(if_contents)
                if template_div_line['type'] is 'end_if':
                    active_iterator = backup_iterator
                    active_if = False
                    skip = True
                if template_div_line['type'] is 'class':
                    print('class name is ' + template_div_line['name'])
                    if template_div_line['name'] == 'print-image':
                        receipt_line = next(receipt_iterator)
                        url = template_div_line['full_line'].split('url')[1].split('"')[1]
                        print('url is ' + url)
                        assert receipt_div_line[
                                   'name'] == 'print-image', 'Expected print-image tag but did not find it'
                        # receipt_div_line = retrieve_div_line(receipt_line)
                        receipt_url = receipt_line.split('img src')[1].split('"')[1]
                        assert url == receipt_url, 'Image url in template is ' + url + ', but image url on receipt is ' + receipt_url
                        get_image_from_terminal(receipt_url)
                        with open('image.bmp', "rb") as f:
                            encoded_image = base64.b64encode(f.read()).decode('ASCII')
                            assert encoded_image == js_globals.template_object[
                                'image'], 'Image on receipt does not match' \
                                          'image provided in template'
                        js_globals.test_object['receipt_url'] = receipt_url
                        receipt_line = next(receipt_iterator)
                        assert receipt_line == '<br>', 'Expected line break after image printed, but none found'
                        receipt_line = next(receipt_iterator)
                    elif template_div_line['name'] == 'line':
                        # need to get text outside of tags
                        template_text = template_line[template_line.find('>') + 1: template_line.rfind('<')]
                        all_vars = get_variables_from_line(template_text)
                        for i in range(len(all_vars)):
                            var_value = get_variable_value(all_vars[i], active_list, list_def)
                            if number_format == 'currency' and (
                                    isinstance(var_value, float) or isinstance(var_value, int)):
                                var_value = '${:,.2f}'.format(var_value)
                            template_text = template_text.replace(all_vars[i], str(var_value))
                        print('after calling function, template text is ' + template_text + '.')
                        if template_text is not '':
                            template_text = template_text.replace(' ', '&nbsp;')
                            print('text to print is ' + template_text)
                            assert receipt_line == '<div>' + template_text + '</div>'
                        receipt_line = next(receipt_iterator)
                    elif template_div_line['name'] == 'feed':
                        print('Entering feed verify')
                        assert receipt_line == '<br>', 'Expected line feed to print blank line, but not found in html'
                        # receipt_line = next(receipt_iterator)
                    elif template_div_line['name'] == 'barcode':
                        assert receipt_line == '<div class="barcode"></div>'
                        receipt_line = next(receipt_iterator)
                        barcode_data = ''
                        if 'data=' in template_div_line['full_line']:
                            barcode_data = template_div_line['full_line'].split('data=')[1].split('"')[1]
                        barcode_data = get_variable_value(barcode_data, active_list, list_def)
                        template_text = '<div>' + str(barcode_data) + '</div>'
                        assert template_text == receipt_line
                    elif template_div_line['name'] == 'feed-cut':
                        assert receipt_line == '<br><br>'
                        receipt_line = next(receipt_iterator)
                        assert receipt_line == '<div class="cut-block">'
                        receipt_line = next(receipt_iterator)
                        assert receipt_line == '<div >--&nbsp;--&nbsp;--&nbsp;--&nbsp;--&nbsp;Paper&nbsp;Cut&nbsp;--&nbsp;--&nbsp;--&nbsp;--&nbsp;--</div>'
                elif template_div_line['type'] is 'id':
                    template_css = get_css_section(template_div_line['name'],
                                                        js_globals.template_object['css'])
                    if template_css is not 'not_found':
                        receipt_css = get_css_section(template_div_line['name'], receipt_string)
                        assert template_css == receipt_css, 'Css section ' + template_div_line['name'] + ' was ' \
                                                            + template_css + ' in template but ' + receipt_css + ' in receipt'
                    else:
                        print('css section ' + template_div_line[
                            'name'] + ' not found in css, skipping verification in receipt')
                    print('receipt line is ' + receipt_line)
            if not skip:
                receipt_line, receipt_iterator = advance_iterator_to_valid_line(receipt_iterator)
            template_line, active_iterator = advance_iterator_to_valid_line(active_iterator)
        except StopIteration:
            print('Reached the end of an iterator')
            break


def retrieve_div_line(div_tag):
    if 'div id' in div_tag:
        return {'type': 'id', 'name': div_tag.split('div id')[1].split('"')[1], 'full_line': div_tag}
    elif 'div class' in div_tag:
        return {'type': 'class', 'name': div_tag.split('div class')[1].split('"')[1], 'full_line': div_tag}
    elif '<#list' in div_tag:
        return {'type': 'list', 'name': (div_tag.split('#list')[1]).split(' as ')[0].strip(),
                'new_name': div_tag.split(' as ')[1].split('>')[0].strip(), 'list_iterations': 0,
                'full_line': div_tag}
    elif '</#list' in div_tag:
        return {'type': 'end_list', 'full_line': div_tag}
    elif '<#setting' in div_tag:
        return {'type': 'setting', 'name': div_tag.split('#setting')[1].split('=')[0].strip(),
                'value': div_tag.split('=')[1].split('"')[1], 'full_line': div_tag}
    elif '<#if' in div_tag:
        return {'type': 'if', 'value': div_tag.split('<#if')[1].split('}')[0].strip(), 'full_line': div_tag}
    elif '</#if' in div_tag:
        return {'type': 'end_if', 'full_line': div_tag}
    else:
        return {}


def get_next_receipt_line(receipt_lines):
    return receipt_lines


def get_variable_value(text, list=False, list_def={}):
    name = text[2: len(text) - 1]
    print('variable name is ' + name)
    if '.' in name:
        before_dot = name[:name.find('.')]
        after_dot = name[name.find('.') + 1:]
        if before_dot == list_def['new_name']:
            # we're in a list, so we need to translate the variable name
            before_dot = list_def['name']
            print('before dot is ' + before_dot + ' and after dot is ' + after_dot)
            full_var = js_globals.test_object[before_dot][list_def['list_iterations']][after_dot]
        else:
            print('before dot is ' + before_dot + ' and after dot is ' + after_dot)
            full_var = js_globals.test_object[before_dot][after_dot]
        return full_var
    else:
        return js_globals.test_object[name]


def advance_iterator_to_valid_line(iterator):
    # print('current line is ' + current_line.strip())
    current_line = next(iterator)
    stripped_line = current_line.strip()
    while stripped_line == '</div>' or stripped_line == '' or stripped_line == '</body>' or stripped_line == '</html>':
        print('skipping line ' + current_line)
        current_line = next(iterator)
        stripped_line = current_line.strip()
    return current_line, iterator


def create_sub_list(input, end_tag, iterator):
    sub_contents = []
    while input is not end_tag:
        template_line, iterator = advance_iterator_to_valid_line(iterator)
        template_div_line = retrieve_div_line(template_line)
        sub_contents.append(template_div_line['full_line'])
        input = template_div_line['type']
        print('adding ' + template_div_line['full_line'] + ' to sub list')
    return sub_contents


def get_css_section(css_name, css_location):
    if '#' + css_name in css_location:
        return js_globals.template_object['css'].split('#' + css_name)[1].split('}')[0].strip()
    else:
        return 'not_found'


def get_variables_from_line(template_line):
    all_vars = []
    var_num = template_line.count('${')
    temp_template_text = template_line
    for i in range(var_num):
        current_var = temp_template_text[temp_template_text.find('$'):temp_template_text.find('}') + 1]
        # var_text.append(read_from_variable(var_to_send, True, list_def['list_iterations']))
        # print('number format is ' + number_format)
        # if isinstance(var_text[i], float) and number_format == 'currency':
        #    var_text[i] = '$' + str(var_text[i])
        # print('setting var to ' + str(var_text[i]))
        temp_template_text = temp_template_text.replace(current_var, '')
        # current_var = current_var[1:-1]
        all_vars.append(current_var)
        # print('temp text is ' + temp_template_text)
        # template_text = template_text.replace(var_to_send, str(var_text[i]))
    return all_vars


def get_image_from_terminal(image_location):
    # convert linux path to 4690 path
    image_location = image_location.replace('/cdrive/f_drive', 'f:')
    props = {
        'image_location': image_location,
        'sit_auth': js_properties.adxsitql_auth,
        'store_number': js_properties.store_number,
        'terminal': js_properties.terminal
    }
    bat_base = 'adxsitql -get -auth:{sit_auth} t{store_number}{terminal} {image_location}'.format(**props)
    file_helper.create_bat(bat_base, '/cdrive/f_drive/getImage.bat')
    file_helper.execute_bat('/cdrive/f_drive/getImage.bat')
    image_name = image_location.split('/')[len(image_location.split('/')) - 1]
    file_helper.get_file_from_remote(image_name, 'image.bmp')


def generate_lotto_line(number_list):
    lotto_line = {}
    i = 1
    for num in number_list.split(','):
        lotto_line['num' + str(i)] = int(num)
        print('lotto number being added is %s' % lotto_line['num' + str(i)])
        i = i + 1
    return lotto_line


def compare_html_receipts_ignore_dynamic_data(reference_receipt, test_receipt):
    date_line = compile(r'^<div>\d{2}/\d{2}/\d{2}.*')
    total_line = compile(r'^<div>(?:&nbsp;){30,32}\d{1,4}\.\d{2}&nbsp;</div>')
    barcode_line = compile(r'<div class="barcode"></div>')
    reference = open(reference_receipt)
    test = open(test_receipt)
    reference_line = reference.readline()
    test_line = test.readline()
    line_no = 1

    skip_next = False
    while reference_line != '' or test_line != '':
        if not skip_next and not date_line.match(reference_line) and not total_line.match(reference_line) and \
                reference_line != test_line:
            print('Receipt lines do not match at line: %s' % line_no)
            print('Reference line: %s' % reference_line)
            print('Test line: %s' % test_line)
            return False
        elif skip_next:
            skip_next = False
        if barcode_line.match(reference_line):
            skip_next = True
        reference_line = reference.readline()
        test_line = test.readline()
        line_no += 1

    reference.close()
    test.close()
    return True
