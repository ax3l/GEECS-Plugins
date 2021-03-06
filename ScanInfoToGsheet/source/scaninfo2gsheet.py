import time
from getscaninfo import df_scaninfo, get_last_scannumber, get_scaninfo_row
from df2gsheet import df2gsheet


class scaninfo2gsheet:
    def __init__(self, dir_date, para_txt):
        self.dir_date = dir_date
        self.para_txt = para_txt
        self.sheet = None
        self.n_columns = None
        self.n_scans = None

    def write(self, gdr_dir, sheet_title):
        '''
        Open (Create if not exist) a google sheet in the google drive, then write down the all scans' infomation
        '''
        # get a dataframe to write
        df = df_scaninfo(self.dir_date, self.para_txt)
        # write the dataframe into a google sheet
        self.sheet = df2gsheet(sheet_title, df, gdr_dir)
        self.n_scans = df.index[-1] + 1
        self.n_columns = len(df.keys())
        return self.sheet

    def update(self):
        '''If there are new scans, these infomation will be added in the google sheet
        return: latest scan number
        '''
        scan_new = get_last_scannumber(self.dir_date)
        scaninfo_new = get_scaninfo_row(self.dir_date, self.para_txt, scan_new, self.n_columns)
        self.sheet[0].append_table(scaninfo_new)
        self.n_scans = scan_new
        return self.n_scans


def main():
    dir_date = 'Z:\\data\\Undulator\\Y2020\\01-Jan\\20_0122'
    sheet_title = 'HTU test2'
    para_txt = 'Jet_X,Jet_Y,Jet_Z,Pressure,separation'
    gdrive_dir = '0B6BJlLNDz1MabGZSMUVWOHVqbE0'
    isAutoUpdate = False

    scaninfo = scaninfo2gsheet(dir_date, para_txt)
    sheet = scaninfo.write(gdrive_dir, sheet_title)
    if isAutoUpdate:
        for i in range(60 * 10):  # run for 10 hour
            time.sleep(60)  # wait for 1 min
            nscan_new = scaninfo.update()


if __name__ == '__main__':
    main()
