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


@router.get(
    "/verify/{certificate_id}"
)
def verify_certificate(
    certificate_id: str
):
    return (
        certificate_service
        .verify_certificate(
            certificate_id
        )
    )


@router.get(
    "/all"
)
def get_all_certificates():
    return (
        certificate_service
        .get_all_certificates()
    )