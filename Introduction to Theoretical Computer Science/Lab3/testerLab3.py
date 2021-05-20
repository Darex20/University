import os
import subprocess as sub
import time

tests_dir = 'testsLab3'
prog = 'SimPa.py'

passed = 0
total_time = 0
dirs = os.listdir(tests_dir)

print(f'Starting tests... ({prog})')

for tst in dirs:

	with open(f'{tests_dir}/{tst}/primjer.in') as infile, open(f'{tests_dir}/{tst}/primjer.out') as outfile:

		progpipe = sub.Popen(f'py -3.9 {prog}', stdin=infile, stdout=sub.PIPE, universal_newlines=True)

		start_time = time.time()

		stroutput = progpipe.communicate()[0]
		progpipe.wait()

		elapsed = time.time() - start_time

		try:
			progpipe.kill()
		except OSError:
			pass

		expected = outfile.read()
		print(f'{tst} ... ', end='')

		if stroutput == expected:
			passed += 1
			print(' YES', end='')
		else:
			print(' NO ', end='')

		total_time += elapsed
		print(f'  ({elapsed:.4f}s)')


print(f'Passed: {passed}/{len(dirs)}')
print(f'Total time: {total_time:.4f}s')