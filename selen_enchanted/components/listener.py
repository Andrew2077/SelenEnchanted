"""
listener.py

This module contains the Listener class, which provides methods to listen to network traffic using Selenium WebDriver.

Classes:
--------
Listener
    A class to listen to and capture network traffic.

"""

import json
from collections import defaultdict

from ..utilities.logger import Logger
from selenium.webdriver.remote.webdriver import WebDriver


class Listener:
    """
    Listener class to listen to network traffic.

    Attributes:
        driver (WebDriver): The Selenium WebDriver instance.
        logger (Logger): The logger instance for logging errors and information.
    """
    def __init__(self, driver: WebDriver, logger: Logger):
        self.all_requests = []
        self.persistent_requests = []
        self.processed_request_ids = set()  # Track already processed request IDs
        self._url_contains_list = []
        self._url_matches_list = []
        self.driver = driver
        self.logger = logger

    def set_url_contains_list(self, url_contains_list: list):
        """Set the list of URL patterns to match (contains)."""
        self._url_contains_list = url_contains_list if url_contains_list else []

    def set_url_matches_list(self, url_matches_list: list):
        """Set the list of URL patterns to match (exact)."""
        self._url_matches_list = url_matches_list if url_matches_list else []

    def get_url_contains_list(self):
        """Get the list of URL patterns to match (contains)."""
        return self._url_contains_list

    def get_url_matches_list(self):
        """Get the list of URL patterns to match (exact)."""
        return self._url_matches_list

    def _should_capture_url(self, url: str) -> bool:
        """
        Check if the URL should be captured based on configured patterns.
        If both lists are empty, capture all URLs.
        """
        # If both lists are empty, capture all URLs
        if not self._url_contains_list and not self._url_matches_list:
            return True
        
        # Check if URL matches any pattern in url_contains_list
        if self._url_contains_list:
            if any(pattern in url for pattern in self._url_contains_list):
                return True
        
        # Check if URL exactly matches any pattern in url_matches_list
        if self._url_matches_list:
            if url in self._url_matches_list:
                return True
        
        return False

    def setup_network_capture(self):
        """
        Setup and start network capture.
        Returns a function that when called will capture new network traffic since the last call.
        """
        pending_requests = defaultdict(dict)
        self.processed_request_ids = set()  # Reset processed request IDs
        
        def capture_network_traffic():
            """Capture network traffic and return new requests."""
            new_requests = []  # Store only new requests for this capture call
            
            try:
                logs_raw = self.driver.get_log("performance")
                logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
            except Exception as e:
                self.logger.error(f"Error getting performance logs: {str(e)}")
                return self.persistent_requests
            
            # Process logs
            for log in logs:
                method = log.get("method", "")
                params = log.get("params", {})
                
                # Handle request sent
                if method == "Network.requestWillBeSent":
                    self._handle_request_sent(params, pending_requests)
                
                # Handle response received
                elif method == "Network.responseReceived":
                    self._handle_response_received(params, pending_requests)
                
                # Handle loading finished
                elif method == "Network.loadingFinished":
                    request_data = self._handle_loading_finished(params, pending_requests)
                    if request_data:
                        new_requests.append(request_data)
            
            # Clean up completed requests to avoid memory leaks
            self._cleanup_pending_requests(pending_requests)
            
            # Combine persistent requests with new requests
            combined_requests = self.persistent_requests + new_requests
            
            # Clear persistent requests after combining
            self.persistent_requests = []
            
            return combined_requests
        
        return capture_network_traffic

    def _handle_request_sent(self, params: dict, pending_requests: dict):
        """Handle Network.requestWillBeSent event."""
        request = params.get("request", {})
        request_id = params.get("requestId")
        request_url = request.get("url", "")
        
        if not request_id:
            return
        
        # Check if the request URL should be captured
        if self._should_capture_url(request_url) and request_id not in self.processed_request_ids:
            pending_requests[request_id].update({
                "url": request_url,
                "method": request.get("method"),
                "requestId": request_id,
                "headers": request.get("headers", {}),
                "postData": request.get("postData", ""),
                "cookies": request.get("cookies", {}),
            })

    def _handle_response_received(self, params: dict, pending_requests: dict):
        """Handle Network.responseReceived event."""
        request_id = params.get("requestId")
        
        if not request_id or request_id not in pending_requests:
            return
        
        response = params.get("response", {})
        pending_requests[request_id]["status"] = response.get("status")
        
        # Save response cookies if available
        if "cookies" in response:
            pending_requests[request_id]["response_cookies"] = response.get("cookies", {})

    def _handle_loading_finished(self, params: dict, pending_requests: dict):
        """Handle Network.loadingFinished event and return request data if complete."""
        request_id = params.get("requestId")
        
        if not request_id or request_id not in pending_requests:
            return None
        
        request_data = pending_requests[request_id]
        request_url = request_data.get("url", "")
        
        # Check if this request should be captured and hasn't been processed yet
        if not self._should_capture_url(request_url) or request_id in self.processed_request_ids:
            return None
        
        try:
            # Get response body
            response_body = self.driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id})
            body = response_body.get("body", "")
            
            # Try to parse as JSON
            try:
                body_json = json.loads(body)
                # Remove extensions key if it exists to save memory
                body_json.pop("extensions", None)
                request_data["body"] = body_json

            except json.JSONDecodeError:
                request_data["body"] = body
            
            # Add browser cookies
            request_data["browser_cookies"] = self.driver.get_cookies()
            
            # Add to the global all_requests list
            self.all_requests.append(request_data)
            
            # Mark this request as processed
            self.processed_request_ids.add(request_id)
            
            return request_data
            
        except Exception as e:
            # Handle the specific error when resource is not found
            if "No resource with given identifier found" not in str(e):
                self.logger.info(f"Error getting response body for request {request_id}: {str(e)}")
        
        return None

    def _cleanup_pending_requests(self, pending_requests: dict):
        """Clean up completed requests to avoid memory leaks."""
        for request_id in list(pending_requests.keys()):
            if request_id in self.processed_request_ids:
                del pending_requests[request_id]
