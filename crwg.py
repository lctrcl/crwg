#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import time
import os
import sys
import re
import urllib.request, urllib.parse, urllib.error
import zipfile
import bz2
from tqdm import tqdm
import codecs

from transliterate.base import TranslitLanguagePack, registry
from transliterate import translit, get_available_language_codes
from transliterate.discover import autodiscover

from collections import Counter
# init
__author__ = "Igor Ivanov, @lctrcl"
__license__ = "GPL"
__version__ = "0.3"
__banner__ = """Custom Russian Wordlists Generator """ + \
    __version__ +  """         """

dictionary_urls = {'ruscorpora': 'https://ruscorpora.ru/new/ngrams/1grams-3.zip',
                   'opencorpora': 'http://opencorpora.org/files/export/ngrams/unigrams.cyr.lc.bz2'}


class MyParser(argparse.ArgumentParser):

    def error(self, message):
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)


autodiscover()


class ReverseInverseRussianLanguagePack(TranslitLanguagePack):
    language_code = "ru_inv_en"
    language_name = "ru_inv_en"
    mapping = (
        "йцукенгшщзхъфывапролджэёячсмитьбю",
        "qwertyuiop[]asdfghjkl;'\zxcvbnm,.",
    )

registry.register(ReverseInverseRussianLanguagePack)



def _reporthook(numblocks, blocksize, filesize, url=None):
    base = os.path.basename(url)
    try:
        percent = min((numblocks * blocksize * 100) / filesize, 100)
    except:
        percent = 100
    if numblocks != 0:
        sys.stdout.write("\b" * 70)
    sys.stdout.write("%-66s%3d%%" % (base, percent))


def downloaddictionaries(dictionary_strings):
    url = dictionary_urls[dictionary_strings]

    try:
        print(f'\n- [*] Downloading {dictionary_strings} dictionary\n')
        name, hdrs = urllib.request.urlretrieve(url, os.path.basename(
            url), lambda nb, bs, fs, url=url: _reporthook(nb, bs, fs, url))
    except IOError as e:
        print(f"Can't retrieve {url!r}: {e}")
    if dictionary_strings == 'ruscorpora':
        try:
            print(f'\n\n- [*] Extracting {dictionary_strings} dictionary\n')
            z = zipfile.ZipFile(os.path.basename(url))
        except zipfile.error as e:
            print(f"Bad zipfile (from {url!r}): {e}")
            return
        for n in z.namelist():
            print(n)
            dest = os.path.join('./', n)
            destdir = os.path.dirname(dest)
            if not os.path.isdir(destdir):
                os.makedirs(destdir)
            data = z.read(n)
            f = open(dest, 'w')
            f.write(data)
            f.close()
        z.close()
        os.unlink(name)
    if dictionary_strings == 'opencorpora':
        print(f'\n- [*] Extracting {dictionary_strings} dictionary\n')
        uncompresseddata = bz2.BZ2File(os.path.basename(url)).read()
        zname = os.path.splitext(os.path.basename(url))[0]
        f = open(zname, 'w')
        f.write(uncompresseddata)
        f.close()
    return


def autoclean(dictionary_strings):
    print(f'\n- [*] Autocleaning {dictionary_strings} dictionary')
    if dictionary_strings == 'opencorpora':
        name = os.path.splitext(
            os.path.basename(dictionary_urls[dictionary_strings]))[0]
    elif dictionary_strings == 'ruscorpora':
        name = os.path.splitext(
            os.path.basename(dictionary_urls[dictionary_strings]))[0] + '.txt'
    # stripping all digits and english characters
    regex = re.compile(r'[a-zA-Z0-9_]')
    with codecs.open(name, 'r', 'utf-8') as f1:
        lines = f1.read().splitlines()
    if dictionary_strings == 'opencorpora':
        lines = [x for x in lines if not regex.search(x.split()[0])]
        lines = [x for x in lines if len(x.split()[0]) > 3]
    elif dictionary_strings == 'ruscorpora':
        lines = [x for x in lines if not regex.search(x.split()[1])]
        lines = [x for x in lines if len(x.split()[1]) > 3]

    with codecs.open(dictionary_strings + 'dict_stripped', 'w', 'utf-8') as f2:
        if dictionary_strings == 'opencorpora':
            for line in lines:
                f2.write(f'{str(line).split()[0].lower()}\n')
        elif dictionary_strings == 'ruscorpora':
            for line in lines:
                f2.write(f'{str(line).split()[1].lower()}\n')

    f1.close()
    f2.close()
    return


