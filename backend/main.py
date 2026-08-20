from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ---------------------------------------------------------
# API Imports
# ---------------------------------------------------------
from app.routers.instructor import router as instructor_router
from app.api.analytics import router as analytics_router
from app.api.dashboard import router as dashboard_router
from app.api.health import router as health_router
from app.api.predict import router as predict_router
from app.api.lessons import router as lessons_router
from app.api.practice import router as practice_router
from app.api.preprocess import router as preprocess_router
from app.api.prediction import router as prediction_router
from app.api.review import router as review_router
from app.api.recommendations import router as recommendation_router
from app.api.learner import router as learner_router
from app.api.instructor_dashboard_router import router as instructor_dashboard_router
from app.routers.auth_router import router as auth_router
from app.core.logging_config import setup_logging
from app.api.assessment import router as assessment_router
from app.api.users import router as users_router
from app.routers.user_router import router as user_router
from app.reports.report_router import router as report_router
# ---------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------

logger = setup_logging()





# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(

    title="SignSync API",

    version="1.0.0"

)





# ---------------------------------------------------------
# CORS Configuration
# ---------------------------------------------------------

app.add_middleware(

    CORSMiddleware,


    allow_origins=[

        "http://localhost:5173",

        "http://127.0.0.1:5173",

    ],


    allow_credentials=True,


    allow_methods=["*"],


    allow_headers=["*"],

)





# ---------------------------------------------------------
# Register API Routers
# ---------------------------------------------------------

app.include_router(
    health_router
)
app.include_router(
    users_router
)
app.include_router(user_router)

app.include_router(
    predict_router
)
app.include_router(report_router)
app.include_router(instructor_dashboard_router)

app.include_router(
    lessons_router
)
app.include_router(instructor_router)
app.include_router(assessment_router)
app.include_router(
    practice_router
)
app.include_router(
    dashboard_router
)

app.include_router(
    preprocess_router
)

app.include_router(auth_router)
app.include_router(
    analytics_router
)
app.include_router(
    learner_router
)

app.include_router(
    prediction_router
)


app.include_router(
    review_router
)

app.include_router(
    recommendation_router
)







# ---------------------------------------------------------
# Startup Event
# ---------------------------------------------------------

@app.on_event("startup")
def startup_event():

    logger.info(
        "SignSync backend started"
    )