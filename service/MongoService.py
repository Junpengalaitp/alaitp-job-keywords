from database.MongodbManager import MongoManager


def get_all_jobs(source: str = 'all') -> list:
    if source == 'all':
        jobs_list = MongoManager().find_all()
    else:
        jobs_list = MongoManager().find_by_source(source)

    return [job['job_desc'] for job in jobs_list]