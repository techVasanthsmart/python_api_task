from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentSubmitSchema, AssignGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    """Returns list of assignments using teacher id"""
    teacher_assignments      = Assignment.get_assignments_by_teacher(p.teacher_id)
    teacher_assignments_dump = AssignmentSchema().dump(teacher_assignments, many=True)
    return APIResponse.respond(data=teacher_assignments_dump)

@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def assign_grade_to_student(p, incoming_payload):
    
    """Assign Grade to assignment for student"""
    assignment_payload = AssignGradeSchema().load(incoming_payload)
    assign_grade = Assignment.assign_grade_to_student(
        _id=assignment_payload.id,
        grade=assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    assign_grade_dump = AssignmentSchema().dump(assign_grade)
    return APIResponse.respond(data=assign_grade_dump)

