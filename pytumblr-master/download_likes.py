__author__ = 'bor1ng'

import pytumblr
import requests
import ConfigParser
import datetime
import os.path
from sys import stdout


def main():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    keys = config.options('Client')
    client = pytumblr.TumblrRestClient(
        config.get('Client', keys[0]),
        config.get('Client', keys[1]),
        config.get('Client', keys[2]),
        config.get('Client', keys[3])
    )

    liked_count = client.info()['user']['likes']
    saved = int(config.get('Saved', 'count'))
    new = liked_count - saved
    i = 0

    output = 'liked2'
    if not os.path.exists(output):
        os.makedirs(output)

    for offset in xrange(0, new, 20):
        limit = 20 if new - offset > 20 else new - offset
        liked_posts = client.likes(offset=offset, limit=limit)['liked_posts']
        for post in liked_posts:
            photos = post.get('photos')
            if not photos:
                continue
            for photo in photos:
                url = photo['original_size']['url']
                r = requests.get(url)
                title = url.split('/')[-1]
                with open(os.path.join(output, title), 'wb') as f:
                    for buf in r.iter_content(1024):
                        if buf:
                            f.write(buf)
            i += 1

            stdout.write("\r%2d%%" % round(float(i) / float(new) * 100, 2))
            stdout.flush()

    config.set('Saved', 'count', liked_count)
    with open('config.ini', 'w') as config_file:
        config.write(config_file)

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    main()
    print("\nDone in %s" % (datetime.datetime.now() - start_time))
