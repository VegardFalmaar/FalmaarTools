import os
import csv


def get_client_details(client_id):
    clients_fname = '../clients.csv'
    with open(clients_fname, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        for client in reader:
            if client['id'] == client_id:
                return client
        raise ValueError('No client found')


def read_detail_file():
    details = {}
    with open('details.txt', 'r') as f:
        for line in f:
            key, value = line.split(':')
            details[key] = value.strip()
    return details


def create_information_tex():
    details = read_detail_file()
    client = get_client_details(details['client'])

    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    with open(os.path.join(src_dir, 'information_base.tex'), 'r') as f:
        content = f.read()

    replacements = {
        'insert_due': details['due'],
        'insert_project_name': details['project'],
        'insert_client_name': client['name'],
        'insert_client_org': f'Org. {client["org"]}' if client["org"] else '',
        'insert_street_address': client['street_address'],
        'insert_city_address': client['city_address'],
        'insert_email': client['email']
    }
    for original, replacement in replacements.items():
        content = content.replace(original, replacement)

    with open('../.tex/information.tex', 'w') as f:
        f.write(content)


def get_invoice_num():
    return os.getcwd().split('/')[-1]


def verify_dir_structure():
    valid = get_invoice_num().isdigit() and os.path.isdir('../.tex')
    if not valid:
        raise DirectoryStructureError


class DirectoryStructureError(Exception):
    def __str__(self):
        msg = 'Dir should be an invoice number. ' \
            + 'Parent dir should contain a ".tex" dir'
        return msg


def main():
    verify_dir_structure()
    create_information_tex()
    invoice_num = get_invoice_num()
    os.chdir('../.tex')
    command = r'pdflatex "\def\invoicenumberfromdirname{' \
        + invoice_num \
        + r'}\input{template}"'
    os.system(command)
    os.rename('template.pdf', f'../{invoice_num}/Faktura{invoice_num}.pdf')
