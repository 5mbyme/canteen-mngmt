const { Builder, By, Key, until } = require('selenium-webdriver');

async function testLogin() {
    let driver = await new Builder().forBrowser('chrome').build();
    try {
        await driver.get('http://localhost:3000/login');
        await driver.sleep(1500);
const emailElement = await driver.findElement(By.id('login-email'));
await driver.wait(until.elementIsVisible(emailElement), 5000);
await emailElement.sendKeys('admin@test.com');
console.log('Email field found and value entered');

const passwordElement = await driver.findElement(By.id('login-password'));
await driver.wait(until.elementIsVisible(passwordElement), 5000);
await passwordElement.sendKeys('admin123456');
console.log('Password field found and value entered');

        // Click submit button
        const loginButton = await driver.findElement(By.css('button[type="submit"]'));
        await loginButton.click();

        // Explicitly wait for navigation off /login
        await driver.wait(async () => {
            const url = await driver.getCurrentUrl();
            return !url.includes('/login');
        }, 10000);

        const currentUrl = await driver.getCurrentUrl();
        if (!currentUrl.includes('/login')) {
            console.log('Login successful!');
        } else {
            console.error('Login failed or did not navigate.');
        }

        await driver.sleep(10000); // Stay after login for observation

    } catch (mainError) {
        console.error('Unexpected error in testLogin:', mainError.message);
    } finally {
        // await driver.quit();
    }
}

testLogin();
