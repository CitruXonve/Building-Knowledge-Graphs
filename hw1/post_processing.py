import logging
import sys, ujson

from pathlib import Path

def deserialize_jl(input_file):
    with open(input_file, "r") as f:
        return [ujson.loads(s) for s in f if s != "\n"]

def check_essential_information(cdr):
    for k in ["id", "url", "timestamp_crawl", "title", \
              "release_date", "budget", "gross_usa", "runtime"]:
        v = cdr[k]
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: missing path to jl file!")
        exit(1)

    jl_file = sys.argv[1]
    if not Path(jl_file).exists():
        print("Error: path of jl file does not exist!")
        exit(1)

    try:
        web_pages = deserialize_jl(jl_file)
    except Exception as e:
        print("Error: invalid jl file!")
        logging.exception(e)
        exit(1)

    for i, page in enumerate(web_pages):
        try:
            check_essential_information(page)
        except:
            print("Your web_page at index %d is invalid!" % (i))
            raise

        print("\rProcess: (%d/%d)..." % (i, len(web_pages)))

    print("\rFinished processing, looks good, found %d entries." % len(web_pages))