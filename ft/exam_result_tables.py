import os
import csv
import shutil
import argparse

from .formats import Table


def main():
    parser = argparse.ArgumentParser(
        description='Create a PDF with results for a test using LaTeX.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-s', '--short-format',
        action='store_true',
        help='Include only the total score, not the score on individual tasks.'
    )
    parser.add_argument(
        '--header',
        default='Fag år-år -- Prøve kap. 0',
        help='Header to be displayed on each page of the resulting PDF.'
    )
    parser.add_argument(
        'filename',
        type=str,
        nargs=1,
        help='Filename with tabulated test results.'
    )
    args = parser.parse_args()

    in_fname = args.filename[0]
    out_fname = create_output_fname(in_fname)

    temp_tex_source_dir = 'resultater-tex'
    if not os.path.isdir(temp_tex_source_dir):
        print(f'Creating directory {temp_tex_source_dir}')
        os.mkdir(temp_tex_source_dir)

    result_table = read_source_csv(in_fname, args.short_format)
    create_student_tex_files(temp_tex_source_dir, result_table)
    create_main_tex_and_compile(temp_tex_source_dir, out_fname, args.header)

    print(f'Removing directory {temp_tex_source_dir}')
    shutil.rmtree(temp_tex_source_dir)


def create_output_fname(in_fname: str):
    f_name, _ = os.path.splitext(in_fname)
    return f_name + '.pdf'


def read_source_csv(f_name: str, short_format: bool = False):
    if not os.path.isfile(f_name):
        raise FileNotFoundError(f'{f_name} is not a file')

    with open(f_name, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        table = [line for line in reader if line[-4] != '']
    cols_to_keep = [i for i in range(len(table[0]) - 2) if table[1][i] != ''] \
        + [len(table[0]) - 1]
    if short_format:
        cols_to_keep = [0] + cols_to_keep[-7:]
    table = [[table[i][j].replace('%', r'\%') for j in cols_to_keep]
             for i in range(len(table))]
    table[1][0] = 'Oppgave'
    table[2][0] = 'Mulige poeng'
    return table


def create_student_tex_files(temp_tex_dir: str, table):
    fnames = []
    header_rows = table[:3]
    for student in table[3:]:
        student_name = student[0]
        student_table = header_rows + [student]
        tab = Table(student_table)
        tab.transpose()
        fname = student_name.replace(' ', '_')
        fname = f'{fname}.tex'
        fnames.append(fname)
        num_rows = len(header_rows[0])
        tab.latex(
            os.path.join(temp_tex_dir, fname),
            extra_separator=[0, num_rows - 8, num_rows - 6, num_rows - 4]
        )

    with open(os.path.join(temp_tex_dir, 'student_list.tex'), 'w') as outfile:
        s = '\n' + r'\newpage' + '\n'
        outfile.write(s.join([r'\input{' + fname + '}' for fname in fnames]))


def create_main_tex_and_compile(
    temp_tex_dir: str,
    out_fname: str,
    header: str
):
    main_tex_fname = os.path.join(temp_tex_dir, 'poengfordeling.tex')
    if not os.path.isfile(main_tex_fname):
        current_dir = os.path.dirname(__file__)
        src_fname = os.path.join(current_dir, 'src/test-scores.tex')
        shutil.copyfile(src_fname, main_tex_fname)

    os.chdir(temp_tex_dir)
    command = r'pdflatex "\def\subjectheader{' \
        + header \
        + r'}\input{poengfordeling.tex}"'
    os.system(command)
    os.chdir('..')
    if os.path.isfile('./' + out_fname):
        print(f'File {out_fname} already exists. Aborting.')
    else:
        os.rename(
            os.path.join(temp_tex_dir, 'poengfordeling.pdf'),
            './' + out_fname
        )
