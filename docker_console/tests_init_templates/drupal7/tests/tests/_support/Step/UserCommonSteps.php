<?php

namespace Step;

use Drupal\Pages\UserLoginPage;
use Drupal\Pages\HomePage;

/**
 * Class UserCommonSteps
 * @package Step
 */
trait UserCommonSteps
{

  /**
   * Login user.
   *
   * @param string $username
   * @param string $password
   */
  public function login($username = 'admin', $password = '123')
  {
    /** @var \AcceptanceTester $I */
    $I = $this;
    $I->amOnPage(UserLoginPage::route());
    $url = $I->grabFromCurrentUrl();
    $I->seeVar($url);
    if ($url != '/user/login') {
      $this->logout();
      $I->amOnPage(UserLoginPage::route());
    }
    $I->fillField(UserLoginPage::$loginFormUsername, $username);
    $I->fillField(UserLoginPage::$loginFormPassword, $password);
    $I->click('Log in');
    $I->seeCurrentUri();
    $I->seeCurrentUrlEquals('/');
    $I->see('Log out');
  }

  /**
   * Logout user.
   */
  public function logout()
  {
    /** @var \AcceptanceTester $I */
    $I = $this;
    $I->amOnPage(HomePage::route());
    $I->click('Log out');
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
