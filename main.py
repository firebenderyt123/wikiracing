import sys
import getopt
import asyncio

from wikiracing import WikiRacer


def form():
    start = input('Start: ')
    finish = input('Finish: ')
    return start, finish


async def main(argv):
    start = None
    finish = None
    opts, args = getopt.getopt(argv, "hs:f:", ["start=", "finish="])
    for opt, arg in opts:
        if opt == '-h':
            print('python3 main.py -s <start> -f <finish>')
            sys.exit()
        elif opt in ('-s', '--start'):
            start = arg
        elif opt in ('-f', '--finish'):
            finish = arg

    if not start or not finish:
        start, finish = form()

    wR = WikiRacer()

    while True:
        try:
            path = await wR.find_path(start, finish)
            break
        except Exception as e:
            print(e)
            start, finish = form()

    print(path)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main(sys.argv[1:]))
    loop.close()
