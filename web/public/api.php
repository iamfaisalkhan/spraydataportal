<?php

$findquery = array();

if (isset($_POST["q"]))
{
    $findquery = parseParameters($_POST["q"]);
}


// print_r($findquery);

$mongoDB = new Mongo();
$database = $mongoDB->spraydataportal;
$collection = $database->dataset;

$response = array();

$cursor = $collection->find($findquery);

foreach ($cursor as $document)
{
    $response[] = formatResult($document);
}

header('Content-Type: application/json');
header('Cache-Control: no-cache');
header('Access-Control-Allow-Origin: *');

echo json_encode($response);


function parseParameters($params)
{

    $query = array();

    $tokens = explode(",", $params);

    foreach ($tokens as $token) 
    {
        $res = explode("=", $token);
        if (count($res) > 1)
        {
            $query[trim($res[0])] = trim($res[1]);
        }
    }

    return $query;

}

function formatResult($document)
{
    return $document;
}

?>