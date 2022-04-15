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
<div style="text-align: center;">
<img src="media/reg.gif">
</div>
  <form method="post" action="registration.php" style="display: table;  width: 300px; transform: scale(1.21); margin-top: 50px; margin-left:200px">
  	<div class="input-group" style="display:table-row;">
  	  <label style="display:table-cell">Name</label>
  	  <input type="text" name="name" style="display:table-cell">
  	</div>
  	<div class="input-group" style="display:table-row;">
  	  <label style="display:table-cell">Password</label>
  	  <input type="password" name="passwd" style="display:table-cell">
  	</div>
  	<div class="input-group" style="display:table-row;">
  	  <label style="display:table-cell">Confirm password</label>
  	  <input type="password" name="passwd_confirm" style="display:table-cell">
  	</div>
  	<div class="input-group" style="display:table-row;">
  	  <button type="submit" class="btn" name="register" style="display:table-cell">Submit</button>
  	</div>
  </form>
    <div style="margin-top:100px">
  <?php include('errors.php'); ?>
</div>
<?php include('footer.php') ?>