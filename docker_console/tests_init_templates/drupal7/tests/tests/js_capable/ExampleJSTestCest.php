<?php

use Step\JSCapable\NodeSteps;
use Step\JSCapable\UserSteps;
use Drupal\Pages\Page;
use Drupal\Pages\HomePage;
use Codeception\Util\Shared\Asserts;
use Codeception\Module\DrupalTestUser;
use \Facebook\WebDriver\Remote\RemoteWebDriver as WebDriver;

class ExampleJSTestCest
{

  use Asserts;

  /**
   * @var string
   * node type machine name
   */
  private $node_type;

  function __construct() {
    $this->node_type = 'content_type_name';
  }

  public function _before(JSCapableTester $I) {
    $I->executeInSelenium(function (WebDriver $webdriver) use (&$curr_window) {
      $webdriver->manage()->timeouts()->pageLoadTimeout(1200);
      $webdriver->manage()->timeouts()->setScriptTimeout(1200);
      $webdriver->get('http://user:pass@web');
    });
  }

  public function _after(JSCapableTester $I) {
  }

  /**   TESTS     */

  /**
   * @param \JSCapableTester $I
   * @param \Step\JSCapable\UserSteps $U
   * @param \Step\JSCapable\NodeSteps $N
   */
  public function exampleTestOfText(JSCapableTester $I, UserSteps $U, NodeSteps $N) {
    $I->wantTo('Test text');
    $I->see('some text');
  }

  /**
   * @param \JSCapableTester $I
   */
  public function exampleTestOfOtherText(JSCapableTester $I) {
    $I->wantTo('Test some other text');
    $I->see('some other text');
  }

}
