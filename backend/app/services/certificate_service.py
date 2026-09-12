from app.database.certificate_database import (
    CertificateDatabase
)


class CertificateService:

    def __init__(self):
        self.db = CertificateDatabase()

    def verify_certificate(
        self,
        certificate_id
    ):
        certificate = (
            self.db.get_certificate(
                certificate_id
            )
        )

        if not certificate:
            return {
                "valid": False,
                "message":
                    "Certificate not found"
            }

        return {
            "valid": True,
            "certificate": certificate
        }

    def get_all_certificates(self):
        return (
            self.db.get_all_certificates()
        )