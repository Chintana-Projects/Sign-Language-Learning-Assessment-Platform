from fastapi import APIRouter
from app.services.certificate_service import (
    CertificateService
)

router = APIRouter(
    prefix="/certificate",
    tags=["Certificate"]
)

certificate_service = (
    CertificateService()
)

@router.get("/all")
def get_all_certificates():

    return {
        "success": True,
        "certificates":
            certificate_service
            .get_all_certificates()
    }

@router.get("/{certificate_id}")
def verify_certificate(
    certificate_id: str
):

    return (
        certificate_service
        .verify_certificate(
            certificate_id
        )
    )