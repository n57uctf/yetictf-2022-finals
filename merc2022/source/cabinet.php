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
<p>Your Merchant ID: <strong><?php echo $_SESSION['merc_id']; ?></strong></p>
<section class="tabs">
  <menu role="tablist" aria-label="Sample Tabs">
    <button role="tab" aria-selected="true" aria-controls="tab-A">Parsels</button>
    <button role="tab" aria-controls="tab-C">Drivers</button>
  </menu>
  <article role="tabpanel" id="tab-A" style="width:670px">
<?php include('track.php'); ?>
  </article>
  <article role="tabpanel" hidden id="tab-C" style="width:650px">
  <section class="tabs">
  <menu role="tablist" aria-label="Sample Tabs">
    <button role="tab" aria-selected="true" aria-controls="tab-AA">Trustees</button>
    <button role="tab" aria-controls="tab-CC">Newbies</button>
  </menu>
  <article role="tabpanel" id="tab-AA" style="width:630px">
    <div style="overflow:auto;height:340px">
<?php 
  $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT name FROM drivers WHERE status=1");
  if (pg_num_rows($results) != 0) {
    $columns=0;
    echo "<table><tr><td></td><td></td><td></td><td></td><td></td></tr><tr>";
    $drivers = pg_fetch_all($results);
    foreach ($drivers as &$item) :?>
<?php 
    $columns++; 
    if ($columns < 6) : echo '<td><a href="profile.php?name='.$item['name'].'"><img src="avatars/'.$item['name'].'.png" style="width:100%;height:100%"></a><p style="text-align:center;">'.$item['name'].'</p></td>'; 
    else : $columns=0; echo '</tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td><a href="profile.php?name='.$item['name'].'"><img src="avatars/'.$item['name'].'.png" style="width:100%;height:100%"></a><p style="text-align:center;">'.$item['name'].'</p></td>';
      $columns++;
    endif;
    endforeach;
    if ($columns < 6) : for ($i=$columns;$i<5;$i++): echo '<td></td>'; endfor; echo '</tr><tr><td></td><td></td><td></td><td></td><td></td></tr>'; endif;?>
    </tr>
<?php echo "</table>";
  } else {
    echo "Seem that there's no drivers available";
  }
  ?>
</div>
  </article>
  <article role="tabpanel" id="tab-CC" style="width:630px">
    <div style="overflow:auto;height:340px">
<?php 
  $results = pg_query(pg_connect($_SESSION['db_string']), "SELECT name FROM drivers WHERE status=0");
  if (pg_num_rows($results) != 0) {
    $columns=0;
    echo "<table><tr><td></td><td></td><td></td><td></td><td></td></tr><tr>";
    $drivers = pg_fetch_all($results);
    foreach ($drivers as &$item) :?>
<?php 
    $columns++; 
    if ($columns < 6) : echo '<td><a href="profile.php?name='.$item['name'].'"><img src="avatars/'.$item['name'].'.png" style="width:100%;height:100%"></a><p style="text-align:center;">'.$item['name'].'</p></td>'; 
    else : $columns=0; echo '</tr><tr><td></td><td></td><td></td><td></td><td></td></tr><tr><td><a href="profile.php?name='.$item['name'].'"><img src="avatars/'.$item['name'].'.png" style="width:100%;height:100%"></a><p style="text-align:center;">'.$item['name'].'</p></td>';
      $columns++;
    endif;
    endforeach;
    if ($columns < 6) : for ($i=$columns;$i<5;$i++): echo '<td></td>'; endfor; echo '</tr><tr><td></td><td></td><td></td><td></td><td></td></tr>'; endif;?>
    </tr>
<?php echo "</table>";
  } else {
    echo "Seem that there's no drivers available";
  }
  ?>
</div>
  </article>
  </section>
  </article>
</section>
<script src="media/script.js"></script>
<?php include('footer.php') ?>