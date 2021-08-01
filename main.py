import datetime
from appstoreconnect import Api
from appstoreconnect.api import APIError

APIKEY_ID = ''
PATH_TO_APIKEY_FILE = ''
ISSUER_ID = ''

APPLE_ID = ''


def main():

    api = Api(APIKEY_ID, PATH_TO_APIKEY_FILE, ISSUER_ID)
    date = datetime.datetime(year=2020, month=11, day=1)
    delta_time = datetime.timedelta(days=32)

    total_units = 0
    for i in range(12):
        monthly_units = 0
        y = str(date.year)
        m = str(date.month)
        report_date = f'{y}-{str(m).zfill(2)}'
        save_file_path = f'reports/report_{report_date}.csv'
        try:
            api.download_sales_and_trends_reports(
                filters={'vendorNumber': '89927539', 'frequency': 'MONTHLY', 'reportDate': report_date},
                save_to=save_file_path
            )
        except APIError:
            break
        date += delta_time

        with open(save_file_path) as rep:
            lines = rep.read().splitlines()
            for line in lines:
                try:
                    units = int(line.split()[8])
                except ValueError:
                    continue
                monthly_units += units
        print(f'{report_date}\t{monthly_units}')
        total_units += monthly_units
    print(f'total\t{total_units}')


if __name__ == '__main__':
    main()
