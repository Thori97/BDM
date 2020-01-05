import pyaudio

p = pyaudio.PyAudio()

apiCnt = p.get_host_api_count()
print("Host API Count: %d"%apiCnt)
for cnt in range(apiCnt):
	print(p.get_host_api_info_by_index(cnt))