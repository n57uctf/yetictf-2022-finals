<?php session_start();
  if (!isset($_SESSION['merc_id']) && !isset($_SESSION['driver_id'])) {
  	header('location: ../index.php');
  }?>
<?php include('header.php')?>
<?php 
	if (isset($_GET['name'])) :
	$name = pg_escape_string(pg_connect($_SESSION['db_string']),$_GET['name']);
	$results = pg_query(pg_connect($_SESSION['db_string']), "SELECT * FROM drivers WHERE name='$name' LIMIT 1");
    $driver = pg_fetch_assoc($results);
    echo '<table style="width:700px"><tr><td>Name</td><td>Vehicle</td><td>Picture</td><td>Biography</td></tr>';
	$counter=0; foreach ($driver as &$pos) : if ($counter!=0 && $counter!=1 && $counter!=5) : echo "<td>".$pos."</td>"; endif; if ($counter==3) : echo '<td><img src="avatars/'.$driver['name'].'.png" width=100 height=100></td>'; endif; ++$counter; endforeach;
	echo '</table>';
      echo '
<form method="post" action="request.php" style="display: table;  width: 300px; transform: scale(1.21); margin-top: 70px; margin-left:200px">';
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
		echo '<option>'.$name.'</option>';
      echo '
    </select>
    </div>
    <div class="input-group" style="display:table-row;">
      <button type="submit" class="btn" name="request" style="display:table-cell">Send Request</button>
    </div></form>';
endif;?>
<?php include('footer.php')?>   