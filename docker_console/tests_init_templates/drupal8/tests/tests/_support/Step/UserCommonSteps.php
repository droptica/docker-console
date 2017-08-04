<?php

namespace Step;

use Drupal\Pages\UserLoginPage;
use Drupal\Pages\HomePage;

/**
 * Class UserCommonSteps
 * @package Step
 */
trait UserCommonSteps {

  /**
   * Login user.
   *
   * @param string $username
   *   Username.
   * @param string $password
   *   Password.
   */
  public function login($username = 'admin', $password = 'admin')
  {
    /** @var \AcceptanceTester $I */
    $I = $this;
    $I->amOnPage(UserLoginPage::route());
    $url = rtrim($I->grabFromCurrentUrl(), '/');
    $I->seeVar($url);
    if ($url != '/user/login') {
      $this->logout();
      $I->amOnPage(UserLoginPage::route());
    }
    $I->fillField(UserLoginPage::$loginFormUsername, $username);
    $I->fillField(UserLoginPage::$loginFormPassword, $password);
    $I->click(UserLoginPage::$loginFormSubmit);
    $I->amOnPage(UserLoginPage::route());
    $I->seeCurrentUri();
    // If user is logged in correctly, he should be redirected from User Login page.
    $I->dontSeeCurrentUrlMatches('/^(' . preg_quote(UserLoginPage::route(), '/') . ')/');
  }

  /**
   * Logout user.
   */
  public function logout()
  {
    /** @var \AcceptanceTester $I */
    $I = $this;
    $I->amOnPage('/user/logout');
    $I->see('Log in');
  }

  /**
   * Check if user is logged in.
   */
  public function userIsLoggedIn()
  {
    /** @var \AcceptanceTester $I */
    $I = $this;
    $I->amOnPage(HomePage::route());
    $I->see('Log out');
  }
}
