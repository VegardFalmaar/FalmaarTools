import numpy as np
import re


class Table:
    def __init__(self, data, delimiter=' '):
        if isinstance(data, list):
            self.data = data
        elif isinstance(data, str):
            self.read_from_file(data, delimiter)
        self.endline = r'    \\ \hline'

    def read_from_file(self, fname, delimiter):
        tab = [[]]
        with open(fname, 'r') as infile:
            line = infile.readline()[:-1]
            if delimiter == ' ':
                line = line.split()
            else:
                line = line.split(delimiter)
            tab[0] = line
            for line in infile:
                line = line[:-1]
                if delimiter == ' ':
                    line = line.split()
                else:
                    line = line.split(delimiter)
                tab.append(line)
        self.data = tab


    def transpose(self):
        tab = [
            [self.data[j][i] for j in range(len(self.data))]
            for i in range(len(self.data[0]))
        ]
        self.data = tab

    def latex(self, filename='print', complete=False, extra_separator=None):
        """Print or save to file a latex formatted table."""
        try:
            data = self.data
        except (TypeError, AttributeError):
            print('No table was written or printed')
            print('Initialize Table instance with table data first.')
            return

        if extra_separator == None:
            extra_separator = []

        width = len(data[0])
        out = self.texHeader(width, complete=complete)
        for i, line in enumerate(data):
            endl = self.endline
            if i in extra_separator:
                endl += r' \hline'
            out.append(' & '.join(line) + endl)
        out += self.texFooter(complete=complete)
        if filename == 'print':
            for line in out:
                print(line)
        else:
            with open(filename, 'w') as outfile:
                for line in out:
                    outfile.write(line + '\n')

    def texHeader(self, width, complete=False):
        if complete:
            out = [r'\begin{table}  %[p] % Uncomment to put table in Appendix',
                    r'\begin{adjustbox}{width=\linewidth}']
        else:
            out = []

        out += [r'\begin{tabular}{||c | ' + '{:s}'.format('c | '*(width-2)) + r'c||}',
                r'\hline']
        return out

    def texFooter(self, complete=False):
        out = [r'\end{tabular}']
        if complete:
            out += [r'\end{adjustbox}',
                r'\caption{}',
                r'\label{}',
                r'\end{table}']
        return out

    def write(self, filename='print', header=True):
        """Print or save to file a good old-fashioned table."""
        try:
            data = self.data
        except (TypeError, AttributeError):
            print('No table was written or printed.')
            print('Initialize Table instance with table data first.')
            return
        bins = np.zeros(len(data[0]))
        for i in range(len(bins)):
            column = [data[j][i] for j in range(len(data))]
            bins[i] = len(max(column, key=len))+4
        out = []
        for i in range(len(data)):
            line = ''
            for j in range(len(data[i])):
                line += '|{:{align}{width}}'.format(data[i][j], align='^', width=str(int(bins[j])))
            line += '|'
            out.append(line)
        out.insert(0, '-'*len(line))
        if header:
            out.insert(2, '|' + '-'*(len(line)-2) + '|')
        out.append('-'*len(line))
        if filename == 'print':
            for line in out:
                print(line)
        else:
            with open(filename, 'w') as outfile:
                for line in out:
                    outfile.write(line + '\n')


class Matrix(Table):
    def __init__(self, data):
        Table.__init__(self, data)
        self.endline = r'    \\'

    def texHeader(self, width, complete=False):
        if complete:
            out = [r'\begin{equation}{}',
                    r'\bm NAME = \begin{pmatrix}']
        else:
            out = [r'\begin{pmatrix}']
        return out

    def texFooter(self, complete=False):
        if complete:
            out = [r'\end{pmatrix}',
                    r'\end{equation}']
        else:
            out = [r'\end{pmatrix}']
        return out


def tex_std_form(num: str) -> str:
    """Replace calculator notation for standard form"""
    # remove e+00
    num = num.replace('e+00', '')
    # match digit followed by e, optional minus and digits
    pattern = r'(\d)e(-?\+?\d+)'
    num = re.sub(pattern, r'\1 \\cdot 10^{\2}', num)
    # remove leading + and 0
    num = num.replace(r'10^{+', r'10^{')
    num = num.replace(r'10^{0', r'10^{')
    num = num.replace(r'10^{-0', r'10^{-')
    return num


if __name__ == '__main__':
    A = np.random.uniform(size=(5, 4))
    data = [['{:.4f}'.format(num) for num in row] for row in A]

    mat = Matrix(data)
    mat.latex(filename='print')

    print()
    data.insert(0, ['Vec {}'.format(i+1) for i in range(4)])
    mat = Matrix(data)
    mat.write(filename='print')

    print()
    data[0] = ['Col {}'.format(i+1) for i in range(4)]
    tab = Table(data)
    tab.latex(filename='print', complete=True)
    print()
    tab.write(filename='print')
    tab.transpose()
    tab.write()
