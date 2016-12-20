<?php
namespace Helper;

// here you can define custom actions
// all public methods declared in helper class will be available in $I

class DrupalHelper extends \Codeception\Module
{
  /**
   * @var
   */
  private $session_limit_behaviour_default;

  public function _beforeSuite($settings = array())
  {
    $session_limit_behaviour = variable_get('session_limit_behaviour');
    if (isset($session_limit_behaviour)) {
      $this->session_limit_behaviour_default = $session_limit_behaviour;
      if (defined('SESSION_LIMIT_DROP')) {
        variable_set('session_limit_behaviour', SESSION_LIMIT_DROP);
      }
    }
  }

  public function _afterSuite()
  {
    if (isset($this->session_limit_behaviour_default)) {
      variable_set('session_limit_behaviour', $this->session_limit_behaviour_default);
    }
  }

  /**
   * @param $var
   * this will only run if you run codeception with -d
   * Otherwise this is silent
   */
  public function seeVar($var){
    $this->debug($var);
  }

}
