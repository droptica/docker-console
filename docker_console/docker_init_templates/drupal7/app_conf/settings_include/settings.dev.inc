<?php

$conf['securepages_enable'] = FALSE;
$conf['reroute_email_enable'] = TRUE;
$conf['cache'] = FALSE; //page cache
$conf['block_cache'] = FALSE; //block cache
$conf['preprocess_css'] = FALSE; //optimize css
$conf['preprocess_js'] = FALSE; //optimize javascript
error_reporting(-1);
$conf['error_level'] = 2;
ini_set('display_errors', TRUE);
ini_set('display_startup_errors', TRUE);
