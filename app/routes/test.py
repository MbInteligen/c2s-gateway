"""
TEST ROUTES - Testing endpoints for C2S Gateway
All endpoints in this file are for TESTING purposes only
User should DELETE these after testing
"""

from fastapi import APIRouter, HTTPException
from app.core.client import c2s_client
from app.models.schemas import TestLeadCreate, TestMessageCreate

router = APIRouter(prefix="/TEST", tags=["TEST - Testing Endpoints"])


@router.get("/ping")
async def test_ping():
    """TEST - Simple ping endpoint to verify gateway is running"""
    return {
        "status": "ok",
        "message": "TEST - C2S Gateway is running",
        "note": "DELETE this endpoint after testing",
    }


@router.get("/company-info")
async def test_get_company_info():
    """TEST - Get company information to verify authentication"""
    try:
        result = await c2s_client.get_me()
        return {
            "status": "success",
            "message": "TEST - Successfully authenticated with C2S API",
            "data": result,
            "note": "DELETE this endpoint after testing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TEST FAILED: {str(e)}")


@router.get("/list-leads")
async def test_list_leads(page: int = 1, perpage: int = 10):
    """TEST - List first few leads to verify read access"""
    try:
        result = await c2s_client.get_leads(page=page, perpage=perpage)
        return {
            "status": "success",
            "message": f"TEST - Successfully retrieved {perpage} leads from page {page}",
            "data": result,
            "note": "DELETE this endpoint after testing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TEST FAILED: {str(e)}")


@router.get("/list-sellers")
async def test_list_sellers():
    """TEST - List all sellers to verify read access"""
    try:
        result = await c2s_client.get_sellers()
        return {
            "status": "success",
            "message": "TEST - Successfully retrieved sellers",
            "data": result,
            "note": "DELETE this endpoint after testing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TEST FAILED: {str(e)}")


@router.get("/list-tags")
async def test_list_tags():
    """TEST - List all tags to verify read access"""
    try:
        result = await c2s_client.get_tags()
        return {
            "status": "success",
            "message": "TEST - Successfully retrieved tags",
            "data": result,
            "note": "DELETE this endpoint after testing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TEST FAILED: {str(e)}")


@router.get("/list-queues")
async def test_list_queues():
    """TEST - List distribution queues to verify read access"""
    try:
        result = await c2s_client.get_distribution_queues()
        return {
            "status": "success",
            "message": "TEST - Successfully retrieved distribution queues",
            "data": result,
            "note": "DELETE this endpoint after testing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TEST FAILED: {str(e)}")


@router.post("/create-test-lead")
async def test_create_lead(lead: TestLeadCreate):
    """
    TEST - Create a test lead (WRITE OPERATION)
    WARNING: This will create actual data in C2S
    User should DELETE test leads and this endpoint after testing
    """
    try:
        result = await c2s_client.create_lead(lead.model_dump(exclude_none=True))
        return {
            "status": "success",
            "message": "TEST - Successfully created test lead (DELETE THIS LEAD!)",
            "data": result,
            "warning": "You created a TEST lead - remember to DELETE it!",
            "note": "DELETE this endpoint after testing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TEST FAILED: {str(e)}")


@router.post("/create-test-message/{lead_id}")
async def test_create_message(lead_id: str, message: TestMessageCreate):
    """
    TEST - Create a test message on a lead (WRITE OPERATION)
    WARNING: This will create actual data in C2S
    User should DELETE this endpoint after testing
    """
    try:
        result = await c2s_client.create_message(lead_id, message.message, message.type)
        return {
            "status": "success",
            "message": "TEST - Successfully created test message",
            "data": result,
            "note": "DELETE this endpoint after testing",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TEST FAILED: {str(e)}")


@router.get("/full-system-test")
async def test_full_system():
    """
    TEST - Run comprehensive system test (READ-ONLY)
    Tests all major read endpoints to verify gateway functionality
    """
    results = {
        "status": "testing",
        "tests": {},
        "note": "DELETE this endpoint after testing",
    }

    # Test 1: Company Info
    try:
        await c2s_client.get_me()
        results["tests"]["company_info"] = {
            "status": "PASSED",
            "message": "Authentication working",
        }
    except Exception as e:
        results["tests"]["company_info"] = {"status": "FAILED", "error": str(e)}

    # Test 2: List Leads
    try:
        await c2s_client.get_leads(page=1, perpage=1)
        results["tests"]["list_leads"] = {
            "status": "PASSED",
            "message": "Can read leads",
        }
    except Exception as e:
        results["tests"]["list_leads"] = {"status": "FAILED", "error": str(e)}

    # Test 3: List Sellers
    try:
        await c2s_client.get_sellers()
        results["tests"]["list_sellers"] = {
            "status": "PASSED",
            "message": "Can read sellers",
        }
    except Exception as e:
        results["tests"]["list_sellers"] = {"status": "FAILED", "error": str(e)}

    # Test 4: List Tags
    try:
        await c2s_client.get_tags()
        results["tests"]["list_tags"] = {"status": "PASSED", "message": "Can read tags"}
    except Exception as e:
        results["tests"]["list_tags"] = {"status": "FAILED", "error": str(e)}

    # Test 5: List Distribution Queues
    try:
        await c2s_client.get_distribution_queues()
        results["tests"]["list_queues"] = {
            "status": "PASSED",
            "message": "Can read distribution queues",
        }
    except Exception as e:
        results["tests"]["list_queues"] = {"status": "FAILED", "error": str(e)}

    # Determine overall status
    all_passed = all(
        test.get("status") == "PASSED" for test in results["tests"].values()
    )
    all_passed = all(test.get("status") == "PASSED" for test in results["tests"].values())
    results["status"] = "ALL TESTS PASSED ✓" if all_passed else "SOME TESTS FAILED ✗"

    return results
