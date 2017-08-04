<?php

namespace Helper;

use \Facebook\WebDriver\Remote\RemoteWebDriver as WebDriver;
use Codeception\Lib\Interfaces\Web as WebInterface;

// here you can define custom actions
// all public methods declared in helper class will be available in $I

class DrupalHelper extends \Codeception\Module {
  /**
   * @param $var
   * this will only run if you run codeception with -d
   * Otherwise this is silent
   */
  public function seeVar($var) {
    $this->debug($var);
  }

  /**
   * Get WebDriver url.
   *
   * @return mixed
   */
  public function getWebDriverUrl() {
    return $this->getModule('WebDriver')->_getConfig('url');
  }

  /**
   * Get WebDriver http auth username.
   *
   * @return mixed
   */
  public function getWebDriverAuthUser() {
    return $this->getModule('WebDriver')->_getConfig('auth_user');
  }

  /**
   * Get WebDriver http auth password.
   *
   * @return mixed
   */
  public function getWebDriverAuthPass() {
    return $this->getModule('WebDriver')->_getConfig('auth_pass');
  }

  /**
   * Get WebDriver http auth timeout.
   *
   * @return mixed
   */
  public function getWebDriverAuthTimeout() {
    return $this->getModule('WebDriver')->_getConfig('auth_timeout');
  }

  /**
   * Perform http authentication for WebDriver.
   *
   * @param WebInterface $I
   *   A reference to the Actor object being used.
   */
  public function webDriverHttpAuthentication ($I) {
    if (method_exists($I, 'executeInSelenium')) {
      $auth_user = $this->getWebDriverAuthUser();
      $auth_pass = $this->getWebDriverAuthPass();
      $auth_timeout = $this->getWebDriverAuthTimeout();
      $url_auth_part = "{$auth_user}:{$auth_pass}@";
      $url = $this->getWebDriverUrl();
      $url = str_replace('http://', "http://{$url_auth_part}", $url);
      $url = str_replace('https://', "https://{$url_auth_part}", $url);
      $I->seeVar($url);
      $I->executeInSelenium(function (WebDriver $webdriver) use (&$curr_window, $auth_timeout, $url) {
        if ($auth_timeout != NULL) {
          $webdriver->manage()->timeouts()->pageLoadTimeout($auth_timeout);
          $webdriver->manage()->timeouts()->setScriptTimeout($auth_timeout);
        }
        $webdriver->get($url);
      });
    }
  }
}
