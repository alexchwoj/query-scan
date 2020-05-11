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
		file = open(f'sec-{args.main_address}.txt', 'a')
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
    return string[len_end:len_end + length].decode('latin-1')


def get_info(address):
	req = query.SendQueryRequest(address, 7777, 'i')
	result = decode_string(req, 5, 4)
	
	if len(result) < 1:
		return False

	return f'{result} | {decode_int(req[1:3])}/{decode_int(req[3:5])}'


class check(threading.Thread):
	def __init__(self, address):
		super(check, self).__init__()
		self.address = address

	def run(self):
		hostname = get_info(self.address)

		if not hostname == False:
			print(f'{self.address}: {hostname}')
			log(f'{self.address}: {hostname}\n').start()

# INIT
print(f'Checking {args.main_address}...')

for x in range(0, 999):
	addr = f'{args.main_address}.{x}'
	check(addr).start()
