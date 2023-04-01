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
<img src="media/driver.gif">
  <form enctype="multipart/form-data" method="post" action="driver.php" style="display: table;  width: 400px; transform: scale(1.21); margin-top: 50px; margin-left:50px">
  	<div class="input-group" style="display:table-row;">
  	  <label style="display:table-cell">Name</label>
  	  <input type="text" name="name" style="display:table-cell">
  	</div>
    <div class="input-group" style="display:table-row">
      <label style="display:table-cell">Vehicle</label>
      <input type="text" name="vehicle" style="display:table-cell">
    </div>
    <input type="hidden" name="MAX_FILE_SIZE" value="900000" />
  	<div class="input-group" style="display:table-row">
  	  <label style="display:table-cell">Avatar upload</label>
  	  <input type="file" name="avatar" accept="image/png" style="display:table-cell">
  	</div>
  	<div class="input-group" style="display:table-row">
  	  <label style="display:table-cell">Driver's license upload</label>
  	  <input type="file" name="license" accept="image/png" style="display:table-cell">
  	</div>
    <div class="input-group" style="display:table-row">
      <label style="display:table-cell">About me</label>
      <input type="text" name="about" style="display:table-cell">
    </div>
    <input type="hidden" type="text" name="status" value="0" />
  	<div class="input-group" style="display:table-row;">
      <p/>
  	  <button type="submit" class="btn" name="driver" style="display:table-cell">Sign up</button>
  	</div>
  </form>
  <form action="driver.php" method="post" style="display: table;  width: 400px; transform: scale(1.21); margin-top: -200px; margin-left:450px; font-smooth:auto">
    <div class="input-group">
      <p>Already applied?</p> 
      <label>Driver ID</label>
      <input type="text" name="driver_id">
      <div class="input-group">
      <button type="submit" name="application" class="btn">Check Status</button></div>
    </div>
  </form>
  <div style="margin-top:100px">
  <?php include('errors.php'); ?>
</div>
<?php include('footer.php') ?>