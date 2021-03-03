from indeed import get_jobs as get_indeed_jobs
from stack import get_jobs as get_stack_jobs
from save import save_to_file

indeed_jobs = get_indeed_jobs()
stack_jobs = get_stack_jobs()
jobs = indeed_jobs +stack_jobs
save_to_file(jobs)


