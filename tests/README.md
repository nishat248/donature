# Comprehensive Selenium Testing Suite

## Overview

This is a comprehensive Selenium testing suite for the Donation Management System. It covers all user types (Donor/Recipient, NGO, Admin) and their complete workflows including authentication, donations, requests, campaigns, reviews, and admin approvals.

## Test Coverage

### 📊 Test Statistics
- **Total Tests**: ~43 comprehensive tests
- **Authentication**: 7 tests
- **Donor Flows**: 13 tests  
- **NGO Flows**: 11 tests
- **Admin Flows**: 12 tests

### 🎯 Features Tested

#### Donor/Recipient Features
- ✅ User signup with profile data
- ✅ Login/logout functionality
- ✅ Create donation items with images and categories
- ✅ Browse donations with filters (category, location, urgency)
- ✅ Claim donations from other users
- ✅ Create request items (needs admin approval)
- ✅ Browse approved requests and donate to them
- ✅ Mark donations as received
- ✅ Submit reviews after completed claims
- ✅ View and update profile
- ✅ Upload profile pictures
- ✅ View rewards and points system
- ✅ View notifications

#### NGO Features
- ✅ NGO signup with registration certificate
- ✅ Login after admin approval
- ✅ Create campaigns (needs admin approval)
- ✅ Edit and delete campaigns
- ✅ View "My Campaigns" with status
- ✅ Add campaign updates
- ✅ View donation history
- ✅ Browse public campaigns
- ✅ Track campaign progress

#### Admin Features
- ✅ Admin login and dashboard access
- ✅ View system statistics
- ✅ Approve/reject NGO registrations
- ✅ Approve/reject campaigns
- ✅ Approve/reject donation requests
- ✅ Manage users, donations, claims, categories
- ✅ Create new admins
- ✅ Manage rewards system
- ✅ View contact messages
- ✅ Update admin profile



## Prerequisites

