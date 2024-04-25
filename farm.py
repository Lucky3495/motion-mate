from utils import EMGStreamer
import os
import time

def get_headers() -> str:
    _gyro_headers = [f"gyro-{i+1}" for i in range(6)]
    _emg_headers = [f"emg-{i+1}" for i in range(8)]
    headers = _gyro_headers + _emg_headers

    return ",".join(headers) + ",label,person"

def santize(data: list, args) -> str:
        record = [str(x) for x in data]
        record = ",".join(record) + f",{args.label},{args.person}"
        
        return record

def read_data(s: EMGStreamer, args) -> list[str]:
    start_time = time.time()

    chunk = []
    # keep reading for three seconds
    while (time.time() - start_time) < 3:
        data = s(log=False)
        record = santize(data, args)
        chunk.append(record)
        print(record)
    
    return chunk

# TODO: maybe use argparser later
def main():

    from argparse import ArgumentParser
    import argparse

    parser = ArgumentParser(description="I love my friend (wont tell you which one so you dont feel jealous if you are not him/her).")
    parser.add_argument("--label", type=str, help="Specify a label string.")
    parser.add_argument("--person", type=str, help="Specify a person string.")
    parser.add_argument('--ask', action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    
    s = EMGStreamer()
    s.open()
    file = open("data.csv", 'a')
    # add headers if file is empty
    if os.stat(file.name).st_size == 0:
        headers = get_headers()
        file.write(headers+"\n")

    n = 10
    input(f"ready? your label is {args.label} btw and you're {args.person} btw (y) ")
    for _ in range(n):
        chunk = read_data(s, args)

        if args.ask:
            answer = input("read again? (y/n/s) ")
            if answer.lower() == 'n':
                break
            elif answer.lower() == 's':
                continue

        file.write("\n".join(chunk)+"\n")
            

    file.close()
    s.close()

if __name__ == "__main__":
    main()

