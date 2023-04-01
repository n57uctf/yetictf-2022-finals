<?php 

  include('server.php');

  if (!isset($_SESSION['merc_id'])) {
    header('location: ../index.php');
  }
  if (isset($_SESSION['driver_id'])) {
    header('location: ../application.php');
  }

?>
<?php include('header.php') ?>
<div>
<?php $db_connect = pg_connect($_SESSION['db_string']);
      $query = "SELECT * FROM drivers WHERE status='1'";
      $results = pg_query($db_connect,$query);
      if (pg_num_rows($results) != 0) {
      $drivers = pg_fetch_all($results);
      echo ' <div style="text-align:center;"><img src="media/request.gif"></div>
<form method="post" action="request.php" style="display: table;  width: 300px; transform: scale(1.21); margin-top: 50px; margin-left:200px">';
    echo '
    <div class="input-group" style="display:table-row;">
      <label style="display:table-cell">Dispatch</label>
      <select name="dispatch" style="display:table-cell">
        <option>East London</option>
        <option>Cape Town</option>
        <option>Germiston</option>
        <option>Johannesburg</option>
        <option>Pretoria</option>
        <option>Durban</option>
        <option>Bloemfontein</option>
        <option>Port Elizabeth</option>
      </select>
    </div>
    <div class="input-group" style="display:table-row;">
      <label style="display:table-cell">Destination</label>
      <select name="destination" style="display:table-cell">
        <option>East London</option>
        <option>Cape Town</option>
        <option>Germiston</option>
        <option>Johannesburg</option>
        <option>Pretoria</option>
        <option>Durban</option>
        <option>Bloemfontein</option>
        <option>Port Elizabeth</option>
      </select>
    </div>
    <div class="input-group" style="display:table-row;">
      <label style="display:table-cell">Comments</label>
      <input type="text" name="note" style="display:table-cell">
    </div>
    <div class="input-group" style="display:table-row;">
      <label style="display:table-cell">Driver</label>
      <select name="name" style="display:table-cell">';
      foreach ($drivers as &$item) : echo '<option>'.$item['name'].'</option>'; endforeach; 
      echo '
    </select>
    </div>
    <div class="input-group" style="display:table-row;">
      <button type="submit" class="btn" name="request" style="display:table-cell">Send Request</button>
    </div></form><div style="margin-top:100px">'; include('errors.php'); echo '</div>';
      } else { echo "No drivers available :,(";}?>
</div>
<?php include('footer.php') ?>