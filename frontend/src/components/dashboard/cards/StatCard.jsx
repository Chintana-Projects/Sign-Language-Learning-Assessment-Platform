
export default function StatCard({
    title,
    value,
    icon,
    color = "#4F46E5"
}) {
    return (
        <div
            className="stat-card"
            style={{
                "--stat-color": color
            }}
        >

            {/* =====================================
                ICON
            ===================================== */}

            <div className="stat-card-icon">
                {icon}
            </div>


            {/* =====================================
                CONTENT
            ===================================== */}

            <div className="stat-card-content">

                <span className="stat-card-title">
                    {title}
                </span>

                <span className="stat-card-value">
                    {value}
                </span>

            </div>

        </div>
    );
}