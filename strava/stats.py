if __name__ == '__main__':
    import argparse
    from strava import GearCheck, Stats

    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bikes', action='store_true')
    parser.add_argument('-r', '--run', action='store_true')
    parser.add_argument('-a', '--all', action='store_true')
    args = parser.parse_args()
    if args.all:
        args.bikes = args.run = True

    if args.run:
        t = Stats().ytd_totals()
        print(f'\nRun Stats')
        print(f'{"Run Avg.":<10}{t["avg_run"]:<25}')
        print(f'{"YTD Run":<10}{t["ytd_run"]:<25}')
    if args.bikes:
        s = GearCheck().list_gear()
        print(f'\n{"Name":<25}{"Distance (in miles)":<20}')
        for b in s['bikes']:
            n = b['name']
            distance = b['distance']
            # print('{k<2}'.format(bike['name']))
            print(f'{n:<25}{distance:<20}')