def generatedictionary(source, destination,  gendic):
    with codecs.open(source, 'r', 'utf-8') as f:
        lines = f.read().splitlines()
    print(f'- [*] Making {gendic} dictionary: ')
    # TODO
    if gendic == 'tran5l1t':
        print("Not implemented yet")
        return
    if gendic == 'translit':
        with codecs.open(destination, 'a+', 'utf-8') as myfile:
            for line in tqdm(lines):
                myfile.write(
                    translit(str(line), 'ru', reversed=True) + '\n')

    if gendic == 'ru_inv_en':
        with codecs.open(destination, 'a+', 'utf-8') as myfile:
            for line in tqdm(lines):
                myfile.write(translit(str(line), gendic) + '\n')

    myfile.close()
    f.close()
    return


def compare_two_password_bases(source, destination, dictionary):
    leaked_passwords_name = source
    translit_dictionary_name = dictionary
    result_statistics_name = destination
    with codecs.open(leaked_passwords_name, 'r', 'utf-8') as f:
        leaked_passwords = f.read().splitlines()
    with codecs.open(translit_dictionary_name, 'r', 'utf-8') as content_file:
        translit_dictionary = content_file.read().splitlines()
    print("- [*] Generating statistics: ")
    s = set(translit_dictionary)
    b3 = [val for val in tqdm(leaked_passwords) if val in s]

    count = Counter(b3)

    print("- [*] Writing to file: ")
    with codecs.open(result_statistics_name, 'w+', 'utf-8') as myfile:
        for k, v in count.most_common():
            myfile.write(
                '%d ' % v + k + ' ' + translit(k, 'ru_inv_en', reversed=True) + '\n')
    myfile.close()
    print("Done")
    return


def main():

    parser = argparse.ArgumentParser(description=__banner__,
                                     epilog='Usage: ./python crwg.py -g ru_inv_en -s sourcedict -d destinationdict \n   /or/   python crwg.py --downloaddictionaries ruscorpora --autoclean \n   /or/   ')
    parser.add_argument(
        '--gendic', '-g', choices=['ru_inv_en', 'translit', 'tran5l1t'], help='Generate dictionary from file ')
    parser.add_argument('--downloaddictionaries', choices=[
                        'ruscorpora', 'opencorpora'], help='Download ruscorpora or opencorpora')
    parser.add_argument('--autoclean', action='store_true',
                        help='Autoclean downloaded dictionaries (english characters, numbers, etc)')
    parser.add_argument('--source', '-s', help="Source file")
    parser.add_argument('--destination', '-d', help='Destination file')
    parser.add_argument('--dictionary', help='Dictionary file')
    parser.add_argument('--compare_two_password_bases', '-c',
                        action='store_true', help='Compare two password files')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    print(__banner__)
    if args.downloaddictionaries:
        downloaddictionaries(args.downloaddictionaries)

    if args.autoclean:
        autoclean(args.downloaddictionaries)

    if args.gendic and not(args.source and args.destination):
        print("You must specify source and destination")
    elif args.gendic and args.source and args.destination:
        generatedictionary(args.source, args.destination, args.gendic)

    if args.compare_two_password_bases and not(args.source and args.destination and args.dictionary):
        print(
            "Usage: python crwg.py -c -s leaked_passwords -d statistics --dictionary ./opencorporadict_stripped_ru_inv_en")
    if args.compare_two_password_bases and args.source and args.destination and args.dictionary:
        compare_two_password_bases(
            args.source, args.destination, args.dictionary)


main()
