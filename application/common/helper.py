import math

from application.common.sqlalchemy_helper import to_dict


def pagination(data, query):
    if data.get("page", None) is None:
        data['page'] = 1
    if data.get("results_per_page", None) is None:
        data['results_per_page'] = 20
    page = int(data['page'])
    results_per_page = int(data['results_per_page'])
    start = (page - 1) * results_per_page
    results = query.limit(results_per_page).offset(start).all()
    count = query.count()
    total_pages = int(math.ceil(count / results_per_page))
    return {
        "page": page,
        "results_per_page": results_per_page,
        "total_pages": total_pages,
        "num_results": len(results),
        "objects": [to_dict(result) for result in results]
    }
