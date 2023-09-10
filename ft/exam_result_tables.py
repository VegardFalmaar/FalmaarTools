import os
import csv
import shutil
import argparse
from typing import List, Union

from .formats import Table


def main():
    parser = argparse.ArgumentParser(
        description='Create a PDF with results for a test using LaTeX.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-s', '--short-format',
        action='store_true',
        default=False,
        help='Include only the total score, not the score on individual tasks.'
    )
    parser.add_argument(
        '--keep-tex',
        action='store_true',
        default=False,
        help='Keep tex files after compilation.'
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

    result_table = prepare_raw_table(
        read_source_csv(in_fname),
        args.short_format
    )
    create_student_tex_files(temp_tex_source_dir, result_table)
    create_main_tex_and_compile(temp_tex_source_dir, out_fname, args.header)

    if not args.keep_tex:
        print(f'Removing directory {temp_tex_source_dir}')
        shutil.rmtree(temp_tex_source_dir)


def create_output_fname(in_fname: str):
    f_name, _ = os.path.splitext(in_fname)
    return f_name + '.pdf'


def columns_to_keep(table: List[List[str]], short_format: bool) -> List[int]:
    num_cols = len(table[0])
    # name and task scores, stop when totals are passed
    result = [i for i in range(num_cols - 7) if table[1][i] != '']
    if short_format:
        result = [0] + result[-6:]  # keep only name and total scores
    result += [
        num_cols - 6,   # grade
        num_cols - 1    # comment for student
    ]
    return result


def read_source_csv(f_name: str) -> List[List[str]]:
    if not os.path.isfile(f_name):
        raise FileNotFoundError(f'{f_name} is not a file')

    with open(f_name, 'r', encoding='UTF-8') as infile:
        reader = csv.reader(infile, delimiter='\t')
        return [line for line in reader if line[-9] != '']


def prepare_raw_table(
    table: List[List[str]],
    short_format: bool
) -> Union[List[List[str]], str]:
    cols = columns_to_keep(table, short_format)
    return [[row[i].replace('%', r'\%') for i in cols] for row in table]


def create_student_tex_files(temp_tex_dir: str, table):
    header_rows = [row[:-1] for row in table[:3]]   # drop comment field
    # remove percentages for totals scores on part 1 and 2
    header_rows[2][-4] = ''
    header_rows[2][-6] = ''

    fnames = []
    for student in table[3:]:
        student_name = student[0]
        student_table = header_rows + [student[:-1]]
        tab = Table(student_table)
        tab.transpose()
        fname = student_name.replace(' ', '_') + '.tex'
        fnames.append(fname)
        tex_fname = os.path.join(temp_tex_dir, fname)
        num_rows = len(header_rows[0])
        tab.latex(
            tex_fname,
            extra_separator=[0, num_rows - 8, num_rows - 6, num_rows - 4]
        )
        comment = student[-1]
        if comment:
            with open(tex_fname, 'a', encoding='UTF-8') as f:
                f.write('\n' + r'\vspace{1cm}' + r'\textbf{Kommentar:} ' + comment)

    with open(os.path.join(temp_tex_dir, 'student_list.tex'), 'w', encoding='UTF-8') as outfile:
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
