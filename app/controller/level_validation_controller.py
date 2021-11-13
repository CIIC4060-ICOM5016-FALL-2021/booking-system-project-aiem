from flask import jsonify

from app.model.level_validation import UserLevelValidationDAO


class UserLevelValidation:

    def validate_permission(self, us_id, ro_id):
        ulv_dao = UserLevelValidationDAO()

        if ulv_dao.get_user_level(us_id) >= ulv_dao.get_room_level(ro_id):
            return jsonify("User has permission"), 200
        else:
            return jsonify("User does not have permission"), 403

