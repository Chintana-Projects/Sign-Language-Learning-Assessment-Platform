import { useState } from "react";
import "../styles/certificateVerification.css";
export default function CertificateVerification() {
    const [certificateId, setCertificateId] =
        useState("");

    const [result, setResult] =
        useState(null);

    async function verifyCertificate() {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/certificate/verify/${certificateId}`
            );

            const data =
                await response.json();

            setResult(data);
        } catch (err) {
            console.error(err);
        }
    }

    return (

<div className="verification-page">

    <div className="verification-card">

        <h1 className="verification-title">
            🛡 Certificate Verification
        </h1>

        <p className="verification-subtitle">
            Verify the authenticity of a SignSync certificate
        </p>

        <input
            className="verification-input"
            type="text"
            value={certificateId}
            onChange={(e) =>
                setCertificateId(
                    e.target.value
                )
            }
            placeholder="Enter Certificate ID"
        />

        <button
            className="verify-btn"
            onClick={verifyCertificate}
        >
            Verify Certificate
        </button>

        {result && result.valid && (

            <div className="valid-card">

                <h2>
                    ✅ Certificate Verified
                </h2>

                <div className="cert-info">

                    <p>
                        <strong>Name:</strong>{" "}
                        {result.certificate.student_name}
                    </p>

                   

                    

                    

                    <p>
                        <strong>Issued:</strong>{" "}
                        {new Date(
                            result.certificate.issued_at
                        ).toLocaleDateString()}
                    </p>

                </div>

            </div>

        )}

        {result && !result.valid && (

            <div className="invalid-card">

                <h2>
                    ❌ Invalid Certificate
                </h2>

                <p>
                    No certificate found with this ID.
                </p>

            </div>

        )}

    </div>

</div>

);
}