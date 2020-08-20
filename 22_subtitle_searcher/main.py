
from datetime import timedelta
from subtitle_filter import sub_filter
import sys
import srt

def duration(func):
	import time
	def test_execution(*args, **kwargs):
		test_start = time.time()
		func(*args, **kwargs)
		print("test duration is : ", time.time() - test_start)
	return test_execution

@duration
def main(args):
	with open(args[1], 'r') as file:
		subtitles = list(srt.parse(file))
	time_start = timedelta(0, 33, 843000)
	time_end = timedelta (0, 57, 554000)
	subtitles_target = sub_filter(subtitles, time_start, time_end)

if __name__ == "__main__":
	main(sys.argv)