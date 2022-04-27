try:
    import pyscca
    from argparse import ArgumentParser
    import pandas as pd
    from colorama import init, Fore, Back, Style
except ImportError:
    print("\nImport Error Triggered, check dependencies, install from requirements.txt. Exiting")
    exit()
import pyfiglet
import ntpath
import os
from pathlib import Path

# libscca-python
listofpf=[]
#outputfilepath
outputpath=""
#outputfileformat
outputfileformat=""
skipped=0

def compulsary_ascii():
    ascii_banner = pyfiglet.figlet_format("PreDfetch")
    print(ascii_banner)

def getdirlist(inputdir):
    pathlist=[]
    for path in Path(inputdir).rglob('*.pf'):
        pathlist.append(str(inputdir/path))
    return pathlist

def generateoutput():
    df = pd.DataFrame()
    for x in range(len(listofpf)):
        df = df.append(listofpf[x], ignore_index=True)
    if outputfileformat=="SCREEN":
        print(df)
    if outputfileformat=="CSV":
        df.to_csv(outputpath, index=False)
    if outputfileformat=="JSON":
        df.to_json(outputpath)
    message = "[+] " + str(len(listofpf)) + " Files Created, " + str(skipped) + " files skipped"
    print(Style.BRIGHT + Fore.GREEN + message)


def pfparser(pffilepath):
   try:

        pfdata = pyscca.open(pffilepath)
        last_runs = []
        for x in range(8):
            if pfdata.get_last_run_time_as_integer(x) > 0:
                last_runs.append(pfdata.get_last_run_time(x).strftime("%Y-%m-%d %H:%M:%S"))
            else:
                last_runs.append("")

        last_run_1, last_run_2, last_run_3, last_run_4, last_run_5, last_run_6, last_run_7, last_run_8 = last_runs
        vol_truncated = "no"
        volumes = []
        for i in range(pfdata.number_of_volumes):
            if i < 2:
                volume = [str(pfdata.get_volume_information(i).device_path),
                      pfdata.get_volume_information(i).creation_time.strftime("%Y-%m-%d %H:%M:%S"),
                      format(pfdata.get_volume_information(i).serial_number, 'x').upper()]
                volumes.append(volume)
            else:
                vol_truncated = "yes"

        if len(volumes) == 1:
            volumes.append("")
        if len(volumes) == 2:
            volumes.append("")

        volume1, volume2, volume3 = volumes

        filesloaded= []
        for filename in iter(pfdata.filenames):
            filesloaded.append(filename)

        pfdatadict = {
            "file":str(ntpath.basename(pffilepath)), "exe_name":str(pfdata.executable_filename),"run_count":str(pfdata.run_count),"prefetch_hash":format(pfdata.prefetch_hash, 'x').upper(),"last_run_1": str(last_run_1), "last_run_2": str(last_run_2), "last_run_3": str(last_run_3),
            "last_run_4": str(last_run_4),
            "last_run_5": str(last_run_5), "last_run_5": str(last_run_5), "last_run_7": str(last_run_7),
            "last_run_8": str(last_run_8), "no_of_volumes" : str(pfdata.number_of_volumes), "vol_truncated" : vol_truncated, "volume1" : volume1, "volume2" : volume2, "volume3" : volume3, "files_loaded":str(filesloaded)

        }
        listofpf.append(pfdatadict)
        print(Style.BRIGHT + Fore.GREEN + "[+] " + pffilepath + " File was processed")
   except:
       print(Style.BRIGHT + Fore.RED + "[!] " + pffilepath + " File was skipped! Likely Corrupt")
       global skipped
       skipped += 1



if __name__ == '__main__':
    compulsary_ascii()
    parser = ArgumentParser()
    parser.add_argument("-c", help="Output to CSV", action="store_true")
    parser.add_argument("-j", help="Output to JSON", action="store_true")
    parser.add_argument("-n", help="Print to Screen - not pretty", action="store_true")
    parser.add_argument('-i', dest="input", help="Path to Prefetch File(s)")
    parser.add_argument('-o', dest="output_file", help="Output File Path")
    args = parser.parse_args()

    if args.c:
        outputfileformat="CSV"
        if args.j:
            print(Style.BRIGHT + Fore.RED + "[!] Only 1 output format at a time supported")
            exit()
        if not args.output_file:
            print(Style.BRIGHT + Fore.RED + "[!] no output path specified")
        else:
            outputpath = args.output_file

    if args.j:
        outputfileformat="JSON"
        if args.c:
            print(Style.BRIGHT + Fore.RED + "[!] Only 1 output format at a time supported")
            exit()
        if not args.output_file:
            print("no output path specified")
        else:
            outputpath = args.output_file

    if args.n:
        outputfileformat="SCREEN"


    if args.input:

        if outputfileformat=="":
            print(Style.BRIGHT + Fore.RED + "need to specify format -j for json, -c for csv, or -n for some reason")
            exit()
        else:
            if os.path.isfile(args.input):
                pfparser(args.input)
            else:
                dirlist = getdirlist(args.input)
                print(Style.BRIGHT + Fore.GREEN + "[+] Prefetch Files Found:" + str(len(dirlist)))
                for i in range(len(dirlist)):
                    pfparser(dirlist[i])
            generateoutput()





