from pydantic import BaseModel


class StudentProofPayload(BaseModel):
    fileName: str
    mimeType: str
    base64: str


class GrantSubmissionFormData(BaseModel):
    email: str
    first_name: str
    last_name: str
    whatsapp: str
    location: str
    country: str
    is_student: bool
    gender: str
    python_journey: str
    need_ticket: bool
    need_transport: bool
    need_accommodation: bool
    support_details: str
    grant_consent: bool
    student_proof:  StudentProofPayload | None = None


class AccessGrantSubmissionPayload(BaseModel):
    agreed_to_code_of_conduct: bool
    agreed_to_privacy_policy: bool
    form_data: GrantSubmissionFormData
