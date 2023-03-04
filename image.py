from os import path, listdir, makedirs, getcwd
from shutil import copy2
from re import sub
import argparse
import json
import textwrap
import subprocess

# Set containing directory for NewView's playlist
playlistsDir = r"C:\path\to\NeeView\Playlists"


def getPaths() -> list:
    if not args.tagname:
        return
    tagName = args.tagname.strip()
    # darn, why windows separates this with backslashes
    parentDir = sub(r"\\+$", "", args.parent.strip())
    PROCESS = (playlistsDir + r"\@@TAGNAME@@.nvpls",
               parentDir + r"\@@TAGNAME@@")
    processMapped = [x.replace("\\", "/")
                      .replace("@@TAGNAME@@", tagName)
                     for x in PROCESS]
    return processMapped


def ls() -> None:
    dirList = listdir(playlistsDir)
    print("", f"Listing {playlistsDir}...", sep="\n", end="\n\n  ")
    str = "\n  ".join((x.replace(".nvpls", "") for x in dirList))
    print(str, end="\n\n")


def readPlaylist(*, file: str) -> list:
    with open(file, 'r', encoding="utf-8_sig") as fp:
        jsonOpen = json.load(fp)
    copyList = [i["Path"] for i in jsonOpen["Items"]]
    return copyList


def copyEach(*, fileList: list, dest: str) -> None:
    counter = {
        "total": len(fileList),
        "i": 1
    }
    if not path.exists(dest):
        makedirs(dest)
    for src in fileList:
        progress = \
            f"({str(round(100 * (counter['i'] / counter['total']), 1))}%)"
        if not counter['i'] >= counter['total']:
            print(f"copying {path.basename(src)} ... {progress} ", end="\r")
        copy2(src, dest, follow_symlinks=True)
        counter['i'] += 1
    print(f"copying {path.basename(src)} ... finished {progress}", end="\n\n")


def run() -> None:
    jsonPath, destDir = getPaths()
    try:
        if not path.exists(jsonPath):
            errorMessage = \
                "error: " + \
                "the NeeView playlist for a tagname that you specified " + \
                "was not found"
            raise FileNotFoundError(errorMessage)
    except FileNotFoundError as e:
        print(e)
        return
    list = readPlaylist(file=jsonPath)

    MAX_RETRY = 2
    i = 1
    for _ in range(MAX_RETRY):
        try:
            if i == 1:
                print("", f"playlist from: {jsonPath}", sep="\n", end="\n")
                print(f"           to: {path.dirname(destDir)}", end="\n\n")
            copyEach(fileList=list, dest=destDir)
        except FileNotFoundError as e:
            print("making a new directory...", end="\n")
            makedirs(name=destDir, exist_ok=False)
            i += 1
        else:
            break
    else:
        print("failed to make a new directory")
        print(e)
    print("opening the directory with explorer...", end="\n\n")

    EXPLORER_PATH = "C:/Windows/explorer.exe"
    if path.exists(EXPLORER_PATH):
        # each directory must be separated with backslash
        # to open a specific folder with explorer.exe
        subprocess.run([EXPLORER_PATH, destDir.replace("/", "\\")])
    pass


def run_wrap() -> None:
    try:
        run()
    except KeyboardInterrupt as error:
        print(error)
        print("copy interrupted")


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter)

# registing sub-command itself
subparsers = parser.add_subparsers(
    metavar="command"
)

# registing sub-command 'run'
parser_run = subparsers.add_parser(
    'run',
    help=textwrap.dedent('''
    Copy images from a NeeView playlist 
    '''),
)
parser_run.set_defaults(func=run_wrap)
parser_run.add_argument(
    "tagname",
    metavar="TAG",
    type=str,
    help="""tag name (e.g. \"2girl\")""")

currentDir = getcwd()
parser_run.add_argument(
    "--parent",
    metavar="DEST",
    type=str,
    required=False,
    default=currentDir,
    help=textwrap.dedent("""\
    parent directory that contains copied file
    (e.g. \"C:\path\\to\Desktop\\tagger\")
    """))

# registing sub-command 'ls'
parser_ls = subparsers.add_parser(
    'ls',
    help='Lists up all the available playlists',
    add_help=False
)
parser_ls.set_defaults(func=ls)

args = parser.parse_args()
if hasattr(args, "func"):
    args.func()
else:
    parser.parse_args(['--help'])
