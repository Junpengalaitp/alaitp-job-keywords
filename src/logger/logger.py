from loguru import logger

log = logger
log.add(f"/logs/job-keyword/job-keyword.log", rotation="00:00")