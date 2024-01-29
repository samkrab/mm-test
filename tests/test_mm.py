import pytest
import utils


@pytest.fixture(scope="function")
def appium_driver(request):
    driver = utils.initialize_appium_driver()

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver


def test_mm(appium_driver):
    appium_driver.terminate_app("com.playrix.manormatters")
    appium_driver.activate_app("com.playrix.manormatters")
    utils.clear_report()

    assert utils.smart_wait_by_image(appium_driver, 'logo', 20) is not None, \
        "VOKI logo is not presented"
    assert utils.smart_wait_by_image(appium_driver, 'loading', 20) is not None, \
        "Loading not started"
    assert utils.smart_wait_by_image_with_condition(appium_driver, 'play', 'updating', 20, click=True) is not None, \
        "Can't find Play button on the screen"
    assert utils.smart_wait_by_image_with_condition(appium_driver, 'gold', 'skip', 20) is not None, \
        "Seems like game doesn't start correctly"

