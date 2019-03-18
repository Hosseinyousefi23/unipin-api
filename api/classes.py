from django.http.response import JsonResponse


def create_json_response(status, details, status_code=None, res_errors=None, data=None, warnings_=None,
                         importer_id=None, auto_generation=None, error_type=None, missing_columns=None):
    info = {'status': status,
            'details': details}
    if res_errors:
        info['errors'] = res_errors
    if data:
        info['data'] = data
    if warnings_:
        info['warnings'] = warnings_
    if importer_id:
        info['importer_id'] = importer_id
    if auto_generation:
        info['auto_generation'] = auto_generation
    if error_type:
        info['error_type'] = error_type
    if missing_columns is not None:
        info['missing_columns'] = missing_columns
    response = JsonResponse(info)
    if status_code:
        response.status_code = status_code
    return response
