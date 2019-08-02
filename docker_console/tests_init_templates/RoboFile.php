<?php

require_once '/root/composer_codecept/vendor/autoload.php';
require_once '/root/composer_codecept/vendor/codeception/codeception/autoload.php';

use \Codeception\Codecept;
use Symfony\Component\Finder\Finder;

/**
 * This is project's console commands configuration for Robo task runner.
 *
 * @see http://robo.li/
 */
class RoboFile extends \Robo\Tasks
{
  use \Codeception\Task\MergeReports;
  use \Codeception\Task\SplitTestsByGroups;

  public function parallelSplitByFiles($groups_number = 5, $suites = '') {
    $this->codecept = new Codecept();
    // Slip your tests by files.
    $splitter = $this->taskSplitTestFilesByGroups($groups_number);
      $splitter->projectRoot('.')
      ->testsFrom('tests', $suites)
      ->groupsTo('tests/_output/parallel_group_')
      ->run();
  }

  public function parallelSplitByTests($groups_number = 5, $suites = '') {
    $this->codecept = new Codecept();
    // Slip your tests by single tests.
    $this->taskSplitTestsByGroups($groups_number)
      ->projectRoot('.')
      ->testsFrom('tests', $suites)
      ->groupsTo('tests/_output/parallel_group_')
      ->run();
  }

  public function parallelMergeXMLResults() {
    $merge = $this->taskMergeXmlReports();
    $files = Finder::create()
      ->name('report_parallel_group_*.xml')
      ->path('tests/_output')
      ->in('.')
      ->sortByName();

    /** @var SplFileInfo $file */
    foreach ($files as $file) {
      $merge->from($file->getRelativePathname());
    }
    $merge->into("tests/_output/report.xml")->run();
  }

  public function parallelMergeHTMLResults() {
    $merge = $this->taskMergeHtmlReports();
    $files = Finder::create()
      ->name('report_parallel_group_*.html')
      ->path('tests/_output')
      ->in('.')
      ->sortByName();

    /** @var SplFileInfo $file */
    foreach ($files as $file) {
      $merge->from($file->getRelativePathname());
    }
    $merge->into("tests/_output/report.html")->run();
  }
}
