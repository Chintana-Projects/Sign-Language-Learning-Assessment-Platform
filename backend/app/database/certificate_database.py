import json
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

CERTIFICATE_FILE = os.path.join(
    BASE_DIR,
    "certificates.json"
)


class CertificateDatabase:

    def __init__(self):

        if not os.path.exists(
            CERTIFICATE_FILE
        ):

            with open(
                CERTIFICATE_FILE,
                "w"
            ) as f:

                json.dump(
                    {},
                    f,
                    indent=4
                )

    def load(self):

        with open(
            CERTIFICATE_FILE,
            "r"
        ) as f:

            return json.load(f)

    def save(self, data):
        print(
        "SAVING CERTIFICATES TO:",
        os.path.abspath(CERTIFICATE_FILE)
    )
        with open(
        CERTIFICATE_FILE,
        "w"
    ) as f:
            json.dump(
            data,
            f,
            indent=4
        )

    def add_certificate(
    self,
    certificate
):
        print(
        "ADDING CERTIFICATE:",
        certificate["certificate_id"]
    )
        data = self.load()
        data[
        certificate["certificate_id"]
    ] = certificate
        self.save(data)

    def get_certificate(
        self,
        certificate_id
    ):

        data = self.load()

        return data.get(
            certificate_id
        )

    def get_all_certificates(
        self
    ):

        return self.load()