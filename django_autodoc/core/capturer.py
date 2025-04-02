import os
from typing import Dict, List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class ScreenshotCapturer:
    """Captures screenshots of Django views using Selenium."""
    
    def __init__(
        self,
        base_url: str,
        output_dir: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        login_url: Optional[str] = None,
    ):
        """
        Initialize the screenshot capturer.
        
        Args:
            base_url: Base URL of the running Django application
            output_dir: Directory to save screenshots
            username: Admin username for authenticated views (optional)
            password: Admin password for authenticated views (optional)
            login_url: URL of the login page (optional)
        """
        self.base_url = base_url.rstrip('/')
        self.output_dir = output_dir
        self.username = username
        self.password = password
        self.login_url = login_url or '/admin/login/'
        self.driver = None
        self._setup_driver()
        
    def _setup_driver(self) -> None:
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
    def _login(self) -> bool:
        """
        Perform login if credentials are provided.
        
        Returns:
            bool: True if login successful, False otherwise
        """
        if not (self.username and self.password):
            return False
            
        try:
            self.driver.get(f"{self.base_url}{self.login_url}")
            
            # Wait for login form
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_field = self.driver.find_element(By.NAME, "password")
            
            # Fill in credentials
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            password_field.submit()
            
            # Wait for redirect
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.current_url != f"{self.base_url}{self.login_url}"
            )
            
            return True
            
        except (TimeoutException, WebDriverException) as e:
            print(f"Login failed: {str(e)}")
            return False
            
    def capture_screenshots(self, urls: List[Dict[str, str]]) -> Dict[str, str]:
        """
        Capture screenshots for the provided URLs.
        
        Args:
            urls: List of URL dictionaries with 'pattern' and 'name' keys
            
        Returns:
            Dict mapping URL names to screenshot file paths
        """
        screenshots = {}
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Login if credentials provided
        if self.username and self.password:
            if not self._login():
                print("Warning: Login failed, some screenshots may be incomplete")
        
        for url_info in urls:
            url_pattern = url_info['pattern']
            url_name = url_info['name'] or url_pattern.replace('/', '_').strip('_')
            
            # Skip URL patterns with parameters
            if '<' in url_pattern or '?' in url_pattern:
                continue
                
            try:
                full_url = f"{self.base_url}{url_pattern}"
                self.driver.get(full_url)
                
                # Wait for page load
                WebDriverWait(self.driver, 10).until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
                
                # Take screenshot
                screenshot_path = os.path.join(self.output_dir, f"{url_name}.png")
                self.driver.save_screenshot(screenshot_path)
                screenshots[url_pattern] = screenshot_path
                
            except (TimeoutException, WebDriverException) as e:
                print(f"Failed to capture screenshot for {url_pattern}: {str(e)}")
                continue
                
        return screenshots
        
    def __del__(self):
        """Clean up WebDriver when done."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass 