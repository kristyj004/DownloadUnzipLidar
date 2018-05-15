#-------------------------------------------------------------------------------
# Name:        DownloadUnzipLidar
# Purpose:     Downloads and then unzips data from the PSU ftp site
#
# Author:      Kristen Jordan Koenig
#
# Created:     May 14, 2018
# Copyright:   (c) Kristen 2018
#-------------------------------------------------------------------------------
import zipfile
from os import listdir, chdir, mkdir
from os.path import join, exists, basename, isdir
from ftplib import FTP

# ftp code from https://www.blog.pythonlibrary.org/2012/07/19/python-101-downloading-a-file-with-ftplib/ &
# https://stackoverflow.com/questions/5230966/python-ftp-download-all-files-in-directory

def unzip(zipFile, unzipLocation):
    zip_ref = zipfile.ZipFile(zipFile, 'r')
    zip_ref.extractall(unzipLocation)
    zip_ref.close()


def listfiles(folder):
    list = listdir(folder)
    return list


def handleDownload(block):
    file.write(block)
    print ".",


def main():

    # edit these variables to the paths you want to use your computer
    downloadFolder = r'C:\temp'
    unzippedLidarFolder = r'C:\temp\unzipped'

    # make sure the folders exist
    for f in [downloadFolder, unzippedLidarFolder]:
        if not exists(f):
            mkdir(f)

    # define ftp variables
    ftpUrl = "ftp.pasda.psu.edu"

    # make the ftp connection
    ftp = FTP(ftpUrl)
    ftp.login()

    # change directory in the ftp site
    ftp.cwd("pub/pasda/psu_opp/2017Orthophotos/LIDAR/DEM")

    filenames = ftp.nlst() # get filenames within the directory
    print filenames

    lidar_downloads = []

    # loop through the filenames
    for filename in filenames:
        if "228" in filename or "227" in filename: # this narrows down the files we're downloading, change if you want

            local_filename = join(downloadFolder, filename)

            if not exists(local_filename):
                file = open(local_filename, 'wb')
                ftp.retrbinary('RETR '+ filename, file.write)
                file.close()
                lidar_downloads.append(filename)

    ftp.quit()

    ##-----------unzip lidar files
    print("Unzipping files")
    for lf in lidar_downloads:
        full_zip_path = join(downloadFolder, lf)

        # test to see if the img file exists already
        img = join(unzippedLidarFolder, lf.replace(".zip", ".img"))
        if not exists(img):
            unzip(full_zip_path, unzippedLidarFolder)

    print("Files downloaded and unzipped to %s" % unzippedLidarFolder)

if __name__ == '__main__':
    main()

