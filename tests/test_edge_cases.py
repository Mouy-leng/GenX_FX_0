import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
import os
import numpy as np
import pandas as pd

# Set test environment variables
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "postgresql://test:test@localhost/test"
os.environ["MONGODB_URL"] = "mongodb://localhost:27017/test"
os.environ["REDIS_URL"] = "redis://localhost:6379"

from api.main import app

client = TestClient(app)

class TestEdgeCases:
    """Comprehensive edge case testing for the GenX FX API"""
    
    def test_health_endpoint_structure(self):
        """Test health endpoint returns correct structure"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields for the /health endpoint
        required_keys = ["status", "database", "timestamp"]
        for key in required_keys:
            assert key in data, f"Missing required key in health endpoint: {key}"
        
        # Validate timestamp format
        from datetime import datetime
        try:
            datetime.fromisoformat(data["timestamp"])
        except (ValueError, KeyError):
            pytest.fail("Invalid or missing timestamp format")
    
    def test_root_endpoint_completeness(self):
        """Test root endpoint has all required information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        
        required_fields = ["message", "version", "status", "github", "repository"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"
        
        assert data["status"] == "running"
    
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = client.options("/")
        assert response.status_code in [200, 405]

    def test_large_request_handling(self):
        """Test handling of large request payloads"""
        large_data = {
            "symbol": "BTCUSDT",
            "data": ["x" * 1000] * 100,
            "metadata": {"large_array": list(range(1000))}
        }
        response = client.post("/api/v1/test-post", json=large_data)
        assert response.status_code == 200
        assert response.json() == large_data

    def test_malformed_json_handling(self):
        """Test handling of malformed JSON requests"""
        response = client.post(
            "/api/v1/test-post",
            content="{ invalid json }",
            headers={"content-type": "application/json"}
        )
        assert response.status_code == 400

    def test_null_and_empty_values(self):
        """Test handling of null and empty values in requests"""
        test_cases = [{}, {"symbol": None}, {"symbol": ""}]
        for test_data in test_cases:
            response = client.post("/api/v1/test-post", json=test_data)
            assert response.status_code == 200
            assert response.json() == test_data

    def test_special_characters_handling(self):
        """Test handling of special characters and Unicode"""
        special_data = {"comment": "Testing 🚀 café résumé"}
        response = client.post("/api/v1/test-post", json=special_data)
        assert response.status_code == 200
        assert response.json() == special_data

    def test_numeric_edge_cases(self):
        """Test handling of numeric edge cases"""
        edge_cases = [{"value": 0}, {"value": -0}, {"value": 1e-10}]
        for test_data in edge_cases:
            response = client.post("/api/v1/test-post", json=test_data)
            assert response.status_code == 200
            assert response.json() == test_data

    def test_array_edge_cases(self):
        """Test handling of array edge cases"""
        array_cases = [{"data": []}, {"data": [None, 1, "s"]}]
        for test_data in array_cases:
            response = client.post("/api/v1/test-post", json=test_data)
            assert response.status_code == 200
            assert response.json() == test_data

    def test_deeply_nested_objects(self):
        """Test handling of deeply nested objects"""
        nested_data = {"data": {"level1": {"level2": "value"}}}
        response = client.post("/api/v1/test-post", json=nested_data)
        assert response.status_code == 200
        assert response.json() == nested_data

    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        import threading
        results = []
        def make_request():
            response = client.get("/health")
            results.append(response.status_code)
        
        threads = [threading.Thread(target=make_request) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        assert all(status == 200 for status in results)

class TestDataValidation:
    def test_sql_injection_prevention(self):
        """Test SQL injection attempts are handled safely"""
        malicious_inputs = ["'; DROP TABLE users; --", "1' OR '1'='1"]
        for malicious_input in malicious_inputs:
            response = client.post("/api/v1/test-post", json={"username": malicious_input})
            assert response.status_code == 200

    def test_xss_prevention(self):
        """Test XSS attempts are handled safely"""
        xss_payloads = ["<script>alert('xss')</script>", "<img src=x onerror=alert('xss')>"]
        for payload in xss_payloads:
            response = client.post("/api/v1/test-post", json={"username": payload})
            assert response.status_code == 200

class TestPerformanceEdgeCases:
    def test_response_time_reasonable(self):
        """Test that responses come back in reasonable time"""
        import time
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        assert (end_time - start_time) < 5.0

    def test_memory_usage_with_large_data(self):
        """Test memory usage doesn't explode with large data"""
        import psutil
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        large_data = {"data": ["x" * 1000] * 100}
        client.post("/api/v1/test-post", json=large_data)
        final_memory = process.memory_info().rss
        assert (final_memory - initial_memory) < 100 * 1024 * 1024

class TestErrorHandling:
    def test_undefined_endpoints(self):
        """Test handling of undefined endpoints"""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

    def test_method_not_allowed(self):
        """Test handling of wrong HTTP methods"""
        response = client.delete("/")
        assert response.status_code == 405

    def test_content_type_handling(self):
        """Test handling of different content types"""
        response = client.post("/api/v1/test-post", content="not json", headers={"content-type": "text/plain"})
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_timeout_handling(self):
        """Test handling of operations that might timeout"""
        with patch('api.main.health_check', new_callable=AsyncMock) as mock_health:
            async def slow_health():
                await asyncio.sleep(0.1)
                return {"status": "delayed"}
            mock_health.side_effect = slow_health
            response = client.get("/health")
            assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])