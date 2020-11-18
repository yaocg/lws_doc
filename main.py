import os
import traceback
from optparse import OptionParser
from optparse import OptionGroup


class Dir(object):
    def __init__(self, name, desc=""):
        self.__name = name
        self.__desc = desc
        self.__sub_dirs = []

    def name(self):
        return self.__name

    def desc(self):
        return self.__desc

    def push_dir(self, one_dir):
        self.__sub_dirs.append(one_dir)

    def __iter__(self):
        for one_dir in self.__sub_dirs:
            yield one_dir

def anlyzeReadMeFile(readmefile):
    res = {}
    if not os.path.isfile(readmefile):
        return res

    with open(readmefile, "r") as rop:
        if not rop.readable():
            return res

        for oneline in rop.readlines():
            pos = oneline.find("|")
            if pos == -1 or pos == 0:
                continue

            res.update({oneline[0:pos]:oneline[pos+1:-1]})

    return res

def readPath(path):
    if not os.path.isdir(path):
        return [];

    if path[-1] != "/":
        path += "/"

    dir_list = []
    readme_dict = anlyzeReadMeFile(path+"README.md")
    paths = os.listdir(path)
    paths.sort()
    for str_path in paths:
        lp = path+str_path
        if not os.path.isdir(lp):
            continue

        one_dir = Dir(str_path, readme_dict.get(str_path, ""))
        for one in readPath(lp):
            one_dir.push_dir(one)
        dir_list.append(one_dir)

    return dir_list

def main(lws_path, lws_url):

    if lws_url and lws_url[-1] != "/":
        lws_url += "/"

    print("use lws path:", lws_path)
    print("use lws url:", lws_url)

    with open("lws.md", "w") as wop:
        # write Html head
        html_head = """# 示例代码\n""" \
                """<div style="overflow-x: auto; overflow-y: auto; height: 1000px; width:6000px;">\n""" \
                """<table id="table" border="1" align="left">\n""" \
                """<tbody>\n"""
        wop.write(html_head)

        # write table head
        all_line = 1
        for one in readPath(lws_path):
            all_line += 1
            for t in one:
                all_line += 1
        tb_head = """  <tr>\n""" \
                """    <td rowspan="{}"><a href="{}">示例代码</a></td>\n""" \
                """    <td>代码分类</td>\n""" \
                """    <td>代码示例</td>\n""" \
                """  </tr>\n""".format(all_line, lws_url)
        wop.write(tb_head)

        # write table lines
        for one in readPath(lws_path):
            colnum = 1
            notes = "\n\n\n  <!-- {} -->\n"
            tb_col2 = """  <tr>\n""" \
                    """    <td rowspan="{}"><a href="{}{}{}">{}</a>{}</td>\n""" \
                    """  </tr>\n"""
            tb_col3 = ""
            for two in one:
                colnum += 1
                tb_col3 += tb_col2.format(1, lws_url, one.name() + "/", two.name(), two.name(), "" if not two.desc() else " - "+two.desc())

            tb_col2 = tb_col2.format(colnum, lws_url, "", one.name(), one.name(), "" if not one.desc() else " - "+ one.desc())

            notes = notes.format(one.name())

            wop.write(notes)
            wop.write(tb_col2)
            wop.write(tb_col3)

        # write Html tail
        html_tail ="""</tbody>\n""" \
                """</table>\n""" \
                """</div>\n"""
        wop.write(html_tail)


    a = """<tr>""" \
            """<td><a href="https://libwebsockets.org/git/libwebsockets/tree/minimal-examples/"></a></td>""" \
            """</tr>"""



if __name__ == "__main__":
    usage = "usage: python3 main.py [options] arg"
    parser = OptionParser(usage=usage,description="command descibe")
    parser.add_option("-p", "--path", dest="path", help="lws minimal-examples path")
    parser.add_option("-u", "--url", dest="url", help="lws minimal-examples url")

    (options, args) = parser.parse_args()
    if options.path and options.url:
        main(options.path, options.url)
    else:
        parser.print_help()
