<?php

require_once '/root/composer_codecept/vendor/autoload.php';
require_once '/root/composer_codecept/vendor/codeception/codeception/autoload.php';

use \Codeception\Codecept;

/**
 * This is project's console commands configuration for Robo task runner.
 *
 * @see http://robo.li/
 */
class RoboFile extends \Robo\Tasks
{
  use \Codeception\Task\MergeReports;
  use \Codeception\Task\SplitTestsByGroups;

  public function parallelSplitByFiles($groups_number = 5) {
    $this->codecept = new Codecept();
    // Slip your tests by files.
    $splitter = $this->taskSplitTestFilesByGroups($groups_number);
      $splitter->projectRoot('.')
      ->testsFrom("tests")
      ->groupsTo("tests/_output/parallel_group_")
      ->run();
  }

  public function parallelSplitByTests($groups_number = 5) {
    $this->codecept = new Codecept();
    // Slip your tests by single tests.
    $this->taskSplitTestsByGroups($groups_number)
      ->projectRoot('.')
      ->testsFrom("tests")
      ->groupsTo("tests/_output/parallel_group_")
      ->run();
  }

  public function parallelMergeXMLResults($groups_number) {
    $merge = $this->taskMergeXmlReports();
    for ($i = 1; $i <= $groups_number; $i++) {
      $report_file = "tests/_output/report_parallel_$i.xml";
      if (file_exists($report_file)) {
        $merge->from($report_file);
      }
    }
    $merge->into("tests/_output/report.xml")->run();
  }

  public function parallelMergeHTMLResults($groups_number) {
    $merge = $this->taskMergeHtmlReports();
    for ($i = 1; $i <= $groups_number; $i++) {
      $report_file = "tests/_output/report_parallel_$i.html";
      if (file_exists($report_file)) {
        $merge->from($report_file);
      }
    }
    $merge->into("tests/_output/report.html")->run();
  }
}
