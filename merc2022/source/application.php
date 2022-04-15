<?php 
  session_start(); 
  if (!isset($_SESSION['driver_id'])) 
  { header('location: ../index.php'); } 
  if (isset($_SESSION['merc_id'])) {
    header('location: ../cabinet.php');
  }
?>

<?php include('header.php') ?>
<div class="content">
  <?php if ($_SESSION['status'] == 0) :?>
    <p><h2 style="text-align:center;">Newbie Driver's profile</h2></p>
  <?php elseif ($_SESSION['status'] == 1):?>
    <p><h2 style="text-align:center;">Trustee Driver's profile</h2></p>
  <?php endif;?>
  <table style="width:700px; text-align: center;">
    <tr>
      <td><strong>Name</strong></td>
      <td><strong>Vehicle</strong></td>
      <td><strong>Picture</strong></td>
      <td><strong>Driver's license</strong></td>
      <td><strong>Driver's ID</strong></td>
    </tr>
    <tr>
  <?php
  echo '
      <td>'.$_SESSION['name'].'</td>
      <td>'.$_SESSION['vehicle'].'</td>
      <td><img src="avatars/'.$_SESSION['name'].'.png" width=100 height=100></td>
      <td><img src="image.php?license" width=100 height=100></td>
      <td>'.$_SESSION['driver_id'].'</td>
    </tr>
  </table>';
  ?>
</div>
<?php include('footer.php') ?>