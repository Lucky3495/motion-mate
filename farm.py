from utils import EMGStreamer
import os
import time

LABEL = "left"
PERSON = "saher"

def get_headers() -> str:
    _gyro_headers = [f"gyro-{i+1}" for i in range(6)]
    _emg_headers = [f"emg-{i+1}" for i in range(8)]
    headers = _gyro_headers + _emg_headers

    return " ,".join(headers) + ", label, person"

def santize(data: list) -> str:
        record = [str(x) for x in data]
        record = ", ".join(record) + f", {LABEL}, {PERSON}"
        
        return record

def read_data(s: EMGStreamer) -> list[str]:
    start_time = time.time()

    chunk = []
    # keep reading for three seconds
    while (time.time() - start_time) < 3:
        data = s(log=False)
        record = santize(data)
        chunk.append(record)
        print(record)
    
    return chunk

# TODO: maybe use argparser later
def main():
    
    s = EMGStreamer()
    file = open("data.csv", 'a')
    # add headers if file is empty
    if os.stat(file.name).st_size == 0:
        headers = get_headers()
        file.write(headers+"\n")

    n = 10
    input(f"ready? your label is {LABEL} btw and you're {PERSON} btw (y) ")
    for _ in range(n):
        chunk = read_data(s)

        answer = input("read again? (y/n/s) ")
        if answer.lower() == 'n':
            break
        elif answer.lower() == 's':
            continue

        file.write("\n".join(chunk))
            

    file.close()
    s.close()

if __name__ == "__main__":
    main()

