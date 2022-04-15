<?php
session_start();

if (isset($_GET['license'])) {
header("Content-Type: image/png");
readfile('licenses/'.$_SESSION['name'].'.png');
} elseif (isset($_GET['advert'])) {
readfile('media/advert.jpg');
}
?>