### Required Software
1. **Python 3.8+**
2. **ChromeDriver** - Download from [ChromeDriver Downloads](https://chromedriver.chromium.org/)
3. **Chrome Browser** - Latest version recommended

### Required Python Packages
```bash
pip install pytest
pip install pytest-django
pip install selenium
pip install pillow
pip install reportlab
```

### ChromeDriver Setup
1. Download ChromeDriver matching your Chrome version
2. Extract the executable
3. Update the path in `conftest.py`:
   ```python
   driver_path = r"D:\3.2\SoftwareLab\chromedriver\chromedriver.exe"  # Update this path
   ```

## Running Tests

### Run All Tests
```bash
# From the project root directory
pytest tests/ -v
```

### Run Specific Test Files
```bash
# Authentication tests
pytest tests/test_01_authentication.py -v

# Donor flow tests
pytest tests/test_02_donor_flows.py -v

# NGO flow tests
pytest tests/test_03_ngo_flows.py -v

# Admin flow tests
pytest tests/test_04_admin_flows.py -v


### Run Specific Test Classes
```bash
# Run only authentication tests
pytest tests/test_01_authentication.py::TestAuthentication -v

# Run only donor flow tests
pytest tests/test_02_donor_flows.py::TestDonorFlows -v
```

### Run Specific Test Methods
```bash
# Run only donor login test
pytest tests/test_01_authentication.py::TestAuthentication::test_donor_login -v

# Run only donation creation test
pytest tests/test_02_donor_flows.py::TestDonorFlows::test_create_donation_item -v
```

### Run Tests with Screenshots
```bash
# Tests automatically take screenshots on failure
pytest tests/ -v --tb=short
```

## Test Configuration

### Database Safety
- ✅ Tests use a separate test database (`test_db.sqlite3`)
- ✅ Your production database (`db.sqlite3`) is never touched
- ✅ Test database is automatically created and destroyed
- ✅ Each test runs in isolation with fresh data

### Test Data
- ✅ Comprehensive fixtures for users, categories, donations, campaigns
- ✅ Realistic test data with proper relationships
- ✅ Automatic cleanup after each test

### Browser Configuration
- ✅ Chrome browser with maximized window
- ✅ Explicit waits instead of sleep() for reliability
- ✅ Automatic screenshot capture on failures
- ✅ Mobile responsiveness testing

## Test Structure

```
donature/tests/
├── conftest.py                    # Enhanced fixtures and configuration
├── test_selenium.py               # Basic smoke tests (kept from original)
├── test_01_authentication.py         # Signup/login tests for all user types
├── test_02_donor_flows.py           # Complete donor/recipient workflows
├── test_03_ngo_flows.py             # NGO campaign management workflows
├── test_04_admin_flows.py           # Admin panel and approval workflows
├── test_helpers.py               # Utility functions for tests
├── fixtures/
│   └── test_data.py             # Test data generators
├── temp/                         # Temporary test files (auto-created)
└── screenshots/                  # Failure screenshots (auto-created)
```

## Helper Functions

### Available in `test_helpers.py`
- `login_user(driver, live_server, username, password)` - Handle modal login
- `wait_for_element(driver, by, value, timeout=10)` - Explicit waits
- `fill_form_field(driver, name, value)` - Form filling
- `upload_file(driver, field_name, file_path)` - File uploads
- `take_screenshot(driver, name)` - Debug screenshots
- `create_test_image()` - Generate test images dynamically
- `create_test_document()` - Generate test documents

## Troubleshooting

### Common Issues

#### 1. ChromeDriver Not Found
```
Error: 'chromedriver' executable needs to be in PATH
```
**Solution**: Update the `driver_path` in `conftest.py` to point to your ChromeDriver executable.

#### 2. Chrome Version Mismatch
```
Error: This version of ChromeDriver only supports Chrome version X
```
**Solution**: Download ChromeDriver version matching your Chrome browser version.

#### 3. Test Database Issues
```
Error: Database is locked
```
**Solution**: Make sure no other Django processes are running. Stop the development server before running tests.

#### 4. Element Not Found
```
Error: Timeout waiting for element
```
**Solution**: Check if the page structure has changed. Update selectors in test files if needed.

#### 5. Modal Not Opening
```
Error: Login modal not found
```
**Solution**: Check if the homepage modal structure has changed. Update selectors in `test_helpers.py`.

### Debug Mode
To run tests with more verbose output:
```bash
pytest donature/tests/ -v -s --tb=long
```

### Screenshot Debugging
Screenshots are automatically saved to `donature/tests/screenshots/` on test failures. Check these for visual debugging.

## Test Data Management

### Fixtures Available
- `donor_user` - Donor with profile and rewards
- `donor_user2` - Second donor for interaction tests
- `ngo_user` - Approved NGO with profile
- `pending_ngo_user` - Unapproved NGO for testing
- `admin_user` - Admin user
- `categories` - Sample donation categories
- `campaign_categories` - Sample campaign categories
- `sample_donations` - Pre-created donation items
- `sample_campaigns` - Pre-created campaigns
- `sample_requests` - Pre-created request items
- `rewards` - Reward tiers
- `test_image_path` - Generated test image
- `test_document_path` - Generated test document

### Custom Test Data
To add custom test data, modify the fixtures in `conftest.py` or create new fixtures in `fixtures/test_data.py`.

## Performance Considerations

### Test Execution Time
- **Individual tests**: 2-5 seconds each
- **Full suite**: 11 minutes
- **Parallel execution**: Not recommended due to database conflicts

### Optimization Tips
1. Use `scope="module"` for expensive fixtures
2. Reuse browser instances where possible
3. Clean up test files regularly
4. Use explicit waits instead of sleep()

## Continuous Integration

### GitHub Actions Example
```yaml
name: Selenium Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-django selenium
    - name: Install Chrome
      run: |
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
    - name: Install ChromeDriver
      run: |
        CHROME_VERSION=$(google-chrome --version | cut -d' ' -f3 | cut -d'.' -f1)
        wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}/chromedriver_linux64.zip"
        sudo unzip /tmp/chromedriver.zip -d /usr/local/bin/
        sudo chmod +x /usr/local/bin/chromedriver
    - name: Run tests
      run: pytest donature/tests/ -v
```

## Contributing

### Adding New Tests
1. Create test methods in appropriate test files
2. Use existing fixtures when possible
3. Follow naming convention: `test_feature_description`
4. Add proper assertions and error messages
5. Update this README if adding new test categories

### Test Guidelines
1. **Independence**: Each test should be independent
2. **Cleanup**: Clean up any created data
3. **Reliability**: Use explicit waits, not sleep()
4. **Clarity**: Use descriptive test names and comments
5. **Coverage**: Test both success and failure scenarios

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review test screenshots for visual debugging
3. Check Django logs for backend errors
4. Verify ChromeDriver compatibility

---

**Note**: This testing suite is designed for the Donation Management System and covers all major user workflows. It ensures the application works correctly across different user types and scenarios.

