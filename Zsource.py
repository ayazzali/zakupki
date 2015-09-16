import re
from ftplib import FTP
from tempfile import TemporaryFile
from zipfile import ZipFile, ZipInfo

from time import sleep


class Zsource:

    ''' This class represents an interface to Zakupki's data source.

        Use to retrieve file lists and then raw XML files applying
        arbitrary filters.
    '''

    def __init__(self):
        ''' Initialize connection to Zakupki FTP.
        '''
        self.connection = FTP('ftp.zakupki.gov.ru', user='free', passwd='free')
        self.connection.cwd('fcs_regions')

    def refresh_list(self, regions=[]):
        ''' Refresh list of files for a given list of regions.
        '''
        self.files = []
        file_re = re.compile(r'^.*\.\w{,3}$')
        folders = []
        all_regions = self.list_regions()
        for current_folder in regions:
            while True:
                print(' ' * 100, end='\r')
                print(current_folder, len(self.files), sep='\t')
                nlst = self.connection.nlst(current_folder)
                folders.extend([x for x in nlst if not file_re.match(x) and x != current_folder])
                if len(folders) == 0:
                    break
                current_folder = folders.pop(0)
                self.files.extend([x for x in nlst if file_re.match(x)])

    def list_regions(self):
        ''' Return a list of available region directories.
        '''
        return [x for x in self.connection.nlst() if not x.startswith('_')]

    def list_document_types(self):
        ''' Return a list of document types in the current self.files list.
        '''
        result = set()
        type_re = re.compile(r'.*/(\w+?)_[^/]+$')
        return set(type_re.match(f).group(1) for f in self.files)

    def get_files(self, region=None, document_type=None):
        ''' Generator that returns file handles for raw XML (unzipped) files
            from self.files list. Additionally can be filtered by document_type
            and region.
        '''
        # TO-DO: Add date filter
        files = self.files
        if region and region in self.list_regions():
            files = [f for f in files if f.startswith(region)]
        if document_type and document_type in self.list_document_types():
            files = [f for f in files if document_type in f]
        l = len(files)
        c = 1
        for path in files:
            print('{}/{}'.format(c, l))
            sleep(1)
            for f in self.retr_file(path):
                yield f
            c += 1

    def retr_file(self, path, retry=3):
        ''' Gererator that returns file handles for raw XML (unzipped) files
            inside a ZIP file at a given FTP path.
        '''
        ftp_size = self.connection.size(path)
        while retry > 0:
            tmp = TemporaryFile()
            self.connection.retrbinary('RETR {}'.format(path), tmp.write)
            down_size = tmp.tell()
            if down_size == ftp_size:
                break
            retry -= 1
        with ZipFile(tmp) as zf:
            for i in zf.infolist():
                yield zf.open(i)
        tmp.close()

    def download_files(self, dir='.', unzip=True):
        ''' download_files
            TO-DO: Save raw XML (or ZIP) files into a directory.
        '''
