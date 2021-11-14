from flask import jsonify

from app.model.level_validation import UserLevelValidationDAO

#The idea for Requirement #7 is to:
#First scratch off the base condition by limiting the CREATION of a Meeting
#to only a user that meets the UserLevel for the RoomLevel that they wish
#to reserve.

#Once that is done, all Meeting operations that may modify/delete the meeting
#will be limited to ONLY the meeting owner
#Access operations should be open to people who are attending said meeting

#SESSION_ID == the current person browsing, in theory
#Once a login function is created, the SESSION_ID will be the USER_ID for the
#current user in session

class UserLevelValidationController:

    def validate_permission_to_create(self, us_id, ro_id):
        rl_dao = UserLevelValidationDAO()
        room_level = rl_dao.get_room_level_from_ro_id(ro_id)
        ul_dao = UserLevelValidationDAO()
        user_level = ul_dao.get_user_level_from_us_id(us_id)

        if user_level >= room_level:
            return True
        else:
            return False

    def validate_owner_through_mt_id(self, session_id, mt_id):
        mt_dao = UserLevelValidationDAO()
        owner_id = mt_dao.get_owner_id_from_mt_id(mt_id)

        if session_id == owner_id:
            return True
        else:
            return False

    def validate_owner_through_re_id(self, session_id, re_id):
        re_dao = UserLevelValidationDAO()
        owner_id = re_dao.get_owner_id_from_re_id(re_id)

        if session_id == owner_id:
            return True
        else:
            return False


    def validate_attendee(self, session_id, mt_id):
        att_dao = UserLevelValidationDAO()
        is_attending = att_dao.confirm_attending(mt_id, session_id)

        if is_attending is not None:
            return True
        else:
            return False





