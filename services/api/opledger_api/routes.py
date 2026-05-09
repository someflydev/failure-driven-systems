"""Aggregate router for the modular monolith API surface."""

from fastapi import APIRouter

from opledger_api.async_jobs import router as async_jobs_router
from opledger_api.customers import router as customers_router
from opledger_api.notifications import router as notifications_router
from opledger_api.reports import router as reports_router
from opledger_api.work_requests import router as work_requests_router

router = APIRouter()
router.include_router(customers_router)
router.include_router(work_requests_router)
router.include_router(reports_router)
router.include_router(async_jobs_router)
router.include_router(notifications_router)
