import sys
import argparse
import urllib.request
import gzip
import multiprocessing as mp
import itertools
from collections import Counter

def count_package(work, counter):
    while True:
        item = work.get()
        _, line = item
        print(line)
        columns = line.split(",")

        if line == None:
            return

        if len(columns) == 2:
            packages = columns[1].split(",")
            for package in packages:
                counter[package] += 1

counter = Counter()

def count_lines(line):
    global counter
    counter.update(line.split()[1].split(","))


def main():
    global counter
    parser = argparse.ArgumentParser(description="Content indices parser for Debian mirror")
    parser.add_argument("arch", type=str, 
                        help="specifies the architecture")
    parser.add_argument("--udeb", action="store_true",
                        help="Download and parse udebs content indices")
    args = parser.parse_args()

    debian_mirror = "http://ftp.uk.debian.org/debian/dists/stable/main/"

    file_name = "Contents-"
    if args.udeb:
      file_name += "udeb-"
    file_name += args.arch + ".gz"

    print("file_name = " + file_name)

    file_url = debian_mirror + file_name

    # try block
    urllib.request.urlretrieve(file_url, file_name)

    # serial version
    counter = Counter()

    with gzip.open(file_name,"rt") as content_index:
        for line in content_index:
            counter.update(line.split()[1].split(","))

    print([package[0] for package in counter.most_common(10)])

    # parallel version
    # num_worker = mp.cpu_count()
    # manager = mp.Manager()
    # work = manager.Queue(num_worker)
    # counter = manager.dict()
    
    # pool = []
    # for _ in range(num_worker):
    #     p = mp.Process(target=count_package, args=(work, counter))
    #     p.start()
    #     pool.append(p)


    # with open(file_name,"r") as content_index:
    #     iters = itertools.chain(content_index, (None,)*num_worker)
    #     for line in enumerate(iters):
    #         work.put(line)

    # for p in pool:
    #     p.join()
    
    # print(len(counter))

    # pool = mp.Pool(mp.cpu_count())
    # with open(file_name,"r") as content_index:
    #     for chunk in grouper(1000, content_index):
    #         results = pool.map(process_chunk, chunk)

    # print(counter)


if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print('Must use Python 3 to run Penny')
        sys.exit(1)
    sys.exit(main())