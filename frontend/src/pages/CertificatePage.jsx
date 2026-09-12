import { useLocation, useNavigate } from "react-router-dom";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import "../styles/certificate.css";

export default function CertificatePage() {
    const location = useLocation();
    const navigate = useNavigate();

    const certificate = location.state?.certificate;

    const levelClass =
    certificate?.level === "Professional"
        ? "professional"
        : certificate?.level === "Intermediate"
        ? "intermediate"
        : "beginner";

    if (!certificate) {
        return (
            <div style={{ padding: "40px", textAlign: "center" }}>
                Certificate not found.
            </div>
        );
    }

    async function downloadCertificate() {
        const element = document.getElementById("certificate");
        if (!element) return;

        const canvas = await html2canvas(element, {
            scale: 2,
            useCORS: true,
            logging: false,
        });

        const imgData = canvas.toDataURL("image/png");

        const pdf = new jsPDF(
            "landscape",
            "mm",
            "a4"
        );

        const pdfWidth =
            pdf.internal.pageSize.getWidth();

        const pdfHeight =
            pdf.internal.pageSize.getHeight();

        pdf.addImage(
            imgData,
            "PNG",
            0,
            0,
            pdfWidth,
            pdfHeight
        );

        pdf.save(
            `${certificate.certificate_id}.pdf`
        );
    }

    return (
        <div className="certificate-container">

            <button
                onClick={() => navigate(-1)}
                className="back-btn"
            >
                ← Back
            </button>

            <div className="certificate-wrapper">

                <div
                    id="certificate"
                    className={`certificate ${levelClass}`}
                >
                    {/* Corner Accents */}
                    <div className="corner-accent top-left"></div>
                    <div className="corner-accent top-right"></div>
                    <div className="corner-accent bottom-left"></div>
                    <div className="corner-accent bottom-right"></div>

                    {/* Watermark */}
                    <div className="watermark-shield"></div>

                    <div className="certificate-content">

                        {/* Header */}
                        <div className="brand-header">
                            <svg
                                width="36"
                                height="36"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="#1e3a8a"
                                strokeWidth="2.2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <path d="M18 11V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v0"></path>
                                <path d="M14 10V4a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"></path>
                                <path d="M10 10.5V6a2 2 0 0 0-2-2v0a2 2 0 0 0-2 2v8"></path>
                                <path d="M18 8a2 2 0 0 1 2 2v4a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"></path>
                            </svg>

                            <span className="certificate-logo">
                                SignSync
                            </span>
                        </div>

                        <h2 className="certificate-title">
                            CERTIFICATE OF ACHIEVEMENT
                        </h2>

                        <p className="cert-subtitle">
                            This certifies that
                        </p>

                        <div className="student-name">
                            {certificate.student_name}
                        </div>

                        <p className="cert-body">
                            has successfully completed the SignSync Certification
                        </p>

                        <div
                            className="level"
                            style={{
                                color:
    certificate.level === "Professional"
        ? "#6d28d9"
        : certificate.level === "Intermediate"
        ? "#2563eb"
        : "#16a34a"
                            }}
                        >
                            {certificate.level === "Professional" && "👑 "}
{certificate.level === "Intermediate" && "🥈 "}
{certificate.level === "Beginner" && "📘 "}
                            {certificate.level}
                        </div>

                        <div className="certificate-badge">
                            #{certificate.certificate_id.slice(-6)}
                        </div>

                        <p
                            style={{
                                fontSize: "18px",
                                fontWeight: "600",
                                marginTop: "10px"
                            }}
                        >
                           {certificate.level === "Professional" &&
    "Highest Certification Distinction"}

{certificate.level === "Intermediate" &&
    "Intermediate Competency Achievement"}

{certificate.level === "Beginner" &&
    "Successfully Certified"}
                        </p>

                        <div className="cert-meta">
                            <p className="score">
                                Score: {certificate.score}%
                            </p>

                            <p className="cert-id">
                                Certificate ID: {certificate.certificate_id}
                            </p>

                            <p className="issued-date">
                                Issued:{" "}
                                {new Date(
                                    certificate.issued_at
                                ).toLocaleDateString()}
                            </p>
                        </div>

                        {/* Signatures */}
                        <div className="signatures">

                            <div className="sig-block">
                                <div className="gold-seal"></div>

                                <div className="sig-wrapper">
                                    <div className="handwritten-sig">
                                        Chintana B
                                    </div>

                                    <div className="sig-line"></div>

                                    <div className="sig-title">
                                        Founder, SignSync
                                    </div>
                                </div>
                            </div>

                            <div className="sig-block">

                                <div className="sig-wrapper">
                                    <div className="handwritten-sig alt-sig">
                                        SignSync
                                    </div>

                                    <div className="sig-line"></div>

                                    <div className="sig-title">
                                        Authorized Signatory
                                    </div>
                                </div>

                                <div className="gold-seal"></div>

                            </div>

                        </div>

                    </div>
                </div>

                <button
                    onClick={downloadCertificate}
                    className="download-btn"
                >
                    Download PDF
                </button>

            </div>
        </div>
    );
}