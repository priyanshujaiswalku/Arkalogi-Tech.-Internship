"""
Task 09: Validation Middleware & Helper Utilities
Arkalogi Internship - Priyanshu Kumar

Provides reusable validation decorators for Flask endpoints.
"""

from functools import wraps
from flask import request, jsonify
from pydantic import ValidationError


def validate_schema(schema_class):
    """
    Decorator for Flask routes to validate incoming JSON/Form request payload with Pydantic.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            raw_data = request.get_json(silent=True) or request.form.to_dict()
            try:
                validated_data = schema_class(**raw_data)
                # Pass validated instance into kwargs
                kwargs['validated_data'] = validated_data
            except ValidationError as e:
                errors = []
                for err in e.errors():
                    loc = " -> ".join(str(l) for l in err['loc'])
                    errors.append({
                        'field': loc,
                        'message': err['msg'],
                        'type': err['type']
                    })
                return jsonify({
                    'status': 'error',
                    'message': 'Request validation failed.',
                    'errors': errors
                }), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator
