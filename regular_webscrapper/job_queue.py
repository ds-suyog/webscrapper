""" 
this Jobqueue module provides job-queue functionality
"""

class Job_Queue(object):

	def __init__(self, max_running):
		print("initializing.............")
		self._queued = []
		self._running = []
		self._max = max_running
		self._completed = []
		self._num_of_jobs = 0
		self._finished = False
		self._closed = False
		self._debug = False

	def _all_alive(self):
		"""
		Simply states if all procs are alive or not. Needed to determine when
		to stop looping, and pop dead processs off and add live ones.
		"""
		if self._running:
			return all([x.is_alive() for x in self._running])
		else:
			return False

	def __len__(selfs):
		"""
		Just going to use number of jobs as the Job_Queue length.
		"""
		return self._num_of_jobs

	def close(self):
		"""
		A sanity check, so that the need to care about new jobs being added in
		the last throws of the job_queue's run are negated.
		"""
		if self._debug:
			print("job queue closed.")
		self._closed = True

	def append(self, process):
		"""
		add process to queue for queue monitoring and job tracking purpose
		"""
		if not self._closed:
			self._queued.append(process)
			self._num_of_jobs += 1
			if self._debug:
				print("job queue appended %s." % process.name)

	def _advance_the_queue(self):
		"""
		helper function to pop job off queue, start it, then add it to the 
		running queue. condition to check queue depletion: self._queued
		"""

		self._queued.reverse() # before it was LIFO (pop() picks last in), reversing it makes it FIFO
		while (len(self._running) < self._max) and (self._queued):
			job = self._queued.pop()
			job.start()
			self._running.append(job)

	def start(self):
		"""
        This is the workhorse. It will take the intial jobs from the _queue,
        start them, add them to _running, and then go into the main running
        loop.
        This loop will check for done procs, if found, move them out of
        _running into _completed. It also checks for a _running queue with open
        spots, which it will then fill as discovered.
        To end the loop, there have to be no running procs, and no more procs
        to be run in the queue.
        When all if finished, it will exit the loop, and disconnect_all()
        """

		if not self._closed:
			raise Exception("Need to close() before starting.")

		if self._debug:
			print("Job queue starting.")
			print("Job queue initial running queue fill.")

		self._advance_the_queue()

		while not self._finished:

			if self._debug:
				print("Job queue running queue filling.")

			self._advance_the_queue()

			if not self._all_alive():
				for id, job in enumerate(self._running):
					if not job.is_alive():
						if self._debug:
							print("Job queue found finished proc: %s." % job.name)

						done = self._running.pop(id)
						self._completed.append(done)

					if self._debug:
						print("Job queue has %d running." % len(self._running))

			if not (self._queued or self._running):
				if self._debug:
					print("Job queue finished.")

				for job in self._completed:
					job.join()

				self._finished = True

def try_using(parallel_type):
	def print_number(num):
		"""
		worker function:
		a simple task to execute
		"""
		print("starting worker..")
		print("num = {}".format(num))

	worker = {'type': ''}
	if parallel_type == "multiprocessing":
		from multiprocessing import Process as Bucket
		worker['type'] = "process"

	elif parallel_type == "threading":
		from threading import Thread as Bucket
		worker['type'] = "thread"

	jobs = Job_Queue(2)
	jobs._debug = False

	for x in range(1,21):
		jobs.append(Bucket(
			target = print_number,
    		args = [x],
    		kwargs = {},)
    		)

	jobs.close()
	jobs.start()


if __name__ == '__main__':
	#try_using("multiprocessing")
	try_using("threading")