from flask import request, jsonify
from loguru import logger

from config.redis_config import redis_template
from controller import app
from service.cache_service import get_job_search_cache
from service.job_keyword_service import get_job_keyword_dict


@DeprecationWarning
@app.route('/keywords', methods=['POST'])
def post_job_keywords():
    job_description_data = request.json
    job_keyword_dict = get_job_keyword_dict(job_description_data)
    return jsonify(job_keyword_dict)


@app.route('/keywords/<string:job_search_id>', methods=['GET'])
def get_job_keywords(job_search_id: str):
    job_description_data = get_job_search_cache(job_search_id)

    if not job_description_data:
        logger.error(f"get job_search_id: {job_search_id} from cache failed")
        return jsonify({"error": True, "jobSearchId": job_search_id})

    logger.debug(
        f"get job_search_id: {job_search_id} job_description_data from cache, length: {len(job_description_data)}")
    job_keyword_dict = get_job_keyword_dict(job_description_data)
    redis_template.db(1).delete(job_search_id)
    logger.debug(f"deleted job_search_id: {job_search_id} from cache")

    return jsonify(job_keyword_dict)

