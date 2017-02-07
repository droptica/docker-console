<?php

use Step\Acceptance\UserSteps;
use Step\Acceptance\NodeSteps;
use Drupal\Pages\Page;
use Drupal\Pages\HomePage;
use Codeception\Util\Shared\Asserts;
use Codeception\Module\DrupalTestUser;
use \Facebook\WebDriver\Remote\RemoteWebDriver as WebDriver;

class ExampleAcceptanceTestCest
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

  public function _before(AcceptanceTester $I) {
  }

  public function _after(AcceptanceTester $I) {
  }

  /**   TESTS     */

  /**
   * @param \AcceptanceTester $I
   * @param \Step\Acceptance\UserSteps $U
   * @param \Step\Acceptance\NodeSteps $N
   */
  public function exampleTestOfText(AcceptanceTester $I, UserSteps $U, NodeSteps $N) {
    $I->wantTo('Test text');
    $I->see('some text');
  }

  /**
   * @param \AcceptanceTester $I
   */
  public function exampleTestOfOtherText(AcceptanceTester $I) {
    $I->wantTo('Test some other text');
    $I->see('some other text');
  }

}
