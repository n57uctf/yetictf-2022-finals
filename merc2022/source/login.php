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
<img src="media/login.gif">
  <form method="post" action="login.php" style="display: table;  width: 300px; transform: scale(1.21); margin-top: 70px; margin-left:200px">
  	<div class="input-group" style="display:table-row;">
  		<label style="display:table-cell">Name</label>
  		<input type="text" name="name" style="display:table-cell">
  	</div>
  	<div class="input-group" style="display:table-row;">
  		<label style="display:table-cell">Password</label>
  		<input type="password" name="passwd" style="display:table-cell">
  	</div>
  	<div class="input-group" style="display:table-row;">
      <p/>
  		<button type="submit" class="btn" name="login" style="display:table-cell">Login</button>
  	</div>
  </form>
  <?php include('errors.php'); ?>
<?php include('footer.php') ?>