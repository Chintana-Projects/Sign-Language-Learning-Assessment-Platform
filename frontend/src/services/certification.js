const API =
    "http://127.0.0.1:8000";

export async function startCertification() {

    const response =
        await fetch(
            `${API}/certification/start`,
            {
                method: "POST"
            }
        );

    return await response.json();

}