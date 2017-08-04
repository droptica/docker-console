<?php

/**
 * @file
 * Example acceptance test cest.
 */

use Step\Acceptance\UserSteps;
use Step\Acceptance\NodeSteps;
use Drupal\Pages\HomePage;
use Drupal\Pages\NodePage;
use Codeception\Util\Shared\Asserts;


/**
 * Class ExampleAcceptanceTestCest
 */
class ExampleAcceptanceTestCest {

  use Asserts;

  /**
   * Node type.
   *
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
   * Example homepage test.
   *
   * @param \AcceptanceTester $I
   */
  public function exampleHomepageTest(AcceptanceTester $I) {
    $I->wantTo('Test homepage.');
    $I->amOnPage(HomePage::route());
    $I->see('some text');
    $page_title = $I->grabTextFrom(HomePage::$pageTitle);
    $I->seeVar($page_title);
    $this->assertContains('some page title', $page_title);
  }

  /**
   * Example see node page test as logged in user.
   *
   * @param \AcceptanceTester $I
   * @param \Step\Acceptance\UserSteps $U
   */
  public function exampleNodePageTest(AcceptanceTester $I, UserSteps $U) {
    $I->wantTo('See node page as logged in user.');
    $U->login('username', 'password');
    $nid = 123;
    $I->amOnPage(NodePage::route($nid));
    $I->see('some other text');
    $U->logout();
  }

  /**
   * Example node create test.
   *
   * @param \AcceptanceTester $I
   * @param \Step\Acceptance\NodeSteps $N
   */
  public function exampleNodeCreateTest(AcceptanceTester $I, NodeSteps $N) {
    $I->wantTo("Create node of type: {$this->node_type}.");

    $node_values = array(
      'title' => 'test node title',
      'body' => 'test node body',
    );

    $nid = $N->createNewNodeAsUser('some_test_user', $this->node_type, $node_values);
    $I->setVariableToStorage('new_node_nid', $nid);
  }

  /**
   * Example see created node page test.
   *
   * @param \AcceptanceTester $I
   * @param \Step\Acceptance\UserSteps $U
   * @param \Step\Acceptance\NodeSteps $N
   */
  public function exampleSeeCreatedNodeTest(AcceptanceTester $I, UserSteps $U, NodeSteps $N) {
    $I->wantTo("See created node.");
    $U->login('username', 'password');
    $nid = $I->getVariableFromStorage('new_node_nid');
    $N->seeNodePage($nid);
    $U->logout();
  }

  /**
   * Example node delete test.
   *
   * @param \AcceptanceTester $I
   * @param \Step\Acceptance\NodeSteps $N
   */
  public function exampleDeleteNodeTest(AcceptanceTester $I, NodeSteps $N) {
    $I->wantTo('Delete test node.');
    $nid = $I->getVariableFromStorage('new_node_nid');
    $N->deleteNodeAsUser('some_test_user', $nid);
  }
}
