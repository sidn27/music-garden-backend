from flask.json import jsonify

from app.settings import page_size

def paginatedQuery(model, page_number, filters=None, order=None):

    if filters is not None:
        return model.query.filter(filters).order_by(order).slice(page_number * page_size, (page_number * page_size) + page_size)

    else:
        return model.query.order_by(order).slice(page_number * page_size, (page_number * page_size) + page_size).all()


def getPageCount(model, filters=None):

    if filters is not None:

        total_count = model.query.filter(filters).count()

        if total_count % page_size == 0:
            page_count = total_count / page_size

        else:
            page_count = 1 + total_count / page_size

    else:

        total_count = model.query.count()

        if total_count % page_size == 0:
            page_count = total_count / page_size

        else:
            page_count = 1 + (total_count / page_size)

    return page_count

def create_success_response(data=None):
    dict = {"response": "success"}
    if data is not None:
        for key in data.keys():
            dict[key] = data[key]
    return jsonify(dict)

def create_error_response(error):
    return jsonify({
        "response": "failure",
        "error": error
    })

def create_success_list_response(list, page_count):
    return jsonify({
        "response": "success",
        "list": list,
        "page_count": page_count
    })


