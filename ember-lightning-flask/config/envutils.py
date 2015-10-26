# from https://gist.github.com/vlasovskikh/e8fe8e0a5c4a73048a09#file-envutils-py
# added env -i to strip out unwanted env vars.

import os
from subprocess import Popen, PIPE
import pickle


PYTHON_DUMP_ENVIRON = """\
import sys
import os
import pickle

data = pickle.dumps(os.environ)
stdout = os.fdopen(sys.stdout.fileno(), "wb")
stdout.write(data)
"""


def source_bash_file(path):
    bash_cmds = [
        "source '%s'" % path,
        "python -c '%s'" % PYTHON_DUMP_ENVIRON,
        ]
    p = Popen(['env','-i','bash', '-c', '&&'.join(bash_cmds)], stdout=PIPE)
    stdout, _ = p.communicate()
    if stdout:
        environ = pickle.loads(stdout)
        for k, v in environ.data.items():
            os.environ[k] = v
