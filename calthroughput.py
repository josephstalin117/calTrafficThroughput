import csv
import os.path


def readfile(file_name):

    text_list=[]
    if (os.path.isfile(file_name)):
        with open(file_name) as f:
            text_list = f.readlines()
            text_list = [x.strip() for x in text_list]
            text_list = filter(lambda x: x[:5] == "nohup", text_list)
    else:
        print "not find output.txt!"
        exit()

    return text_list


def parser(text):
    list = text.split()

    times_per_s = 1000000 / int(list[list.index("-i") + 1][1:])
    throughput = int(list[list.index("-d") + 1])

    bps = times_per_s * throughput * 8

    if "-S" in list:
        if throughput > 1500:
            packets = 3
        else:
            packets = 2
    elif "-2" in list:
        if throughput > 1500:
            packets = 2
        else:
            packets = 1
    elif "-1" in list:
        if throughput > 1500:
            packets = 4
        else:
            packets = 2
    else:
        packets = 0

    pps = packets * times_per_s

    if "-k" in list or "-1" in list:
        fps = 1
    else:
        fps = times_per_s

    data = [text, bps, pps, fps]
    return data


def write_cvs(data, file_name):
    if (os.path.isfile(file_name)):
        with open(file_name, 'ab') as f:
            wr = csv.writer(f)
            wr.writerow(data)
    else:
        with open(file_name, 'wb') as f:
            wr = csv.writer(f, quoting=csv.QUOTE_ALL)
            wr.writerow(data)


def main():
    text_list = readfile("output.txt")
    for text in text_list:
        data = parser(text)
        write_cvs(data, 'output.csv')


if __name__ == '__main__':
    main()
