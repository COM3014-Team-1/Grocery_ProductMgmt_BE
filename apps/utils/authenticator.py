from flask import jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from functools import wraps

def roles_allowed(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_roles = claims.get("roles",[])
            current_app.logger.info("User Roles:"+ str(user_roles))
            if not any(role in roles for role in user_roles):
                return jsonify({"msg": "Unauthorized - role not allowed"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator