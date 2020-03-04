import urequests
from config import CONFIG

INFLUXDB_OK = 204


class InfluxdbError(Exception):
    pass


def update_influxdb(tables, devices, datas):
    if not (len(tables) == len(devices) == len(datas)):
        raise InfluxdbError('update_influxdb() input len not match')

    # write multiple data in once, for better performance
    post_data = ''
    for t, dev, d in zip(tables, devices, datas):
        post_data += '{},device={} value={} \n'.format(t, dev, d)

    print('Post Data: {}'.format(post_data))
    db_url = str(CONFIG['DATABASE']['URL']).rstrip('/') + '/write?db=' + \
                 CONFIG['DATABASE']['DB'] + '&u=' + \
                 CONFIG['DATABASE']['USERNAME'] + '&p=' + \
                 CONFIG['DATABASE']['PASSWORD']

    resp = urequests.post(db_url, data=post_data)

    if resp.status_code != INFLUXDB_OK:
        raise InfluxdbError('Influxdb Post Failed: {}'.format(resp.status_code))

    return resp


def main():
    for d in range(3):
        for data in range(10):
            device = 'Dev' + str(d)
            update_influxdb(['test_table2'], [device], [data])


if __name__ == '__main__':
    main()
