import argparse
import query
import threading
import time

parser = argparse.ArgumentParser(add_help = True)
parser.add_argument("main_address", type = str, help = "address init")
args = parser.parse_args()


class log(threading.Thread):
	def __init__(self, text):
		super(log, self).__init__()
		self.text = text

	def run(self):
		file = open(f'port-{args.main_address}.txt', 'a')
		file.write(self.text)

# UTILS
def decode_int(string):
    result = 0
    for n, c in enumerate(string):
        if isinstance(c, str):
            c = ord(c)
        result |= c << (8 * n)
    return result


def decode_string(string, len_pos, len_bytes = 4):
    assert isinstance(len_pos, int)
    len_end = len_pos + len_bytes
    length = decode_int(string[len_pos:len_end])

    return string[len_end:len_end + length]


def get_info(address, port):
	req = query.SendQueryRequest(address, port, 'i')

	try:
		result = decode_string(req, 5, 4).decode('latin-1')

	except:
		result = decode_string(req, 5, 4)

	if len(result) < 1:
		return False

	return f'{result} | {decode_int(req[1:3])}/{decode_int(req[3:5])}'


class check(threading.Thread):
	def __init__(self, port):
		super(check, self).__init__()
		self.port = port

	def run(self):
		hostname = get_info(args.main_address, self.port)

		if not hostname == False:
			print(f'{args.main_address}:{self.port} > {hostname}')
			log(f'{args.main_address}:{self.port} > {hostname}\n').start()

# INIT
print(f'Checking {args.main_address}...')

for x in range(0, 9999):
	check(x).start()
