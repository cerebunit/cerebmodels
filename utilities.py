# ~/utilities.py
import re

class UsefulUtils(object):

    @classmethod
    # https://stackoverflow.com/questions/4289331/python-extract-numbers-from-a-string
    def extract_key_id(cls, key):
        return [int(s) for s in re.findall(r'\d+', key)][0]

    @classmethod
    # https://stackoverflow.com/questions/10712002/create-an-empty-list-in-python-with-certain-size/33513257
    def create_empty_list(cls, size):
        return [None]*size

    @classmethod
    # https://stackoverflow.com/questions/5520580/how-do-you-get-all-classes-defined-in-a-module-but-not-imported
    def classesinmodule(cls,module):
        md = module.__dict__
        return [
            md[c] for c in md if (
                isinstance(md[c], type) and md[c].__module__ == module.__name__
            )
        ]

    @classmethod
    def check_not_None_in_arg(cls,args):
        for argname, argvalue in args.iteritems():
            if argvalue is None:
                raise ValueError( ", ".join(list(args.keys())) + " must be given.")

    @classmethod
    # https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
    def check_allNone_in_arg(cls,args):
        if len(set(list(args.values()))) != 1: # if all are not None
            raise ValueError( ", ".join(list(args.keys())) + " must all be given if one of them is given (i.e, one of them is NOT None.")
        # do nothing if all args are None

    @classmethod
    # https://stackoverflow.com/questions/5909873/how-can-i-pretty-print-ascii-tables-with-python
    def pprinttable(rows):
        if len(rows) > 1:
            headers = rows[0]._fields
            lens = []
            for i in range(len(rows[0])):
                lens.append(len(max([x[i] for x in rows] + [headers[i]],key=lambda x:len(str(x)))))
            formats = []
            hformats = []
            for i in range(len(rows[0])):
                if isinstance(rows[0][i], int):
                    formats.append("%%%dd" % lens[i])
                else:
                    formats.append("%%-%ds" % lens[i])
                hformats.append("%%-%ds" % lens[i])
            pattern = " | ".join(formats)
            hpattern = " | ".join(hformats)
            separator = "-+-".join(['-' * n for n in lens])
            print hpattern % tuple(headers)
            print separator
            _u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t
            for line in rows:
                print pattern % tuple(_u(t) for t in line)
        elif len(rows) == 1:
            row = rows[0]
            hwidth = len(max(row._fields,key=lambda x: len(x)))
            for i in range(len(row)):
                print "%*s = %s" % (hwidth,row._fields[i],row[i])
