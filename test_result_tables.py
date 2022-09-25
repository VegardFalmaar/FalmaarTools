import sys, os, csv, shutil, argparse

from .formats import Table


def main():
    parser = argparse.ArgumentParser(
        description='Create a LaTeX source file with results for a test.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-s', '--short-format',
        action='store_true',
        help='Include only the total score, not the score on individual tasks.'
    )
    parser.add_argument(
        'filename',
        type=str,
        nargs=1,
        help='Filename with tabulated test results.'
    )
    args = parser.parse_args()
    in_f_name = args.filename[0]
    if not os.path.isfile(in_f_name):
        raise FileNotFoundError(f'{in_f_name} is not a file')

    path = 'resultater-tex'
    if not os.path.isdir(path):
        print(f'Creating directory {path}')
        os.mkdir(path)

    with open(in_f_name, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        table = [line for line in reader if line[-4] != '']
    cols_to_keep = [i for i in range(len(table[0]) - 2) if table[1][i] != ''] + [len(table[0]) - 1]
    if args.short_format:
        cols_to_keep = [0] + cols_to_keep[-7:]
    table = [[table[i][j].replace('%', '\%') for j in cols_to_keep] for i in range(len(table))]

    fnames = []
    header_rows= table[:3]
    header_rows[1][0] = 'Oppgave'
    header_rows[2][0] = 'Mulige poeng'
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
            os.path.join(path, fname),
            extra_separator=[0, num_rows - 8, num_rows - 6, num_rows - 4]
        )

    with open(os.path.join(path, 'student_list.tex'), 'w') as outfile:
        s = '\n' + r'\newpage' + '\n'
        outfile.write(s.join([r'\input{' + fname + '}' for fname in fnames]))

    main_tex_fname = os.path.join(path, 'poengfordeling.tex')
    if not os.path.isfile(main_tex_fname):
        current_dir = os.path.dirname(__file__)
        src_fname = os.path.join(current_dir, 'src/test-scores.tex')
        shutil.copyfile(src_fname, main_tex_fname)

    print(f'TeX files done! Move into the {path}/ directory')
    print('and run "pdflatex poengfordeling.tex" to compile.')

    os.chdir(path)
    os.system('pdflatex poengfordeling.tex')
    os.system('pdflatex poengfordeling.tex')
    os.chdir('..')
    os.rename(os.path.join(path, 'poengfordeling.pdf'), './poengfordeling.pdf')
    shutil.rmtree(path)
