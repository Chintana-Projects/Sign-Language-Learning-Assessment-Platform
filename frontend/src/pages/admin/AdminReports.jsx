import { useState } from "react";

export default function AdminReports() {

    const [downloading, setDownloading] =
        useState(false);

    const downloadExcelReport = async () => {

        try {

            setDownloading(true);

            const response = await fetch(
                "http://127.0.0.1:8000/admin/reports/export"
            );

            if (!response.ok) {
                throw new Error(
                    "Failed to download report"
                );
            }

            const blob =
                await response.blob();

            const url =
                window.URL.createObjectURL(blob);

            const link =
                document.createElement("a");

            link.href = url;

            link.download =
                "SignSync_Admin_Report.xlsx";

            document.body.appendChild(link);

            link.click();

            link.remove();

            window.URL.revokeObjectURL(url);

        } catch (error) {

            console.error(
                "Download error:",
                error
            );

            alert(
                "Unable to download report."
            );

        } finally {

            setDownloading(false);

        }
    };

    return (

        <div
            style={{
                padding: "30px"
            }}
        >
            <h1>
                Reports
            </h1>

            <p>
                Generate platform analytics reports.
            </p>

            <div
                style={{
                    marginTop: "30px"
                }}
            >
                <button
                    onClick={
                        downloadExcelReport
                    }
                    disabled={downloading}
                    style={{
                        padding:
                            "12px 20px",
                        border: "none",
                        borderRadius:
                            "8px",
                        background:
                            "#4F46E5",
                        color: "#FFF",
                        cursor:
                            "pointer"
                    }}
                >
                    {downloading
                        ? "Generating..."
                        : "📊 Export Excel Report"}
                </button>
            </div>
        </div>
    );
}