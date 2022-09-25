from pandas import read_csv
import tempfile, os, sys

from formats import Table


def main():
    if len(sys.argv) != 3:
        print('Please provide HTML title and input filename as arguments')
        sys.exit(1)

    path = os.getcwd()
    html_title, fname = sys.argv[1:]

    source = '/home/vegard/Dropbox/Skole/Priv/src/'

    df = read_csv(os.path.join(path, fname), keep_default_na=False)
    columns = {
        'Start Date': 'Dato',
        'Start Time': 'Starttid',
        'End Time': 'Sluttid',
        'Duration (h)': 'Varighet',
        'Description': 'Tema',
        'Billable Amount (NOK)': 'Beløp',
        'Task': 'Utbetaling',
    }

    # keep only what is interesting and rename the columns
    df = df[[key for key in columns]]
    df.rename(columns=columns, inplace=True)

    df['Dato'] = df['Dato'].str.replace(
        r'(\d\d)/(\d\d)/(\d\d\d\d)',
        lambda m: m.group(2) + '.' + m.group(1) + '.' + m.group(3),
        regex=True,
    )

    df['Utbetaling'] = df['Utbetaling'].str.replace(
        r'(\d\d\d\d)\.(\d\d)\.(\d\d)',
        lambda m: m.group(3) + '.' + m.group(2) + '.' + m.group(1),
        regex=True,
    )

    # change format of time to not include seconds
    for col in ['Starttid', 'Sluttid', 'Varighet']:
        df[col] = df[col].str.replace(
            r'(\d\d):(\d\d):(\d\d)',
            lambda m: m.group(1) + ':' + m.group(2),
            regex=True,
        )

    df['Utbetaling'] = df['Utbetaling'].str.replace(
        'Current',
        '-',
        regex=True,
    )

    tmp = tempfile.NamedTemporaryFile(suffix='.html')
    df.to_html(
        tmp.name,
        index=False,
        formatters={
            'Beløp': lambda flt: f'{flt:,.0f}'.replace(',', ' ') + ',-'
        }
    )

    with open(source + 'base.html', 'r') as infile:
        lines = infile.readlines()

    lines += ['<h1>' + html_title + '</h1>\n']

    with open(tmp.name, 'r') as infile:
        lines += [
            '<table border="1" class="dataframe" id="customers">'
            ] + infile.readlines()[1:]

    lines += ['</body>\n', '</html>\n']

    with open(os.path.join(path, fname.replace('.csv', '.html')), 'w') as outfile:
        for line in lines:
            outfile.write(line)
