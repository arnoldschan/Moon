


<html lang="en">
<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>Display Instagram Posts On Website - BASIC - Live Demo</title>

    <link rel="stylesheet" href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css">
<style>

    item_box{
        height:500px;
    }

    .photo-thumb{
        width:100%;
        height:auto;
        float:left;
        border: thin solid #d1d1d1;
        margin:0 1em .5em 0;
        float:left;
    }
    </style>

</head>
<body>

<div class="container">
<div class="row">
  <div class="col-lg-12">
     <div class="page-header">
       {% raw %}<?php
$client_id= '736e92b0331a42868971d7bd099e354d';
$client_secret= '7d0f208feb65477fba1d691969c2378e';
$redirect_uri= 'http://localhost:4000/auth';
$code= '46372804af934d4f90f1dc41d8d41c0e';
$url='https://api.instagram.com/oauth/access_token';
$data = array(
    'client_id'=> $client_id,
    'client_secret' => $client_secret,
    'grant_type' =>'authorization_code',
    'redirect_uri' =>$redirect_uri,
    'code' =>$code );
$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($data)
    )
);
$context  = stream_context_create($options);
$json = file_get_contents($url, false, $context);

$obj = json_decode($json, true, 512, JSON_BIGINT_AS_STRING);
// foreach ($obj['data'] as $post) {
//
//     $pic_text=$post['caption']['text'];
//     $pic_link=$post['link'];
//     $pic_like_count=$post['likes']['count'];
//     $pic_comment_count=$post['comments']['count'];
//     $pic_src=str_replace("http://", "https://", $post['images']['standard_resolution']['url']);
//     $pic_created_time=date("F j, Y", $post['caption']['created_time']);
//     $pic_created_time=date("F j, Y", strtotime($pic_created_time . " +1 days")); -->

    echo "<p>$obj['username']</p>";

//     <!--echo "<div class='col-md-4 col-sm-6 col-xs-12 item_box'>";
//         echo "<a href='{$pic_link}' target='_blank'>";
//             echo "<img class='img-responsive photo-thumb' src='{$pic_src}' alt='{$pic_text}'>";
//         echo "</a>";
//         echo "<p>";
//             echo "<p>";
//                 echo "<div style='color:#888;'>";
//                     echo "<a href='{$pic_link}' target='_blank'>{$pic_created_time}</a>";
//                 echo "</div>";
//             echo "</p>";
//             echo "<p>{$pic_text}</p>";
//         echo "</p>";
//     echo "</div>";
// } -->

?>{% endraw %}

         <h1>Display Instagram Feed On Website - BASIC - Live Demo</h1>
     </div>
 </div>
<!-- Instagram feed will be here -->

</div>
</div>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
<script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>

<!--[if lt IE 9]>
<script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
<script src="https://oss.maxcdn.com/libs/respond.js/1.4.2/respond.min.js"></script>
<![endif]-->

</body>
</html>