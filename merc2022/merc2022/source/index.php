<?php include('server.php') ?>
<?php 
  if (isset($_SESSION['merc_id'])) {
    header('location: ../cabinet.php');
  }
  if (isset($_SESSION['driver_id'])) {
    header('location: ../application.php');
  }
?>
<?php include('header.php') ?>
<form action="registration.php" method="get" style="text-align: center;"><button type="submit" class="btn" style="font-family:Perfect DOS VGA\ 437 Win; font-size:28px;">Register Merchant Account</button></form>
<p></p>
<form action="login.php" method="get" style="text-align: center;"><button type="submit" class="btn"style="font-family:Perfect DOS VGA\ 437 Win; font-size:28px;">Log Into Mechant Account</button></form>
<?php include('errors.php'); ?>
<?php include('footer.php') ?>